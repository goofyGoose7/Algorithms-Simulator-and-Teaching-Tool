# imports specific to the BubbleSort class
from tkinter import *
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # allows matplotlib graph to be put in tkinter window
from menu_code import Menu
from NEA_utilities import closeOpen, fontLarge, fontMedium, fontSmall


class BubbleSort(Menu):
    def __init__(self, master, pUsername, show_menu=True):
        Menu.__init__(self, master, 12, 19)
        self.numbers = []
        self.userEntries = []
        
        self.username = pUsername
        
        self.master.configure(bg="#eaebed")
        self.master.geometry("1105x905") # required here as goes back into HomeMain first
        
        self.sortOrder = StringVar(value="Ascending")
        
        self.invalidMessage = None
        
        self.fig = None
        self.ax = None
        self.canvas = None
        
        self.visualiseText = None
        
        self.numberPasses = 0
        
        self.bubbleSortWidgets()
        if show_menu:
            self.menuWidgets()
        
        
    def bubbleSortWidgets(self):
        # BUBBLE SORT FRAME:
        self.bubbleSortFrame = Frame(self.master, bg="#eaebed")
        self.bubbleSortFrame.grid(row=0, column=0, columnspan=19, rowspan=12)
        
        # TITLE / TOP SECTION:
        self.title = Label(self.bubbleSortFrame, text="Bubble Sort Algorithm Visualisation", font=fontLarge, fg="#1b263b", bg="#eaebed")
        self.title.grid(row=0, column=0, columnspan=17)
        
        Button(self.bubbleSortFrame, text="Home", command=self.openHome, bg="#1b263b", fg="white", font=fontMedium, width=15).grid(row=0, column=17, columnspan=2)
        
        Label(self.bubbleSortFrame,
              text= "1. Start at the first item in the list.\n"
                    "2. Compare the current item with the next item.\n"
                    "3. If the two items are in the wrong position, swap them.\n"
                    "4. Move up one item to the next time in the list.\n"
                    "5. Repeat from step 3 until all the unsorted items have been compared.\n"
                    "6. If any items were swapped, repeat from step 1. Otherwise, the algorithm is complete.",
              font=fontSmall,
              fg="#1b263b",
              bg="#eaebed",
              justify="left").grid(row=1, column=0, columnspan=19, sticky="w", padx=10, pady=5) # justify aligns the text to the left within the label
        
        # create 8 entry fields for user to enter numbers into
        self.entryFrame = Frame(self.bubbleSortFrame, bg="#eaebed")
        self.entryFrame.grid(row=4, column=7, columnspan=12, rowspan=2)
        for i in range(8):
            entry = Entry(self.entryFrame, width=3)
            entry.grid(row=0 , column=(i+7), padx=2)
            #print(f"userEntries: {self.userEntries}")
            self.userEntries.append(entry)
        #print(f"userEntries: {self.userEntries}")
        
        self.addButton = Button(self.entryFrame, text="Add Number", command=self.addEntry, bg="#1b263b", fg="white", font=fontMedium, width=15)
        self.addButton.grid(row=1, column=15, columnspan=4)
        
        # ascending descending choice:
        Radiobutton(self.bubbleSortFrame, text="Ascending", variable=self.sortOrder, value="Ascending", font=fontSmall, fg="#1b263b", bg="#eaebed").grid(row=10, column=0, columnspan=3)
        Radiobutton(self.bubbleSortFrame, text="Descending", variable=self.sortOrder, value="Descending", font=fontSmall, fg="#1b263b", bg="#eaebed").grid(row=10, column=3, columnspan=3)
        
        Button(self.bubbleSortFrame, text="Visualise", command=self.validate, bg="#1b263b", fg="white", font=fontMedium, width=20).grid(row=10, column=11, columnspan=4)
        
        self.invalidMessage = Label(self.bubbleSortFrame, text="", font=fontSmall, fg="#990000", bg="#eaebed")
        self.invalidMessage.grid(row=11, columnspan=19)
        
        # dataset plot
        self.fig, self.ax = plt.subplots(figsize=(5,5))
        self.ax.set_xticks([])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.bubbleSortFrame)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=7, rowspan=5, pady=5)
        
        self.visualiseText = Text(self.bubbleSortFrame, width=50, height=30)
        self.visualiseText.grid(row=6, column=7, columnspan=12, rowspan=4)
        
    def addEntry(self):
        #print("in add entry")
        if len(self.userEntries) < 11:
            entry = Entry(self.entryFrame, width=3)
            entry.grid(row=0, column=(7+len(self.userEntries)))
            self.userEntries.append(entry)
        elif len(self.userEntries) == 11:
            entry = Entry(self.entryFrame, width=3)
            entry.grid(row=0, column=(7+len(self.userEntries)))
            self.userEntries.append(entry)
            self.addButton.grid_forget()
            
    def updateChart(self, numbers, swapIndices=None):
        # this is for animating the swapping of items on the bar chart
        #print("in update chart")
        self.ax.clear()
        barColours = ["#606c38"] * len(numbers) # all bars blue
        if swapIndices: # not None
            for index in swapIndices:
                barColours[index] = "#b2675e" # swapping items in red
        self.ax.bar(range(len(numbers)), numbers, color=barColours)
        self.canvas.draw()
        self.bubbleSortFrame.update()
        #time.sleep(0.3) # smooth animation
    
            
    def validate(self):
        #print("in validate")
        for entry in self.userEntries:
            try:
                num = int(entry.get())
                if 1 <= num <= 100:
                    self.numbers.append(num)
                else:
                    raise ValueError
            except ValueError:
                self.invalidMessage["text"] = "Invalid dataset: all values must be integers between 1 and 100"
                self.numbers = []
                return
            
        if len(self.numbers) < 8 or len(self.numbers) > 12:
            #print("in length error")
            self.invalidMessage["text"] = "Invalid dataset: the dataset must consist of between 8 and 12 numbers (inclusive)"
            self.numbers = []
            return
        
        self.invalidMessage["text"] = ""
        self.bubbleSortSteps()
        #print(self.steps)
        #print(self.stepsDictionary)
        self.bubbleSortAnimate()
        
        
    def bubbleSortSteps(self):
        #print("in bubble sort steps")
        n = len(self.numbers)
        swapped = True
        stepsDict = {}
        stepsDict[tuple(self.numbers)] = [0]
        
        if self.sortOrder.get() == "Ascending":
            while swapped:
                swapped = False
                for j in range(n-1):
                    if self.numbers[j] > self.numbers[j+1]:
                        temp= self.numbers[j]
                        self.numbers[j] = self.numbers[j+1]
                        self.numbers[j+1] = temp
                        swapped = True
                        #self.steps.append(self.numbers[:])
                        # note must be tuple because lists are mutable so they are unhashable
                        stepsDict[tuple(self.numbers)] = [j, j+1]
                if swapped:
                    self.numberPasses += 1
        elif self.sortOrder.get() == "Descending":
            while swapped:
                swapped = False
                for j in range(n-1):
                    if self.numbers[j] < self.numbers[j+1]:
                        temp= self.numbers[j]
                        self.numbers[j] = self.numbers[j+1]
                        self.numbers[j+1] = temp
                        swapped = True                        
                        #self.steps.append(self.numbers[:])
                        # note must be tuple because lists are mutable so they are unhashable
                        stepsDict[tuple(self.numbers)] = [j, j+1]
                if swapped:
                    self.numberPasses += 1
                    
        self.stepsDictionary = stepsDict
        self.steps = list(self.stepsDictionary.keys())
        
    def bubbleSortAnimate(self):
        #print("in bubble sort animate")
        if not self.isPaused and self.currentStep < len(self.steps)-1:
            numbers = self.steps[self.currentStep]
            indices = self.stepsDictionary[numbers]
            self.updateChart(numbers, indices)
            self.visualiseText.insert(tk.END, f"{numbers}\n")
            self.visualiseText.see(tk.END)
            
            self.bubbleSortFrame.update()
            self.currentStep += 1
            self.master.after(750, self.bubbleSortAnimate)
            
        elif not self.isPaused and self.currentStep == len(self.steps)-1:
            numbers = self.steps[self.currentStep]
            indices = self.stepsDictionary[numbers]
            self.updateChart(numbers, indices)
            self.visualiseText.insert(tk.END, f"{numbers}\n")
            self.visualiseText.see(tk.END)
            #print("sort complete")
            self.invalidMessage["text"] = "Sort complete"
            self.bubbleSortFrame.update()
            
        
    def openHome(self):
        closeOpen(self.master, "home", self.username)

# for testing --------------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("BubbleSort test")
    #root.geometry("800x595")
    graph_input = BubbleSort(root, "HelloWord!!!") #HellowWord!!! username for testing purposes
    root.mainloop()
