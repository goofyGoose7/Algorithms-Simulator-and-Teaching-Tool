# imports specific to the Quiz class
from tkinter import *
import tkinter as tk
import sqlite3 # for writing scores to the database
from NEA_utilities import closeOpen, fontLarge, fontMedium, fontSmall
from main_class_code import Main
from PIL import Image, ImageTk # for logo image editing
from random import randint, shuffle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bubble_sort_page import BubbleSort
from prim_page import Prim
from dijkstra_page import Dijkstra
from simplex_page import Simplex
from fractions import Fraction
import networkx as nx
import heapq


class Quiz(Main):
    def __init__(self, master, pUsername):
        super().__init__(master)
        self.master = master
        self.username = pUsername
        self.currentQType = None
        
        # instances of algorithm classes - composition:
        self.bubbleSort = BubbleSort(master, pUsername, show_menu=False)
        self.prim = Prim(master, pUsername, show_menu=False)
        self.dijkstra = Dijkstra(master, pUsername, show_menu=False)
        self.simplex = Simplex(master, pUsername, show_menu=False)
        
        # hide algorithm frames to avoid interference
        self.bubbleSort.bubbleSortFrame.grid_forget()
        self.prim.primFrame.grid_forget()
        self.dijkstra.dijkstraFrame.grid_forget()
        self.simplex.simplexFrame.grid_forget()
        
        self.userAlgorithmLocations = self.accountAlgorithms()
        
        self.initialQuizWidgets()

    def initialQuizWidgets(self):
        self.master.configure(bg="#eaebed")
        self.master.geometry("930x730")
        
        self.title = Label(self.master, text="Quiz", font=fontLarge, bg="#eaebed", fg="#1b263b")
        self.title.grid(row=0, column=0, columnspan=10)
        Button(self.master, text="Home", command=self.openHome, bg="#1b263b", fg="white", font=fontMedium, width=15).grid(row=0, column=10, columnspan=2, padx=5, pady=1)
        
        if "Bubble Sort" in self.userAlgorithmLocations:
            self.bubbleSortButton = Button(self.master, text="Bubble Sort", command=lambda: self.newType("Bubble Sort"), bg="#1b263b", fg="white", font=fontMedium, width=20)
            self.bubbleSortButton.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        
        if "Prim's" in self.userAlgorithmLocations:
            primColumn = self.userAlgorithmLocations.index("Prim's") * 3
            self.primButton = Button(self.master, text="Prim's", command=lambda: self.newType("Prim's"), bg="#1b263b", fg="white", font=fontMedium, width=20)
            self.primButton.grid(row=1, column=primColumn, columnspan=3, padx=5, pady=5)
        
        if "Dijkstra's" in self.userAlgorithmLocations:
            dijkstraColumn = self.userAlgorithmLocations.index("Dijkstra's") * 3
            self.dijkstraButton = Button(self.master, text="Dijkstra's", command=lambda: self.newType("Dijkstra's"), bg="#1b263b", fg="white", font=fontMedium, width=20)
            self.dijkstraButton.grid(row=1, column=dijkstraColumn, columnspan=3, padx=5, pady=5)
        
        if "Simplex" in self.userAlgorithmLocations:
            simplexColumn = self.userAlgorithmLocations.index("Simplex") * 3
            self.simplexButton = Button(self.master, text="Simplex", command=lambda: self.newType("Simplex"), bg="#1b263b", fg="white", font=fontMedium, width=20)
            self.simplexButton.grid(row=1, column=simplexColumn, columnspan=3, padx=5, pady=5)
        
        
        image = Image.open("NEA_logo_image.png")
        image = image.resize((481,626))
        self.logoImg = ImageTk.PhotoImage(image) # creates tkinter widget
        self.imageLabel = Label(self.master, image=self.logoImg)
        self.imageLabel.grid(row=2, column=3, columnspan=6, rowspan=8)
        
        
    def bubbleSortQuizWidgets(self):
        # widgets for bubbleSort frame
        #print("in bubbleSort quiz widgets")
        
        self.bubbleSortButton["bg"] = "#b2675e"
        
        self.bubbleSortQuizFrame = Frame(self.master, bg="#eaebed")
        self.bubbleSortQuizFrame.grid(row=2, column=0, columnspan=12, rowspan=8)
        
        Label(self.bubbleSortQuizFrame,
              text= "1. Start at the first item in the list.\n"
                    "2. Compare the current item with the next item.\n"
                    "3. If the two items are in the wrong position, swap them.\n"
                    "4. Move up one item to the next time in the list.\n"
                    "5. Repeat from step 3 until all the unsorted items have been compared.\n"
                    "6. If any items were swapped, repeat from step 1. Otherwise, the algorithm is complete.",
              font=fontSmall,
              fg="#1b263b",
              bg="#eaebed",
              justify="left").grid(row=2, column=0, columnspan=12, sticky="w", padx=10, pady=5)
        
        Label(self.bubbleSortQuizFrame, text="Please sort the following unsorted dataset in ascending order and input the number of passes it took:",
              font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=4, column=0, columnspan=12, padx=2)
        
        self.numLabels = []
        self.numChoices = []
        self.dropdowns = []
        iCounter = 1 # column index counter
        for number in self.quizNumbers:
            numText= str(number)
            label = Label(self.bubbleSortQuizFrame, text=numText, font=fontMedium, fg="#1b263b", bg="#eaebed")
            label.grid(row=5, column=iCounter, padx=1, pady=1)
            self.numLabels.append(label)
            
            var = IntVar()
            var.set(0) # default value
            self.numChoices.append(var)
            
            dropdown = OptionMenu(self.bubbleSortQuizFrame, var, *self.quizNumbers)
            dropdown.grid(row=6, column=iCounter, padx=1, pady=1)
            self.dropdowns.append(dropdown)
            
            iCounter += 1
        
        Label(self.bubbleSortQuizFrame, text="Number of passes = ", font=fontMedium, fg="#1b263b", bg="#eaebed", width=20).grid(row=7, column=0, columnspan=3, padx=5, pady=5)
        
        self.passesInput = IntVar()
        Entry(self.bubbleSortQuizFrame, textvariable=self.passesInput).grid(row=7, column=3, columnspan=3, padx=1, pady=1)
        
        self.answerText = Label(self.bubbleSortQuizFrame, text="", font=fontMedium, fg="#990000", bg="#eaebed")
        self.answerText.grid(row=9, column=0, columnspan=6)
        
        Button(self.bubbleSortQuizFrame, text="Submit", command=self.check, bg="#1b263b", fg="white",
               font=fontMedium, width=20).grid(row=9, column=6, columnspan=3, padx=5, pady=5)
        Button(self.bubbleSortQuizFrame, text="New Question", command=lambda: self.newQuestion("Bubble Sort"), bg="#1b263b", fg="white",
               font=fontMedium, width=20).grid(row=9, column=9, columnspan=3, padx=5, pady=5)
        
        
        
    def primQuizWidgets(self):
        # widgets for prim frame
        #print("in prim quiz widgets")
        
        self.primButton["bg"] = "#b2675e"
        
        self.primQuizFrame = Frame(self.master, bg="#eaebed")
        self.primQuizFrame.grid(row=2, column=0, columnspan=12, rowspan=8)
        
        Label(self.primQuizFrame,
              text= "1. Choose any vertex to start the tree.\n"
                    "2. Choose the edge of least weight that joins a vertex that is already in the tree to a vertex that is not yet in the tree.\n"
                    "3. Repeat step 2 until all the vertices are connected to the tree.",
              font=fontSmall,
              fg="#1b263b",
              bg="#eaebed",
              justify="left").grid(row=2, column=0, columnspan=12, sticky="w", padx=10, pady=5)
        
        Label(self.primQuizFrame,
              text="Start at vertex A.\n Input the MST edges below in the form 'AB, BC' etc:",
              font=fontMedium,
              fg="#1b263b",
              bg="#eaebed",
              justify="left").grid(row=4, column=6, columnspan=6, rowspan=2)
        
        self.mstEntry = StringVar()
        Entry(self.primQuizFrame, textvariable=self.mstEntry, width=35, font=("Arial", 14)).grid(row=6, column=6, columnspan=6, rowspan=2)
        
        Label(self.primQuizFrame, text="MST weight = ", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=8, column=6, columnspan=3)
        self.weightEntry = IntVar()
        Entry(self.primQuizFrame, textvariable=self.weightEntry).grid(row=8, column=9, columnspan=3)
        
        self.answerText = Label(self.primQuizFrame, text="", font=fontMedium, fg="#990000", bg="#eaebed")
        self.answerText.grid(row=9, column=0, columnspan=6)
        
        Button(self.primQuizFrame, text="Submit", command=self.check, bg="#1b263b", fg="white",
               font=fontMedium, width=20).grid(row=9, column=6, columnspan=3, padx=5, pady=5)
        Button(self.primQuizFrame, text="New Question", command=lambda: self.newQuestion("Prim's"), bg="#1b263b", fg="white",
               font=fontMedium, width=20).grid(row=9, column=9, columnspan=3, padx=5, pady=5)
        
        #print(f"graph: {self.quizGraph}")
        # create axes to plot graph on
        self.fig, self.ax = plt.subplots(figsize=(3.5,3.5))
        self.primQuizGraphCanvas = FigureCanvasTkAgg(self.fig, self.primQuizFrame)
        self.primQuizGraphCanvas.get_tk_widget().grid(row=4, column=0, rowspan=5, columnspan=6)
        # draw graph on axes
        pos = nx.spring_layout(self.quizGraph)
        nx.draw(self.quizGraph, pos, with_labels=True, node_color='#606c38', edge_color='black', node_size=200, font_color='white', font_size=11, ax=self.ax)
        edge_labels = nx.get_edge_attributes(self.quizGraph, 'weight')
        nx.draw_networkx_edge_labels(self.quizGraph, pos, edge_labels=edge_labels, font_size=10, ax=self.ax)
        self.primQuizGraphCanvas.draw()
        
        
        
    def dijkstraQuizWidgets(self):
        # widgets for dijkstra frame
        #print("in dijkstra quiz widgets")
        self.dijkstraButton["bg"] = "#b2675e"
        
        self.dijkstraQuizFrame = Frame(self.master, bg="#eaebed")
        self.dijkstraQuizFrame.grid(row=2, column=0, columnspan=12, rowspan=8)
        
        Label(self.dijkstraQuizFrame, text=
              "1. Set the initial distance from the start values for all nodes (0 for the start node and infinity for all other nodes).\n"
              "2. Find the node with the shortest distance from the start that has not been visited and look at all the unvisited connected nodes.\n"
              "3. Calculate the distance from the start for each of the unvisited connected nodes. \n"
              "4. If the distance calculated is less than the current shortest distance from the start, set the previous node for that connected\nnode to be the current node. \n"
              "5. Then set the current node as visited.\n"
              "6. Repeat steps 2 to 5 until all nodes are set to visited.\n"
              "To find the shortest path through backtracking:\n"
              "7. Start from the goal node.\n"
              "8. Add the ‘previous node’ to the start of a list.\n"
              "9. Repeat step 7 until the start node is reached.",
              font=fontSmall,
              fg="#1b263b",
              bg="#eaebed",
              justify="left").grid(row=2, column=0, columnspan=12, sticky="w", padx=10, pady=5)
        
        self.startEndText = Label(self.dijkstraQuizFrame,
              text=f"Start at vertex A. End vertex {self.endVertex}.\nInput the shortest path in the form 'ABC...':",
              font=fontMedium,
              fg="#1b263b",
              bg="#eaebed",
              justify="left")
        self.startEndText.grid(row=4, column=6, columnspan=6, rowspan=2)
        
        self.shortestPathEntry = StringVar()
        Entry(self.dijkstraQuizFrame, textvariable=self.shortestPathEntry).grid(row=6, column=6, columnspan=6, rowspan=2)
        
        Label(self.dijkstraQuizFrame, text="Shortest path weight = ", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=8, column=6, columnspan=3)
        self.weightEntry = IntVar()
        Entry(self.dijkstraQuizFrame, textvariable=self.weightEntry).grid(row=8, column=9, columnspan=3)
        
        self.answerText = Label(self.dijkstraQuizFrame, text="", font=fontMedium, fg="#990000", bg="#eaebed")
        self.answerText.grid(row=9, column=0, columnspan=6)
        
        Button(self.dijkstraQuizFrame, text="Submit", command=self.check, bg="#1b263b", fg="white",
               font=fontMedium, width=20).grid(row=9, column=6, columnspan=3, padx=5, pady=5)
        Button(self.dijkstraQuizFrame, text="New Question", command=lambda: self.newQuestion("Dijkstra's"), bg="#1b263b", fg="white",
               font=fontMedium, width=20).grid(row=9, column=9, columnspan=3, padx=5, pady=5)
        
        #print(f"graph: {self.graph}")
        # create axes to plot graph on
        self.fig, self.ax = plt.subplots(figsize=(3.5,3.5))
        self.dijkstraQuizGraphCanvas = FigureCanvasTkAgg(self.fig, self.dijkstraQuizFrame)
        self.dijkstraQuizGraphCanvas.get_tk_widget().grid(row=4, column=0, rowspan=5, columnspan=6)
        # draw graph on axes
        pos = nx.spring_layout(self.quizGraph)
        nx.draw(self.quizGraph, pos, with_labels=True, node_color='#606c38', edge_color='black', node_size=200, font_color='white', font_size=11, ax=self.ax)
        edge_labels = nx.get_edge_attributes(self.quizGraph, 'weight')
        nx.draw_networkx_edge_labels(self.quizGraph, pos, edge_labels=edge_labels, ax=self.ax)
        self.dijkstraQuizGraphCanvas.draw()
       
       
        
    def simplexQuizWidgets(self):
        # widgets for simplex frame
        #print("in simplex quiz widgets")
        self.simplexButton["bg"] = "#b2675e"
        self.simplexQuizFrame = Frame(self.master, bg="#eaebed")
        self.simplexQuizFrame.grid(row=2, column=0, columnspan=12, rowspan=8)
        
        
        Label(self.simplexQuizFrame, text=
              "1. Turn the inequalities into equalities by adding a slack variable. Rearrange the objective function\nto be equal to 0. Input these equations into the simplex tableau.\n"
              "2. Choose the most negative value in the objective row to become the basis.\n"
              "3. Work out the θ‐values for each row. Using the smallest (but not negative) value, select the pivot.\n"
              "4. Divide the pivot row by the value of the pivot.\n"
              "5. Add or subtract multiple of the pivot row from the other rows so that the basis variable is 0.\n"
              "6. Repeat until the objective row contains no negative entries.\n"
              "7. Read off the optimal solution from the tableau.",
              font=fontSmall,
              fg="#1b263b",
              bg="#eaebed",
              justify="left").grid(row=2, column=0, rowspan=2, columnspan=12, sticky="w", padx=5, pady=5)
        
        self.constraintTexts = []
        for constraint in self.quizConstraints:
            a,b,c = constraint
            text = f"{a}x + {b}y ≤ {c}"
            self.constraintTexts.append(text)
        
        a,b, = self.quizObjective
        self.objectiveText = f"P = {a}x + {b}y"
        
        self.textSayingConstraints = Label(self.simplexQuizFrame, text=
              "Please enter either integers or fractions (e.g. in the form 3/5)\n"+
              "Constraints:\n" + "\n".join(self.constraintTexts) + "\n"
              "Objective: " + self.objectiveText,
              font=fontMedium,
              fg="#1b263b",
              bg="#eaebed",
              justify="left")
        self.textSayingConstraints.grid(row=4, column=7, rowspan=2, columnspan=5, sticky="w", padx=5, pady=5)
        
        Label(self.simplexQuizFrame, text="x = ", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=6, column=6, columnspan=2, padx=5)
        self.xInput = StringVar()
        Entry(self.simplexQuizFrame, textvariable=self.xInput).grid(row=6, column=8, columnspan=2)
        
        Label(self.simplexQuizFrame, text="y = ", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=7, column=6, columnspan=2, padx=5)
        self.yInput = StringVar()
        Entry(self.simplexQuizFrame, textvariable=self.yInput).grid(row=7, column=8, columnspan=2)
        
        Label(self.simplexQuizFrame, text="P = ", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=8, column=6, columnspan=2, padx=5)
        self.pInput = StringVar()
        Entry(self.simplexQuizFrame, textvariable=self.pInput).grid(row=8, column=8, columnspan=2)
        
        
        self.answerText = Label(self.simplexQuizFrame, text="", font=fontMedium, fg="#990000", bg="#eaebed")
        self.answerText.grid(row=9, column=0, columnspan=6)
        
        Button(self.simplexQuizFrame, text="Submit", command=self.check, bg="#1b263b", fg="white",
               font=fontMedium, width=20).grid(row=9, column=6, columnspan=3, padx=5, pady=5)
        Button(self.simplexQuizFrame, text="New Question", command=lambda: self.newQuestion("Simplex"), bg="#1b263b", fg="white",
               font=fontMedium, width=20).grid(row=9, column=9, columnspan=3, padx=5, pady=5)
        # plot on graph:
        self.colours = ["#606c38", "#b2675e", "#eca400"]
        
        self.fig, self.ax = plt.subplots(figsize=(4,4))
        for constraint in self.quizConstraints:
            a, b, c = constraint
            #print(a, b, c)
            i = self.quizConstraints.index(constraint)
            xVals = np.linspace(0, 10, 200) # used to plot constriant lines on graph
            if b != 0: # is a line in the form ax + by = c
                yVals = (c - a*xVals) / b
            else: # in the form ax = c
                xVals = np.full_like(xVals, c / a)
                yVals = np.linspace(0, 10, 200)
            self.ax.plot(xVals, yVals, label=f"Constraint {i+1}", color=self.colours[i])
        
        self.ax.set_xlim(0,10)
        self.ax.set_ylim(0,10)
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend()
        self.ax.grid()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.simplexQuizFrame)
        self.canvas.get_tk_widget().grid(row=4, column=0, rowspan=5, columnspan=6)
        self.canvas.draw()
        
        
        
    def bubbleSortDataset(self):
        # 10 random integers between 1 and 50 inclusive
        #print("in create bubbleSort dataset")
        self.quizNumbers = []
        for i in range(10):
            number = randint(1, 50)
            self.quizNumbers.append(number)
        
        
    def randomGraph(self):
        # connected graph of 6-8 vertices labelled A, B, C...
        # weights between 1 and 50
        #print("in create random graph")
        numVertices = randint(6,8)
        vertices = [chr(65+i) for i in range(numVertices)]
        edges = []
        startVertex = vertices[0]
        visited = set([startVertex])
        queue = []
        
        # alll edges from start vertex to queue
        for v in vertices:
            if v != startVertex:
                weight = randint(1,50)
                heapq.heappush(queue, (weight, startVertex, v))
        
        while queue:
            weight, u, v = heapq.heappop(queue)
            # has been visited - add to MST
            if v not in visited:
                visited.add(v)
                edges.append((u, v, weight))
                for w in vertices:
                    if w != v and w not in visited:
                        weight = randint(1,50)
                        heapq.heappush(queue, (weight, v, w))
            if len(visited) == numVertices:
                break
        
        # add random extra edges:
        extraEdges = randint(4, 10)
        allPossEdges = [(u,v) for u in vertices for v in vertices if u<v]
        shuffle(allPossEdges)
        totalEdges = extraEdges + len(edges)
        for u, v in allPossEdges:
            if len(edges) >= totalEdges:
                break
            if (u,v) not in edges and (v,u) not in edges:
                weight = randint(1,50)
                edges.append((u,v,weight))
        
        #print(f"Vertices generated: {vertices}")
        #print(f"Edges generated: {edges}")
        self.quizGraph = nx.Graph()
        self.quizGraph.add_weighted_edges_from(edges)
        #print(f"self.graph nodes: {self.graph.nodes}")
        #print(f"self.graph edges: {self.graph.edges}")
        
        self.endVertex = vertices[-1] # this is needed for dijkstra's
        
    def simplexConstraints(self):
        # 3 constraints and objective function
        # integers coefficients between -10 and 10, x and y not both 0
        #print("in create simplex constraints")
        while True:
            self.quizConstraints = []
            while len(self.quizConstraints) < 3:
                xCoef = randint(-10, 10)
                yCoef = randint(-10, 10)
                rhs = randint(0, 10)
                if yCoef !=0 or xCoef != 0: # allows for one to be 0 using or
                    self.quizConstraints.append([float(xCoef), float(yCoef), float(rhs)])
            
            self.quizObjective = []
            while len(self.quizObjective) < 1:
                xCoef = randint(0, 10)
                yCoef = randint(0, 10)
                if yCoef != 0 or xCoef != 0: # allows for one to be 0 using or
                    self.quizObjective.append(float(xCoef))
                    self.quizObjective.append(float(yCoef))
            
            
            # check if feasible:
            self.simplex.valueConstraints = self.quizConstraints[:]
            self.simplex.valueObjective = self.quizObjective[:]
            #print(f"simplex valueConstraints: {self.simplex.valueConstraints}")
            #print(f"simplex valueObjective: {self.simplex.valueObjective}")
            
            self.simplex.createTableau()
            self.simplex.simplexSteps()
            '''print("steps:")
            for step in self.simplex.steps:
                print(step)'''            
            #print(f"state of invalid: {self.simplex.invalid}")
            if self.simplex.invalid == False:
                break
            else:
                #print("Generated infeasible problem")
                self.simplex.steps = [(0,0,0)]
                self.simplex.tableau = np.array([], dtype=float) # empty numpy array'''
                self.simplex.valueConstraints = []
                self.simplex.valueObjective = []
        correctX, correctY, correctP = self.simplex.steps[-1]
        #print(f"correct: x={correctX}, y={correctY}, P={correctP}")
        
    def check(self):
        # calls updateScore
        #print("in check")
        if self.currentQType == "Bubble Sort":
            self.bubbleSort.numbers = self.quizNumbers[:] # copy
            self.bubbleSort.bubbleSortSteps()
            correctOrder = list(self.bubbleSort.steps[-1]) # final sorted order
            correctPasses = self.bubbleSort.numberPasses
            
            userOrder = [var.get() for var in self.numChoices]
            try:
                userPasses = int(self.passesInput.get())
            except ValueError:
                userPasses = -1
            
            if userOrder == correctOrder and userPasses == correctPasses:
                self.answerText["text"] = "Correct :)"
                self.answerText["fg"] = "#008000"
                self.updateScore("Correct")
            elif userOrder != correctOrder:
                self.answerText["text"] = "Incorrect order\nTry a new question"
                self.answerText["fg"] = "#990000"
                self.updateScore("Incorrect")
            else: # passes wrong
                self.answerText["text"] = f"Incorrect number of passes. Correct answer: {correctPasses}.\nTry a new question"
                self.answerText["fg"] = "#990000"
                self.updateScore("Incorrect")
        
        
        elif self.currentQType == "Prim's":
            self.prim.graph = self.quizGraph.copy()
            #self.prim.startVertexChoice = "A"
            self.prim.primSteps(start="A")
            # edges in alphabetical roder AB instead of BA:
            correctMST = set(tuple(sorted(edge)) for edge in self.prim.steps[-1]) 
            correctWeight = sum(self.quizGraph[u][v]["weight"] for u,v in correctMST)
            
            #print(f"Correct MST: {correctMST}")
            #print(f"Correct weight: {correctWeight}")
            # remove spaces, split by commas
            userMSTInput = self.mstEntry.get().replace(" ", "").split(",")
            userMST = set()
            for edge in userMSTInput:
                if len(edge) == 2:
                    userMST.add(tuple(sorted(edge))) # store as sorted tuple - AB same as BA
            try:
                userWeight = int(self.weightEntry.get())
            except ValueError:
                userWeight = -1 # invalid input
            
            #print(f"User MST: {userMST}")
            #print(f"User weight: {userWeight}")
            # check correctness:
            if userMST == correctMST and userWeight == correctWeight:
                self.answerText["text"] = "Correct :)"
                self.answerText["fg"] = "#008000"
                self.updateScore("Correct")
            elif userMST != correctMST:
                self.answerText["text"] = "Incorrect MST edges\nTry a new question"
                self.answerText["fg"] = "#990000"
                self.updateScore("Incorrect")
            else:
                self.answerText["text"] = f"Incorrect MST weight. Correct answer: {correctWeight}"
                self.answerText["fg"] = "#990000"
                self.updateScore("Incorrect")
            
            
            
        elif self.currentQType == "Dijkstra's":
            self.dijkstra.graph = self.quizGraph.copy()
            self.dijkstra.dijkstraSteps(startV="A", endV=self.endVertex)
            correctPath = "".join(self.dijkstra.steps[-1][1]) # last tuple, 2nd part
            correctWeight = self.dijkstra.distances[self.endVertex]
            
            userPath = self.shortestPathEntry.get().strip().upper()
            try:
                userWeight = int(self.weightEntry.get())
            except ValueError:
                userWeight = -1
            
            # check correctness:
            if userPath == correctPath and userWeight == correctWeight:
                self.answerText["text"] = "Correct :)"
                self.answerText["fg"] = "#008000"
                self.updateScore("Correct")
            elif userPath != correctPath:
                self.answerText["text"] = "Incorrect path\nTry a new question"
                self.answerText["fg"] = "#990000"
                self.updateScore("Incorrect")
            else:
                self.answerText["text"] = f"Incorrect path weight. Correct answer: {correctWeight}"
                self.answerText["fg"] = "#990000"
                self.updateScore("Incorrect")
            
        
        elif self.currentQType == "Simplex":
            correctX = Fraction(self.simplex.steps[-1][0]).limit_denominator()
            correctY = Fraction(self.simplex.steps[-1][1]).limit_denominator()
            correctP = Fraction(self.simplex.steps[-1][2]).limit_denominator()
            
            #correctX, correctY, correctP = self.simplex.steps[-1]
            #print(f"correct: x={correctX}, y={correctY}, P={correctP}")
            try:
                userX = Fraction(self.xInput.get())
                userY = Fraction(self.yInput.get())
                userP = Fraction(self.pInput.get())
            except ValueError:
                self.answerText["text"] = "Please enter numbers of fractions (e.g. 3/5)"
                self.answerText["fg"] = "#990000"
                return
            
            if userX == correctX and userY == correctY and userP == correctP:
                self.answerText["text"] = "Correct :)"
                self.answerText["fg"] = "#008000"
                self.updateScore("Correct")
            else:
                self.answerText["text"] = "Incorrect\nTry a new question."
                self.answerText["fg"] = "#990000"
                self.updateScore("Incorrect")
            
            
        
        
    def newQuestion(self, qType):
        # forget current widgets, create new ones.for qType
        #print(f"in new question for: {qType}")
        if qType == "Bubble Sort":
            self.bubbleSortDataset()
            # reset text labels:
            for label, number in zip(self.numLabels, self.quizNumbers):
                label.config(text=str(number))
            # reset dropdowns:
            for var, dropdown in zip(self.numChoices, self.dropdowns):
                var.set(0)
                dropdown["menu"].delete(0, "end")
                for num in self.quizNumbers:
                    dropdown["menu"].add_command(label=num, command=lambda value=num, var=var: var.set(value))
            # clear text box:
            self.passesInput.set("")
            self.answerText["text"] = ""
            self.bubbleSort.numberPasses = 0
            
            
        elif qType == "Prim's":
            self.randomGraph()
            
            self.ax.clear()
            pos = nx.spring_layout(self.quizGraph)
            nx.draw(self.quizGraph, pos, with_labels=True, node_color='#606c38', edge_color='black',
                    node_size=200, font_color='white', font_size=11, ax=self.ax)
            edge_labels = nx.get_edge_attributes(self.quizGraph, 'weight')
            nx.draw_networkx_edge_labels(self.quizGraph, pos, edge_labels=edge_labels, ax=self.ax)
            self.primQuizGraphCanvas.draw()
            
            self.mstEntry.set("")
            self.weightEntry.set(0)
            self.answerText["text"] = ""
            
            
        elif qType == "Dijkstra's":
            self.randomGraph()
            
            self.ax.clear()
            pos = nx.spring_layout(self.quizGraph)
            nx.draw(self.quizGraph, pos, with_labels=True, node_color='#606c38', edge_color='black',
                    node_size=200, font_color='white', font_size=11, ax=self.ax)
            edge_labels = nx.get_edge_attributes(self.quizGraph, 'weight')
            nx.draw_networkx_edge_labels(self.quizGraph, pos, edge_labels=edge_labels, ax=self.ax)
            self.dijkstraQuizGraphCanvas.draw()
            
            self.shortestPathEntry.set("")
            self.weightEntry.set(0)
            self.answerText["text"] = ""
            
            # add code to update the text saying the end vertex
            self.startEndText["text"] = f"Start at vertex A. End vertex {self.endVertex}.\nInput the shortest path in the form 'ABC...':"
            
            
        elif qType == "Simplex":
            self.simplexConstraints()
            self.answerText["text"] = ""
            
            self.constriantsTexts = [ f"{a}x + {b}y ≤ {c}" for a,b,c in self.quizConstraints]
            self.objectiveText = f"P = {self.quizObjective[0]}x + {self.quizObjective[1]}y"
            self.textSayingConstraints["text"] = "Please enter either integers or fractions (e.g. in the form 3/5)\n" + "Constraints:\n" + "\n".join(self.constraintTexts) + "\n" + "Objective: " + self.objectiveText
            
            self.xInput.set("")
            self.yInput.set("")
            self.pInput.set("")
            
            self.ax.clear()
            for constraint in self.quizConstraints:
                a, b, c = constraint
                #print(a, b, c)
                i = self.quizConstraints.index(constraint)
                xVals = np.linspace(0, 10, 200) # used to plot constriant lines on graph
                if b != 0: # is a line in the form ax + by = c
                    yVals = (c - a*xVals) / b
                else: # in the form ax = c
                    xVals = np.full_like(xVals, c / a)
                    yVals = np.linspace(0, 10, 200)
                self.ax.plot(xVals, yVals, label=f"Constraint {i+1}", color=self.colours[i])
        
            self.ax.set_xlim(0,10)
            self.ax.set_ylim(0,10)
            self.ax.axhline(0, color="black", linewidth=1)
            self.ax.axvline(0, color="black", linewidth=1)
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.legend()
            self.ax.grid()
            
            self.canvas.draw()
            self.answerText["text"] = ""
            




    def newType(self, newQType):
        # qType = question type ---> bubble Sort, prim, dijkstra, simplex
        # forget currentQType ---> None initially
        #print(f"current question type: {self.currentQType}, new question type: {newQType}")
        self.imageLabel.grid_forget()
        
        # change current button colour to blue, forget current question widgets
        if self.currentQType == "Bubble Sort":
            self.bubbleSortButton["bg"] = "#1b263b"
            for widget in self.bubbleSortQuizFrame.winfo_children():
                widget.grid_forget()
                    
        elif self.currentQType == "Prim's":
            self.primButton["bg"] = "#1b263b"
            for widget in self.primQuizFrame.winfo_children():
                widget.grid_forget()
            
        elif self.currentQType == "Dijkstra's":
            self.dijkstraButton["bg"] = "#1b263b"
            for widget in self.dijkstraQuizFrame.winfo_children():
                widget.grid_forget()
            
        elif self.currentQType == "Simplex":
            self.simplexButton["bg"] = "#1b263b"
            for widget in self.simplexQuizFrame.winfo_children():
                widget.grid_forget()
                
        # new question widgets:
        if newQType == "Bubble Sort":
            self.currentQType = "Bubble Sort"
            self.bubbleSortDataset()
            self.bubbleSortQuizWidgets()
            self.master.geometry("880x440")
            
        elif newQType == "Prim's":
            self.currentQType = "Prim's"
            self.randomGraph()
            self.primQuizWidgets()
            self.master.geometry("880x650")
            
        elif newQType == "Dijkstra's":
            self.currentQType = "Dijkstra's"
            self.randomGraph()
            self.dijkstraQuizWidgets()
            self.master.geometry("880x795")
            
        elif newQType == "Simplex":
            self.currentQType = "Simplex"
            self.simplexConstraints()
            self.simplexQuizWidgets()
            self.master.geometry("965x795")
        
    def updateScore(self, answer):
        # answer = Correct or Incorrect
        #print("in update score")
        usernameHolder = self.username
        algorithmHolder = self.currentQType
        if answer == "Correct":
            self.cursor.execute("UPDATE StudentEnrolment SET CorrectScore = CorrectScore+1 WHERE Username = ? AND Algorithm=?;", (usernameHolder, algorithmHolder))
            self.conn.commit()
        elif answer == "Incorrect":
            self.cursor.execute("UPDATE StudentEnrolment SET IncorrectScore = IncorrectScore+1 WHERE Username = ? AND Algorithm=?;", (usernameHolder, algorithmHolder))
            self.conn.commit()
        #print("score updated")
       
       
    def accountAlgorithms(self):
        try:
            usernameHolder = self.username
            self.cursor.execute("SELECT Algorithm FROM StudentEnrolment WHERE Username=?;", (usernameHolder,))
            result = self.cursor.fetchall()
            #print(f"sql result: {result}")
            algorithmsList = [row[0] for row in result]
            #print(f"algorithms list: {algorithmsList}")
            return algorithmsList
        except sqlite3.Error as e:
            print(f"Database error: {e}")
       
    def openHome(self):
        closeOpen(self.master, "home", self.username)

# fro testing ------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quiz test")
    #root.geometry("800x595")
    graph_input = Quiz(root, "HelloWord!!!") #HellowWord!!! username for testing purposes
    root.mainloop()
