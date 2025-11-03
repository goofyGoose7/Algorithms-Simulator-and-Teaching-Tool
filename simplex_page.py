# imports specific to the Simplex page
from tkinter import *
import tkinter as tk
from NEA_utilities import closeOpen, fontLarge, fontMedium, fontSmall
from menu_code import Menu
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fractions import Fraction

class Simplex(Menu):
    def __init__(self, master, pUsername, show_menu=True):
        Menu.__init__(self, master, 12, 14)
        self.username = pUsername
        self.textConstraints = [] # for widgets
        self.valueConstraints = []
        self.valueObjective = []
        self.tableau = np.array([], dtype=float) # empty numpy array
        self.canvas = None
        self.currentStep = 0
        self.simplexPath = [(0,0)]
        self.simplexWidgets()
        if show_menu:
            self.menuWidgets()
            self.menuText["text"] = "Use right/left arrow keys to step forward/back\nthrough the visualisation when paused."
        self.invalid = False
        
    def simplexWidgets(self):
        self.master.configure(bg="#eaebed")
        self.master.geometry("845x470")
        self.simplexFrame = Frame(self.master, bg="#eaebed")
        self.simplexFrame.grid(row=0, column=0, columnspan=14, rowspan=12)
        
        self.title = Label(self.simplexFrame, text="Simplex Algorithm Visualisation", font=fontLarge, bg="#eaebed", fg="#1b263b")
        self.title.grid(row=0, column=0, columnspan=12) # change columnspan
        Button(self.simplexFrame, text="Home", command=self.openHome, bg="#1b263b", fg="white", font=fontMedium, width=15).grid(row=0, column=12, columnspan=2)
        
        Label(self.simplexFrame, text=
              "1. Turn the inequalities into equalities by adding a slack variable. Rearrange the objective function\nto be equal to 0. Input these equations into the simplex tableau.\n"
              "2. Choose the most negative value in the objective row to become the basis.\n"
              "3. Work out the θ‐values for each row. Using the smallest (but not negative) value, select the pivot.\n"
              "4. Divide the pivot row by the value of the pivot.\n"
              "5. Add or subtract multiple of the pivot row from the other rows so that the basis variable is 0.\n"
              "6. Repeat until the objective row contains no negative entries.\n"
              "7. Read off the optimal solution from the tableau,",
              font=fontSmall,
              fg="#1b263b",
              bg="#eaebed",
              justify="left").grid(row=1, column=0, rowspan=3, columnspan=14, sticky="w")
        
        # constraint 1:
        Label(self.simplexFrame, text="Constraint 1:", font=fontSmall, bg="#eaebed", fg="#606c38").grid(row=4, column=8)
        self.addConstraint(4)
        # constraint 2:
        Label(self.simplexFrame, text="Constraint 2:", font=fontSmall, bg="#eaebed", fg="#b2675e").grid(row=5, column=8)
        self.addConstraint(5)
        # constraint 3 button:
        self.constraintButton = Button(self.simplexFrame, text="Add constraint", command=lambda: self.addConstraint(6), bg="#1b263b", fg="white", font=fontMedium, width=15)
        self.constraintButton.grid(row=6, column=9, columnspan=3)
        # objective:
        Label(self.simplexFrame, text="Objective function:", font=fontMedium, bg="#eaebed", fg="#1b263b").grid(row=7, column=8, columnspan=4)
        Label(self.simplexFrame, text="P =", font=fontSmall, bg="#eaebed", fg="#1b263b").grid(row=8, column=8)
        xEntry = Entry(self.simplexFrame, width=5)
        xEntry.grid(row=8, column=9)
        Label(self.simplexFrame, text=" x + ", font=fontSmall, bg="#eaebed", fg="#1b263b").grid(row=8, column=10)
        yEntry = Entry(self.simplexFrame, width=5)
        yEntry.grid(row=8, column=11)
        Label(self.simplexFrame, text=" y", font=fontSmall, bg="#eaebed", fg="#1b263b").grid(row=8, column=12)
        self.objectiveText = {"x": xEntry,
                              "y": yEntry}
        
        # visualise:
        Button(self.simplexFrame, text="Visualise", command=self.validate, bg="#1b263b", fg="white", font=fontMedium, width=15).grid(row=9, column=10, columnspan=3)
        # invalid:
        self.invalidMessage = Label(self.simplexFrame, text="", font=fontMedium, bg="#eaebed", fg="#990000")
        self.invalidMessage.grid(row=10, column=8, columnspan=6, rowspan=2)
        
    def openHome(self):
        closeOpen(self.master, "home", self.username)
        
    def addConstraint(self, row):
        #print("in add constraint")
        if row == 6:
            self.constraintButton.destroy()
            Label(self.simplexFrame, text="Constraint 3: ", font=fontSmall, bg="#eaebed", fg="#eca400").grid(row=6, column=8)
        
        xEntry = Entry(self.simplexFrame, width=5)
        xEntry.grid(row=row, column=9)
        Label(self.simplexFrame, text=" x + ", font=fontSmall, bg="#eaebed", fg="#1b263b").grid(row=row, column=10)
        yEntry = Entry(self.simplexFrame, width=5)
        yEntry.grid(row=row, column=11)
        Label(self.simplexFrame, text=" y ≤ ", font=fontSmall, bg="#eaebed", fg="#1b263b").grid(row=row, column=12)
        rhsEntry = Entry(self.simplexFrame, width=5)
        rhsEntry.grid(row=row, column=13)
        
        self.textConstraints.append({
            "x": xEntry,
            "y": yEntry,
            "rhs": rhsEntry})
    
    def validate(self):
        #print("in validate")
        # validate constriants
        # reset lists before revalidating
        self.valueConstraints = []
        self.valueObjective = []
        for constraint in self.textConstraints:
            try:
                x = float(constraint["x"].get())
                y = float(constraint["y"].get())
                rhs = float(constraint["rhs"].get())
                if x == 0.0 and y == 0.0:
                    raise ValueError
                if x < -10.0 or x > 10.0:
                    raise ValueError
                if y < -10.0 or y > 10.0:
                    raise ValueError
                if rhs < -10.0 or rhs > 10.0:
                    raise ValueError
                self.valueConstraints.append([x,y,rhs])
                print(x, y, rhs)
            except ValueError:
                self.invalidMessage["text"] = '''Invalid constraint entry: please ensure that all numbers entered\n
are between -10 and 10, with the x\nand y coefficients not both being 0.'''
                self.valueConstraints = []
                return
        #print("constraints valid")
        # validate objective
        try:
            x = float(self.objectiveText["x"].get())
            y = float(self.objectiveText["y"].get())
            if x == 0.0 and y == 0.0:
                raise ValueError
            if x < -10.0 or x > 10.0:
                raise ValueError
            if y < -10.0 or y > 10.0:
                raise ValueError
            #print("objective valid")
            self.valueObjective.append(x)
            self.valueObjective.append(y)
            #print(x, y)
        except ValueError:
            self.invalidMessage["text"] = '''Invalid objective entry: please ensure that all numbers entered\n
are between -10 and 0, with the x\nand y coefficients not both being 0.'''
            self.valueObjective = []
            return
        # print("fully valid")
        
        '''
        if self.checkFeasible() == False:
            # no feasible region
            self.invalidMessage["text"] = "Invalid: no feasible region."
            return'''
        
        # all validation passed
        self.invalidMessage["text"] = ""
        self.createTableau()
        self.plotConstraints()
        self.master.geometry("1005x858")
        self.simplexSteps()
        if self.invalid == False:
            self.simplexAnimate()
        
            
    def createTableau(self):
        #print("in create tableau")
        numSlackVars = len(self.valueConstraints)
        for i, constraint in enumerate(self.valueConstraints):
            row = constraint[:-1] # take all coefficients except rhs
            row += [1 if j==i else 0 for j in range(numSlackVars)] # add slack variable
            row.append(constraint[-1]) # append rhs value
            if self.tableau.size == 0:
                self.tableau = np.array([row])
            else:
                self.tableau = np.vstack([self.tableau, row])
        # add objective with -ve coefficients as maximising
        objectiveRow = [-c for c in self.valueObjective] + [0]*(numSlackVars +1)
        self.tableau = np.vstack([self.tableau, objectiveRow])
        # check
        #print("initial tableau:")
        #print(self.tableau)
    
    def plotConstraints(self):
        colours = ["#606c38", "#b2675e", "#eca400"]
        
        self.fig, self.ax = plt.subplots(figsize=(5,5))
        for constraint in self.valueConstraints:
            a, b, c = constraint
            #print(a, b, c)
            i = self.valueConstraints.index(constraint)
            xVals = np.linspace(0, 10, 200) # used to plot constriant lines on graph
            if b != 0: # is a line in the form ax + by = c
                yVals = (c - a*xVals) / b
            else: # in the form ax = c
                xVals = np.full_like(xVals, c / a)
                yVals = np.linspace(0, 10, 200)
            self.ax.plot(xVals, yVals, label=f"Constraint {i+1}", color=colours[i])
        
        self.ax.set_xlim(0,10)
        self.ax.set_ylim(0,10)
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend()
        self.ax.grid()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.simplexFrame)
        self.canvas.get_tk_widget().grid(row=4, column=0, rowspan=8, columnspan=8)
        self.canvas.draw()
                
        
        
    def isOptimal(self):
        #print("in is optimal")
        # checks all values in objective row except rhs are non-negative
        return np.all(self.tableau[-1, :-1] >= -1e-9)
    
    
    def findPivotColumn(self):
        # find most negative coef in objective row
        return np.argmin(self.tableau[-1, :-1])
    
    
    def findPivotRow(self, pivotColumn):
        # find row by doing rhs/pivot column value - least positive
        ratios = []
        for i in range(len(self.valueConstraints)):
            if self.tableau[i, pivotColumn] > 0:
                ratios.append(self.tableau[i, -1] / self.tableau[i, pivotColumn])
            else:
                ratios.append(float("inf")) # ignores negative or 0 values
                
        pivotRow = np.argmin(ratios)
        if ratios[pivotRow] == float("inf"):
            #print("No valid pivot row found. solution unbounded.")
            return -1
        return pivotRow
    
    
    def pivot(self, row, column):
        # perform row op to change values by Gaussian elimination style row reduction
        pivotValue = self.tableau[row, column]
        
        # 1: make pivot element 1
        self.tableau[row] = self.tableau[row] / pivotValue
        
        # 2: row reduction
        for i in range(len(self.tableau)):
            if i != row:
                multiplier = self.tableau[i, column]
                self.tableau[i] -= multiplier * self.tableau[row]
        #print("Updated tableau after pivot:")
        #print("Tableau after pivot")
        #print(self.tableau)
        
        
    def getVariableValue(self, varIndex):
        # find row where variable is basic
        column = self.tableau[:, varIndex] # selects all rows in varIndex column
        basicRow = -1
        
        for i in range(len(column) -1): # ignores last row as this is the objective function
            if abs(column[i]-1) < 1e-9: # avoids rounding error of 0.999999999
                # ensure all other coefficients in row are 0
                if np.count_nonzero(column)==1: 
                    basicRow = i
                    break
        #print("basic row is:", basicRow)
        # variable is basic returns value in rightmost column, variable not basic returns 0
        return self.tableau[basicRow, -1] if basicRow != -1 else 0
        
        
    def updateSimplexGraph(self):
        #print("in update simplex graph")
        self.ax.clear()
        
        # replot constraints
        self.plotConstraints()
        
        # draw path of visited points
        if self.currentStep > 0:
            xPath, yPath = zip(*self.simplexPath[:self.currentStep +1])
            self.ax.plot(xPath, yPath, "ro-", linewidth=3, markersize=5)
        self.canvas.draw()
        
        
    def simplexSteps(self):
        #print("in simplex steps")
        self.steps = [(0,0,0)]
        x,y,P = 0,0,0
        while not self.isOptimal():
            #print("in new step loop")
            pivotColumn = self.findPivotColumn()
            #print("pivot column:", pivotColumn)
            pivotRow = self.findPivotRow(pivotColumn)
            #print("pivot row:", pivotRow)
            
            # check for unbounded:
            if self.tableau[pivotRow, pivotColumn] <= 0 :
                self.invalidMessage["text"] = "Unbounded solution."
                self.invalid = True
                return
            self.invalid = False
            
            #print("Tableau before pivot:")
            #print(self.tableau)
            
            self.pivot(pivotRow, pivotColumn)
            
            # steps append ...
            x = Fraction(self.getVariableValue(0)).limit_denominator() # x is in tableau column 0
            y = Fraction(self.getVariableValue(1)).limit_denominator() # y is in column index 1
            P = Fraction(self.tableau[-1][-1]).limit_denominator()
            #print("At this step:")
            #print("x, y, P:", x, y, P)
            self.steps.append((x,y,P))
            self.simplexPath.append((x,y))
            
        #print("tableau is optimal")
        self.steps.append((x,y,P))
        #print("steps:")
        #print(self.steps)
        
    def simplexAnimate(self):
        #print("in simplex animate")
        if self.currentStep < len(self.steps)-1 and not self.isPaused:
            self.updateSimplexGraph()
            self.currentStep += 1
            self.master.after(1000, self.simplexAnimate) # change time for smoothness
        elif self.currentStep == len(self.steps)-1:
            self.updateSimplexGraph()
            self.invalidMessage["text"] = f"Optimal solution P = {self.steps[-1][2]}\nx = {self.steps[-1][0]}, y = {self.steps[-1][1]}"
            
# for testing ------------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simplex test")
    #root.geometry("800x595")
    graph_input = Simplex(root, "HelloWord!!!") #HellowWord!!! username for testing purposes
    root.mainloop()
        
    