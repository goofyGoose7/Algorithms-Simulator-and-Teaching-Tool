# imports required specific to the HomeMain class
from tkinter import *
import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # allows matplotlib graph to be put in tkinter window
from PIL import Image, ImageTk # for logo image editing
from main_class_code import Main
from NEA_utilities import closeOpen, fontLarge, fontMedium, fontSmall


class HomeMain(Main):
    def __init__(self, master, pUsername):
        #print(f"inside HomeMain __init__")
        super().__init__(master)
        #print("Back inside HomeMain __init__")
        self.homeFrame = None
        
        # current account username:
        self.currentAccUsername = pUsername
        self.accountType = self.accountTypeGet()
                
        if self.accountType == "Student":
            # holds algorithm names to go as labels on the x axis
            self.algorithmNames = self.algorithmAxisValues("Name")
            # hold the correct and incorrect scores to be plot as bars on the bar chart
            self.correctScores = self.algorithmAxisValues("Correct")
            self.incorrectScores = self.algorithmAxisValues("Incorrect")
            self.master.geometry("1150x740")
        
        elif self.accountType == "Teacher":
            self.algorithmNames = self.teacherAlgorithmsGet()
            self.master.geometry("935x775")
        
        self.logoImg = None
        self.master.configure(bg="#eaebed")
        HomeMain.pageStarter(self)
        
    def pageStarter(self):
        self.homeWidgets()
        if self.accountType == "Student":
            self.plotStatistics()
        elif self.accountType == "Teacher":
            self.displayLogo()
        
        
    def accountTypeGet(self):
        usernameHolder = self.currentAccUsername
        #print(usernameHolder)
        self.cursor.execute("SELECT Account_type FROM Users WHERE Username=?", (usernameHolder,))
        result = self.cursor.fetchone()
        print(f"result: {result}")
        accountType = result[0]
        #print(accountType)
        return accountType
        
    def teacherAlgorithmsGet(self):
        usernameHolder = self.currentAccUsername
        algorithmList = []
        self.cursor.execute("SELECT Algorithm FROM TeacherEnrolment WHERE Username=?", (usernameHolder,))
        result = self.cursor.fetchall()
        #print(result)
        algorithmList = [row[0] for row in result]
        #print(algorithmList)
        return algorithmList
        
    def homeWidgets(self):
        self.title = Label(self.master, text="Algorithm's Simulator and Teaching Tool", font=fontLarge, fg="#1b263b", bg="#eaebed")
        self.title.grid(row=0, column=0, columnspan=5)
        
        self.homeFrame = Frame(self.master, bg="#eaebed")
        
        buttonLocations = self.locations()
        #print(buttonLocations)
        # the index of each item in the list is the column of it in the gui
        if "Bubble Sort" in buttonLocations:
            Button(self.homeFrame, text="Bubble Sort", command=self.openBubbleSort, activebackground="white", activeforeground="#1b263b",
                   bg="#1b263b", fg="white", font=fontMedium, width=20).grid(row=1, column=buttonLocations.index("Bubble Sort"), padx=10, pady=5) #bubble sort button
        if "Prim's" in buttonLocations:
            Button(self.homeFrame, text="Prim's Algorithm", command=self.openPrim, activebackground="white", activeforeground="#1b263b",
                   bg="#1b263b", fg="white", font=fontMedium, width=20).grid(row=1, column=buttonLocations.index("Prim's"), padx=10, pady=5) # prim's button
        if "Dijkstra's" in buttonLocations:
            Button(self.homeFrame, text="Dijkstra's Algorithm", command=self.openDijkstra, activebackground="white", activeforeground="#1b263b",
                   bg="#1b263b", fg="white", font=fontMedium, width=20).grid(row=1, column=buttonLocations.index("Dijkstra's"), padx=10, pady=5) # dijkstra button
        if "Simplex" in buttonLocations:
            Button(self.homeFrame, text="Simplex Algorithm", command=self.openSimplex, activebackground="white", activeforeground="#1b263b",
                   bg="#1b263b", fg="white", font=fontMedium, width=20).grid(row=1, column=buttonLocations.index("Simplex"), padx=10, pady=5) # simplex button
        if "Quiz" in buttonLocations:
            Button(self.homeFrame, text="Quiz", command=self.openQuiz, activebackground="white", activeforeground="#1b263b", bg="#1b263b",
                   fg="white", font=fontMedium, width=20).grid(row=1, column=buttonLocations.index("Quiz"), padx=10, pady=5) # quiz button
        
        if self.accountType == "Student":
            Button(self.homeFrame, text="Logout", command=self.logout, activebackground="white", activeforeground="#1b263b", bg="#1b263b",
                   fg="white", font=fontMedium, width=20).grid(row=4, column=4, padx=10, pady=5) # logout button Student
        elif self.accountType == "Teacher":
            Button(self.homeFrame, text="Logout", command=self.logout, activebackground="white", activeforeground="#1b263b", bg="#1b263b",
                   fg="white", font=fontMedium, width=20).grid(row=7, column=3, padx=10, pady=5) # logout button Teacher
        self.homeFrame.grid(row=1, column=0, columnspan=5)
        
    
    def locations(self):
        try:
            buttonLocations = []
            if self.accountType == "Student":
                for counter in range (len(self.algorithmNames)-1):
                    buttonLocations.append(self.algorithmNames[counter])
                buttonLocations.append("Quiz")
            elif self.accountType == "Teacher":
                buttonLocations = self.algorithmNames
            return buttonLocations
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    
    def algorithmAxisValues(self, listType):
        valuesList = []
        try:
            self.cursor.execute("SELECT Algorithm, CorrectScore, IncorrectScore FROM StudentEnrolment WHERE Username = ?", (self.currentAccUsername,))  
            results = self.cursor.fetchall()
            #print(results)
            if listType == "Name":
                for row in results:
                    valuesList.append(row[0])
                valuesList.append("Total")
                #self.algorithmNames = valuesList
            elif listType == "Correct":
                totalCorrect = 0
                for row in results:
                    valuesList.append(row[1])
                    totalCorrect += row[1]
                valuesList.append(totalCorrect)
                #self.correctScores = valuesList
            elif listType == "Incorrect":
                totalIncorrect = 0
                for row in results:
                    valuesList.append(row[2])
                    totalIncorrect += row[2]
                valuesList.append(totalIncorrect)
                #self.incorrectScores = valuesList
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        return valuesList
        
    def plotStatistics(self):
        # create figure and axes for the bar chart
        # fig = entire chart (figure) area
        # ax represents the axes where the bars are plotted
        #print(f"Correct Scores: {self.correctScores}")
        #print(f"Incorrect Scores: {self.incorrectScores}")
        fig, ax = plt.subplots(figsize=(5,5)) 
        x = range(len(self.algorithmNames))
        
        # plot the bars
        ax.bar(x, self.correctScores, width=0.3, label="Correct", align="center", color="#606c38")
        ax.bar([p + 0.3 for p in x], self.incorrectScores, width=0.3, label = "Incorrect", align = "center", color = "#b26754")
        
        # labels, title, legend
        ax.set_xlabel("Algorithms", fontsize=11, fontfamily="Calibri", color="#1b263b")
        ax.set_ylabel("Score", fontsize=11, fontfamily="Calibri", color="#1b263b")
        ax.set_title("Quiz Statistics", fontsize=12, fontfamily="Calibri", color="#1b263b")
        ax.set_xticks([p + 0.3 for p in x])
        ax.set_xticklabels(self.algorithmNames, fontsize=10, fontfamily="Calibri", color="#1b263b")
        ax.legend()
        
        # embed into Tkinter
        canvas = FigureCanvasTkAgg(fig, self.homeFrame)
        canvasWidget = canvas.get_tk_widget()
        canvasWidget.grid(row=2, column=1, columnspan=3)     # rowspan = 4
        canvasWidget.config(bg="#eaebed")
        
    def displayLogo(self):
        # open the image
        image = Image.open("NEA_logo_image.png")
        image = image.resize((481,626))
        self.logoImg = ImageTk.PhotoImage(image) # creates tkinter widget
        
        # create a label and set the image
        imageLabel = Label(self.homeFrame, image=self.logoImg)
        imageLabel.grid(row=2, column=0, columnspan=4, rowspan=5)
        
        

    def openBubbleSort(self):
        usernameHolder = self.currentAccUsername
        closeOpen(self.master, "bubble sort", usernameHolder)
    
    def openPrim(self):
        usernameHolder = self.currentAccUsername
        closeOpen(self.master, "prim", usernameHolder)
        
    def openDijkstra(self):
        usernameHolder = self.currentAccUsername
        closeOpen(self.master, "dijkstra", usernameHolder)
        
    def openSimplex(self):
        usernameHolder = self.currentAccUsername
        closeOpen(self.master, "simplex", usernameHolder)
        
    def openQuiz(self):
        usernameHolder = self.currentAccUsername
        closeOpen(self.master, "quiz", usernameHolder)

    def logout(self):
        closeOpen(self.master, "login")
        
    def hideHomeWidgets(self):
        for widget in self.homeFrame.winfo_children():
            widget.grid_forget()
        self.title.grid_forget()

