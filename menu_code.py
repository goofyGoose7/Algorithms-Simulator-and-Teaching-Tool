# imports specific to the Menu class
from tkinter import *
import tkinter as tk
from NEA_utilities import fontLarge, fontMedium, fontSmall


class Menu:
    def __init__(self, master, rowCoord, columnsLength):
        self.rowStart = rowCoord # this is the y coordinate of where the menu starts for the current page
        self.menuLength = columnsLength # this is the rowspan of the menu based on the current page
        self.menuFrame = None
        
        self.master = master
        self.currentStep = 0
        self.isPaused = False
        
    def menuWidgets(self):
        #print("in menuWidgets")
        
        self.menuFrame = Frame(self.master, bg="#1b263b")
        #self.menuFrame.grid(row=self.rowStart, column = 0, columnspan = self.menuLength, rowspan=3)
        self.menuFrame.grid(row=self.rowStart, column=0, columnspan=self.menuLength, rowspan=3, sticky="ew")
        
        Button(self.menuFrame, text="Skip Back", command=self.skipBack, fg="#1b263b", bg="#eaebed",
               font=fontMedium, width=15).grid(row=1, column= 1, padx=10, pady=10)
        self.playPauseButton = Button(self.menuFrame, text="Pause", command=self.togglePlayPause,
                                      fg="#1b263b", bg="#eaebed", font=fontMedium, width=15)
        self.playPauseButton.grid(row=1, column=3, padx=5, pady=5)
        Button(self.menuFrame, text="Skip Forward", command=self.skipForward, bg="#eaebed",
               fg="#1b263b", font=fontMedium, width=15).grid(row=1, column=5, padx=10, pady=10)
        # add text describing arrow stuff
        self.menuText = Label(self.menuFrame, text="Use right/left arrow keys to step forward/back through the visualisation when paused.",
                              font=fontSmall, fg="#eaebed", bg="#1b263b")
        self.menuText.grid(row=1, column=7, columnspan=12, padx=5)   
        
        # these are for the keyboard inputs:
        self.master.bind("<Left>", lambda e: self.stepBack())
        self.master.bind("<Right>", lambda e: self.stepForward())
    
    def skipBack(self):
        self.currentStep = 0
        self.isPaused = True
        
        if hasattr(self, "updateChart"): # note that methods count as attributes
            self.updateChart(self.steps[self.currentStep])
            
        elif hasattr(self, "updatePrimGraph"):
            self.updatePrimGraph(self.steps[self.currentStep])
            
        elif hasattr(self, "updateDijkstraGraph"):
            print("in dijkstra skip back")
            step = self.steps[self.currentStep]
            visitedNodes, currentNode, checkingEdges = step[0], step[1], step[2]
            self.updateDijkstraGraph(visitedNodes, currentNode, checkingEdges)
            self.updateDijkstraTable(step)
            
        elif hasattr(self, "updateSimplexGraph"):
            self.updateSimplexGraph()
        
        self.invalidMessage["text"] = ""
        
    def skipForward(self):
        self.currentStep = len(self.steps) - 1 # gets the last step index
        self.isPaused = True
        if hasattr(self, "updateChart"): # note that methods count as attributes
            self.updateChart(self.steps[self.currentStep])
            
        elif hasattr(self, "updatePrimGraph"):
            self.updatePrimGraph(self.steps[self.currentStep])
            
        elif hasattr(self, "updateDijkstraGraph"):
            print("in dijkstra skip forward")
            step = self.steps[self.currentStep]
            pathEdges = [(step[1][i], step[1][i+1]) for i in range(len(step[1]) -1)]
            self.updateDijkstraGraph([], checkingEdges=pathEdges)
            shortestPathText = " -> ".join(step[1])
            self.invalidMessage["text"] = f'''Shortest path between {self.startVertexChoice.get()} and {self.endVertexChoice.get()}
is {shortestPathText} \nWeight: {self.distances[self.endVertexChoice.get()]}'''
            step1 = self.steps[self.currentStep-1] # so that the vertex table is actually filled in
            self.updateDijkstraTable(step1)
            
        elif hasattr(self, "updateSimplexGraph"):
            self.updateSimplexGraph()
            self.invalidMessage["text"] = f"Optimal solution P = {self.steps[-1][2]}\nx = {self.steps[-1][0]}, y = {self.steps[-1][1]}"

        
    def togglePlayPause(self):
        print("in toggle play pause")
        self.isPaused = not self.isPaused # switches the state
        self.playPauseButton.config(text="Pause" if not self.isPaused else "Play") # switches the text
        if not self.isPaused: # ie displays Pause but the visualisation is playing
            print("in not self.isPaused")
            #self.playAnimation()
            if hasattr(self, "bubbleSortAnimate"):
                self.bubbleSortAnimate()
                
            elif hasattr(self, "primAnimate"):
                self.primAnimate()
                
            elif hasattr(self, "dijkstraAnimate"):
                #print("in dijkstra toggle play pause")
                self.dijkstraAnimate()
                
            elif hasattr(self, "simplexAnimate"):
                self.simplexAnimate()
                
            
    def stepBack(self):
        if self.isPaused and self.currentStep > 0:
            self.currentStep -= 1
            if hasattr(self, "updateChart"): # note that methods count as attributes
                numbers = self.steps[self.currentStep]
                indices = self.stepsDictionary[numbers]
                self.updateChart(numbers, indices)
                
            elif hasattr(self, "updatePrimGraph"):
                mstStep = self.steps[self.currentStep]
                self.updatePrimGraph(mstStep)
                self.visualiseText.insert(tk.END, "MST:" + " ".join([f"{u}{v}," for u,v in mstStep]) + "\n") 
                self.visualiseText.see(tk.END)
                
            elif hasattr(self, "updateDijkstraGraph"):
                print("in dijkstra step back")
                step = self.steps[self.currentStep]
                if isinstance(step[0], set): # check not shortest path
                    visitedNodes, currentNode, checkingEdges = step[0], step[1], step[2]
                    self.updateDijkstraGraph(visitedNodes, currentNode, checkingEdges)
                    self.updateDijkstraTable(step)
            
            elif hasattr(self, "updateSimplexGraph"):
                self.updateSimplexGraph()
                self.invalidMessage["text"] = ""
     
     
    def stepForward(self):
        if self.isPaused and self.currentStep < len(self.steps)-1:
            self.currentStep += 1
            if hasattr(self, "updateChart"): # note that method count as attributes
                numbers = self.steps[self.currentStep]
                indices = self.stepsDictionary[numbers]
                self.updateChart(numbers, indices)
            
            elif hasattr(self, "updatePrimGraph"):
                mstStep = self.steps[self.currentStep]
                self.updatePrimGraph(mstStep)
                self.visualiseText.insert(tk.END, "MST:" + " ".join([f"{u}{v}," for u,v in mstStep]) + "\n") 
                self.visualiseText.see(tk.END)
            
            elif hasattr(self, "updateDijkstraGraph"):
                print("in dijkstra step forward")
                step = self.steps[self.currentStep]
                if step[0] == "shortest path":
                    pathEdges = [(step[1][i], step[1][i+1]) for i in range(len(step[1]) -1)]
                    self.updateDijkstraGraph([], checkingEdges=pathEdges)
                    shortestPathText = " -> ".join(step[1])
                    self.invalidMessage["text"] = f'''Shortest path between {self.startVertexChoice.get()} and {self.endVertexChoice.get()}
is {shortestPathText} \nWeight: {self.distances[self.endVertexChoice.get()]}'''
                else:
                    visitedNodes, currentNode, checkingEdges = step[0], step[1], step[2]
                    self.updateDijkstraGraph(visitedNodes, currentNode, checkingEdges)
                    self.updateDijkstraTable(step)
                    
            elif hasattr(self, "updateSimplexGraph"):
                step = self.steps[self.currentStep]
                self.updateSimplexGraph()
                if step == self.steps[-1]:
                    self.invalidMessage["text"] = f"Optimal solution P = {self.steps[-1][2]}\nx = {self.steps[-1][0]}, y = {self.steps[-1][1]}"
                else:
                    self.invalidMessage["text"] = ""
            
    def hideMenuWidgets(self):
        for widget in self.menuFrame.winfo_children():
            widget.grid_forget()
        self.title.grid_forget()
        self.menuFrame.configure(bg="#eaebed")
