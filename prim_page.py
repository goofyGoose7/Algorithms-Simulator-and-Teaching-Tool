# imports specific to the Prim class
from tkinter import *
import tkinter as tk
from NEA_utilities import closeOpen, fontLarge, fontMedium, fontSmall
from graph_input_page import GraphInput
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import heapq # for a queue for prim's algorithm
from menu_code import Menu

class Prim(GraphInput, Menu): #HomeMain
    def __init__(self, master, pusername, show_menu=True):
        self.master = master
        #print("in prim __init__ 1")
        GraphInput.__init__(self, master)
        #print("in prim __init__ after GraphInput")
        Menu.__init__(self, master, 13, 12)
        #print("in prim__init__ after Menu")
        self.username = pusername
        self.primWidgets()
        if show_menu:
            self.menuWidgets()
            self.menuText["text"] = "Use right/left arrow keys to step forward/back\nthrough the visualisation when paused."
        
    def primWidgets(self):
        self.master.configure(bg="#eaebed")
        self.master.geometry("845x640")
        
        self.primFrame = Frame(self.master, bg="#eaebed")
        self.primFrame.grid(row=0, column=0, columnspan=12, rowspan=13)
        
        self.title = Label(self.primFrame, text="Prim's Algorithm Visualisation", fg="#1b263b", bg="#eaebed", font=fontLarge)
        self.title.grid(row=0, column=0, columnspan=10) # change columnspan
        
        Button(self.primFrame, text="Home", command=self.openHome, bg="#1b263b", fg="white", font=fontMedium, width=15).grid(row=0, column=10, columnspan=2)
         
        Label(self.primFrame,
              text= "1. Choose any vertex to start the tree.\n"
                    "2. Choose the edge of least weight that joins a vertex that is already in the tree to a vertex that is not yet in the tree.\n"
                    "3. Repeat step 2 until all the vertices are connected to the tree.",
              font=fontSmall,
              fg="#1b263b",
              bg="#eaebed",
              justify="left").grid(row=1, column=0, columnspan=12, rowspan=3, sticky="w", padx=10, pady=5)
        
        Label(self.primFrame,
              text="In order to input a graph, press the 'Input a graph' button, which will open the window to create the graph.\n"
                   "Then choose a start vertex from the list and visualise Prim's algorithm on the graph.",
              font=fontSmall,
              fg="#1b263b",
              bg="#eaebed",
              justify="left").grid(row=4, column=0, columnspan=12, rowspan=2, sticky="w", padx=10, pady=5)
        
        self.graphInputButton = Button(self.primFrame, text="Input a graph", bg="#1b263b", fg="white",
                                       font=fontMedium, width=20, command=self.graphInputWindow)
        self.graphInputButton.grid(row=6, column=1, columnspan=2)
        
        Label(self.primFrame, text="Start vertex:", bg="#eaebed", fg="#1b263b", font=fontMedium).grid(row=6, column=8, columnspan=2)
        
        Label(self.primFrame, text="MST edges:", bg="#eaebed", fg="#1b263b", font=fontMedium).grid(row=7, column=8, columnspan=4)
        self.visualiseText = Text(self.primFrame, width=30, height=16)
        self.visualiseText.grid(row=8, column=8, columnspan=4, rowspan=4, padx=5)
        
        Button(self.primFrame, text="Visualise", command=self.validate, bg="#1b263b", fg="white",
               font=fontMedium, width=20).grid(row=12, column=0, columnspan=3, padx=10, pady=5)
        
        self.invalidMessage = Label(self.primFrame, text="", font=fontMedium, bg="#eaebed", fg="#990000")
        self.invalidMessage.grid(row=12, column=3, columnspan=9)
        
        self.startVertexOptions = ["Select"] # initially Select - changes to the list of vertices once graph input
        self.startVertexChoice = StringVar(self.primFrame)
        self.startVertexChoice.set("Select")
        
        self.startVertexDropdown = OptionMenu(self.primFrame, self.startVertexChoice, *self.startVertexOptions)
        self.startVertexDropdown.grid(row=6, column=10, columnspan=2)
        self.startVertexDropdown.config(font=fontSmall, bg="#eaebed", fg="#1b263b")
        self.startVertexDropdown["menu"].config(font=fontSmall, bg="#eaebed", fg="#1b263b")
        
        
    def openHome(self):
        closeOpen(self.master, "home", self.username)
        
    def graphInputWindow(self):
        # open graph input window (but don't close current window
        #print("in graph input window method")
        # hide widgets on prim page
        self.hidePrimWidgets()
        # hide menu widgets
        self.hideMenuWidgets()
        # create graph page to open
        self.graphInputPageWidgets()
        
        
    def primExtraWidgets(self):
        # show menu widgets
        self.menuWidgets()
        self.menuText["text"] = "Use right/left arrow keys to step forward/back\nthrough the visualisation when paused." 
        
        # vertex dropdown menu
        self.startVertexOptions = list(self.graph.nodes)
        self.startVertexChoice.set(self.startVertexOptions[0] if self.startVertexOptions else "Select")
        self.startVertexDropdown["menu"].delete(0, "end")
        for vertex in self.startVertexOptions:
            self.startVertexDropdown["menu"].add_command(label=vertex, command=lambda v=vertex: self.startVertexChoice.set(v))
        
        # destroy button so axes can go there
        self.graphInputButton.destroy()
        # change size of window
        self.master.geometry("845x697")
        
        # create axes to plot graph on
        self.fig, self.ax = plt.subplots(figsize=(3.5,3.5))
        self.primGraphCanvas = FigureCanvasTkAgg(self.fig, self.primFrame)
        self.primGraphCanvas.get_tk_widget().grid(row=6, column=0, rowspan=6, columnspan=8)
        # draw graph on axes
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True, node_color='#606c38', edge_color='black', node_size=500, font_color='white', ax=self.ax)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=self.ax)
        self.primGraphCanvas.draw()
        
        
    def hidePrimWidgets(self):
        for widget in self.primFrame.winfo_children():
            widget.grid_forget()
        self.title.grid_forget()
        
    def validate(self):
        #print("in validate prim's")
        # note that graph has already been validated
        # checks that a start vertex has been input, then starts finding steps
        #print(f"start vertex: {self.startVertexChoice}")
        if self.startVertexChoice == "Select": # select is default option where there is no vertex selected
            #print("invalid")
            self.invalidMessage["text"] = "Invalid: please enter a start vertex."
            # start vertex not chosen
            return
        self.invalidMessage["text"] = ""
        self.primSteps()
        self.primAnimate()
        
        
    def updatePrimGraph(self, step):
        #print("in update graph")
        # will change colours of current vertex and joined edges
        self.ax.clear()
        pos = nx.get_node_attributes(self.graph, "pos")
        
        nx.draw(self.graph, pos, with_labels=True, node_color='#606c38', edge_color='black', node_size=500, font_color='white', ax=self.ax)
        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=self.ax)
        
        for u,v in step:
            colour = "#b2675e" if step == self.steps[-1] else "#606c38"
            nx.draw_networkx_edges(self.graph, pos, edgelist=[(u,v)], edge_color = colour, width=2, ax=self.ax)
        
        self.primGraphCanvas.draw()
        
        
    def primSteps(self, start=None):
        #print("in prim steps")
        
        self.steps = []
        self.mstEdges = []
        if start:
            startVertex = start
        else:
            startVertex = self.startVertexChoice.get()
        visited = set() # stores mst edges in an unordered, unchangeable and unindexed format
        minHeap = [] # this is the queue for the edges connected to the current vertex
        
        visited.add(startVertex)
        
        for neighbour, edgeData in self.graph[startVertex].items():
            weight = edgeData["weight"]
            # enqueue all connected nodes and edges onto minHeap
            heapq.heappush(minHeap, (weight, startVertex, neighbour)) 
        
        self.steps.append(tuple(self.mstEdges))
        
        while len(visited) < len(self.graph.nodes):
            if not minHeap: 
                self.invalidMessage["text"] = "The graph is not fully connected so there is no MST"
                return
            # heappop returns the smallest edge value element in minHeap
            weight, u, v = heapq.heappop(minHeap) 
            if v not in visited:
                visited.add(v)
                self.mstEdges.append((u,v))
                self.steps.append(tuple(self.mstEdges))
                for neighbour, edgeData in self.graph[v].items():
                    weight = edgeData["weight"]
                    if neighbour not in visited:
                        heapq.heappush(minHeap, (weight, v, neighbour))
        
        
        
    def primAnimate(self):
        # animates at start when not paused
        #print("in primAnimate")
        # test steps:
        if not self.steps:
            #print("Error: no steps recorded in self.steps")
            return
        
        if not self.isPaused and self.currentStep < len(self.steps):
            mstStep = self.steps[self.currentStep] # current step#s edges
            self.updatePrimGraph(mstStep)
            # show all edges currently in the mst in the Text section
            self.visualiseText.insert(tk.END, "MST:" + " ".join([f"{u}{v}," for u,v in mstStep]) + "\n") 
            self.visualiseText.see(tk.END)
            
            self.currentStep += 1
            self.master.after(750, self.primAnimate)
            
        elif not self.isPaused and self.currentStep == len(self.steps):
            mstStep = self.steps[self.currentStep - 1]
            print(mstStep)
            print(str(len(mstStep)))
            if len(mstStep) == len(self.graph)-1:
                self.updatePrimGraph(mstStep)
                self.invalidMessage["text"] = "MST found"
            else:
                self.invalidMessage["text"] = "The graph is not fully connected so there is no MST"

# for testing --------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Prim's test")
    #root.geometry("800x595")
    graph_input = Prim(root, "HelloWord!!!") #HellowWord!!! username for testing purposes
    root.mainloop()
        
        
        