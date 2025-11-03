# imports specific to the Dijkstra's page
from tkinter import *
import tkinter as tk
from NEA_utilities import closeOpen, fontLarge, fontMedium, fontSmall
from graph_input_page import GraphInput
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from menu_code import Menu
import heapq

class Dijkstra(GraphInput, Menu):
    def __init__(self, master, pUsername, show_menu=True):
        self.master = master
        #print("in prim __init__ 1")
        GraphInput.__init__(self, master)
        #print("in prim __init__ after GraphInput")
        Menu.__init__(self, master, 14, 16) 
        
        self.username = pUsername
        
        self.dijkstraWidgets()
        if show_menu:
            self.menuWidgets()
            self.menuText["text"] = "Use right/left arrow keys to step forward/back through\nthe visualisation when paused."
        
        
    def dijkstraWidgets(self):
        self.master.configure(bg="#eaebed")
        self.master.geometry("905x505")
        
        self.dijkstraFrame = Frame(self.master, bg="#eaebed")
        self.dijkstraFrame.grid(row=0, column=0, columnspan=16, rowspan=14)
        
        self.title = Label(self.dijkstraFrame, text="Dijkstra's Algorithm Visualisation", font=fontLarge, bg="#eaebed", fg="#1b263b")
        self.title.grid(row=0, column=0, columnspan=14)
        
        Button(self.dijkstraFrame, text="Home", command=self.openHome, bg="#1b263b", fg="white", font=fontMedium, width=15).grid(row=0, column=14, columnspan=2)
        
        Label(self.dijkstraFrame, text=
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
              justify="left").grid(row=1, column=0, rowspan=3, columnspan=16, sticky="w")
        
        Label(self.dijkstraFrame,
              text='''In order to input a graph, press the 'Input a graph' button, which will open the window to create the graph.
Then choose a\nstart vertex from the list and visualise Dijkstra's algorithm on the graph.\n''',
              font=fontSmall,
              fg="#1b263b",
              bg="#eaebed",
              justify="left").grid(row=4, column=0, rowspan=2, columnspan=16, sticky="w")
        
        self.graphInputButton = Button(self.dijkstraFrame, text="Input a graph", bg="#1b263b", fg="white", font=fontMedium, width=20, command=self.graphInputWindow)
        self.graphInputButton.grid(row=6, column=1, columnspan=2)
        
        # start vertex:
        Label(self.dijkstraFrame, text="Start vertex:", bg="#eaebed", fg="#1b263b", font=fontMedium).grid(row=12, column=0, columnspan=2)
        
        self.startVertexOptions = ["Select"] # initially Select - changes to the list of vertices once graph input
        self.startVertexChoice = StringVar(self.dijkstraFrame)
        self.startVertexChoice.set("Select")
        
        self.startVertexDropdown = OptionMenu(self.dijkstraFrame, self.startVertexChoice, *self.startVertexOptions)
        self.startVertexDropdown.grid(row=12, column=2, columnspan=2)
        self.startVertexDropdown.config(font=fontSmall, bg="#eaebed", fg="#1b263b")
        self.startVertexDropdown["menu"].config(font=fontSmall, bg="#eaebed", fg="#1b263b")
        
        #end vertex:
        Label(self.dijkstraFrame, text="End vertex:", bg="#eaebed", fg="#1b263b", font=fontMedium).grid(row=13, column=0, columnspan=2)
        
        self.endVertexOptions = ["Select"] # initially Select - changes to the list of vertices once graph input
        self.endVertexChoice = StringVar(self.dijkstraFrame)
        self.endVertexChoice.set("Select")
        
        self.endVertexDropdown = OptionMenu(self.dijkstraFrame, self.endVertexChoice, *self.endVertexOptions)
        self.endVertexDropdown.grid(row=13, column=2, columnspan=2)
        self.endVertexDropdown.config(font=fontSmall, bg="#eaebed", fg="#1b263b")
        self.endVertexDropdown["menu"].config(font=fontSmall, bg="#eaebed", fg="#1b263b")
        
        Button(self.dijkstraFrame, text="Visualise", command=self.validate, bg="#1b263b", fg="white", font=fontMedium, width=20).grid(row=12, column=5, columnspan=3, padx=10, pady=5)
        
        self.invalidMessage = Label(self.dijkstraFrame, text="", font=fontMedium, bg="#eaebed", fg="#990000")
        self.invalidMessage.grid(row=12, column=8, columnspan=8)


    def graphInputWindow(self):
        print("in start graph input window")
        self.hideDijkstraWidgets()
        self.hideMenuWidgets()
        self.graphInputPageWidgets()

    def hideDijkstraWidgets(self):
        print("in hide dijkstra widgets")
        for widget in self.dijkstraFrame.winfo_children():
            widget.grid_forget()
        self.title.grid_forget()
        
    def validate(self):
        print("in validate")
        # checks start and end vertex entered
        if self.startVertexChoice.get() == "Select": # select is default option where there is no vertex selected
            self.invalidMessage["text"] = "Invalid: please enter a start vertex."
            # start vertex not chosen
            #print("invalid start")
            return
        if self.endVertexChoice.get() == "Select":
            #print("invalid end")
            self.invalidMessage["text"] = "Invalid: please enter an end vertex."
            return
        if self.startVertexChoice.get() == self.endVertexChoice.get():
            #print("invalid same")
            self.invalidMessage["text"] = "Invalid: please enter a start and end vertex that are different."
            return
        #print("valid")
        self.invalidMessage["text"] = ""
        self.dijkstraSteps()
        self.dijkstraAnimate()
        
    def dijkstraExtraWidgets(self):
        print("in dijkstra extra widgets")
        self.master.geometry("905x880")
        
        self.menuWidgets()
        self.menuText["text"] = "Use right/left arrow keys to step forward/back through\nthe visualisation when paused."
        # destroy Graph Input button
        self.graphInputButton.destroy()
        
        # start vertex choices:
        self.startVertexOptions = list(self.graph.nodes)
        self.startVertexChoice.set(self.startVertexOptions[0] if self.startVertexOptions else "Select")
        self.startVertexDropdown["menu"].delete(0, "end")
        for vertex in self.startVertexOptions:
            self.startVertexDropdown["menu"].add_command(label=vertex, command=lambda v=vertex: self.startVertexChoice.set(v))
        
        # end vertex choices:
        self.endVertexOptions = list(self.graph.nodes)
        self.endVertexChoice.set(self.startVertexOptions[0] if self.startVertexOptions else "Select")
        self.endVertexDropdown["menu"].delete(0, "end")
        for vertex in self.endVertexOptions:
            self.endVertexDropdown["menu"].add_command(label=vertex, command=lambda v=vertex: self.endVertexChoice.set(v))
                
        
        # create axes to plot graph on
        self.fig, self.ax = plt.subplots(figsize=(3.5,3.5))
        self.dijkstraGraphCanvas = FigureCanvasTkAgg(self.fig, self.dijkstraFrame)
        self.dijkstraGraphCanvas.get_tk_widget().grid(row=6, column=0, rowspan=6, columnspan=6)
        # draw graph on axes
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True, node_color='#606c38', edge_color='black', node_size=500, font_color='white', ax=self.ax)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=self.ax)
        self.dijkstraGraphCanvas.draw()
        
        
        # create frame to hold the table
        self.tableFrame = Frame(self.dijkstraFrame, bg="#eaebed")
        self.tableFrame.grid(row=6, column=8, rowspan=6, columnspan=8)
        
        headers = ["Vertex", "Shortest Distance", "Previous Vertex", "Visited"]
        for column, text in enumerate(headers): # enumerate returns index and value
            label = Label(self.tableFrame, text=text, font=fontMedium, borderwidth=1, relief="solid", padx=5, pady=5)
            if text == "Vertex":
                label.grid(row=6, column=8, columnspan=2)
            else:
                label.grid(row=6, column=(8+(2*column)), sticky="nsew", columnspan=2)
        
        # fill in vertex values in distance table
        self.tableData = {}
        for row, vertex in enumerate(self.graph.nodes(), start=1):
            self.tableData[vertex] = {}
            # vertex name:
            vLabel = Label(self.tableFrame, text=vertex, font=fontMedium, borderwidth=1, relief="solid", padx=5, pady=5)
            vLabel.grid(row=(6+row), column=8, sticky="nsew", columnspan=2)
            self.tableData[vertex]["vertex"] = vLabel
            # shortest distance: initialise infinity except start:
            sdLabel = Label(self.tableFrame, text="∞", font=fontMedium, borderwidth=1, relief="solid", padx=5, pady=5)
            sdLabel.grid(row=(6+row), column=10, sticky="nsew", columnspan=2)
            self.tableData[vertex]["shortest distance"] = sdLabel
            # previous vertex: initialise to -
            pvLabel = Label(self.tableFrame, text="-", font=fontMedium, borderwidth=1, relief="solid", padx=5, pady=5)
            pvLabel.grid(row=(6+row), column=12, sticky="nsew", columnspan=2)
            self.tableData[vertex]["previous vertex"] = pvLabel
            # visited: iniitalise empty
            visitedLabel = Label(self.tableFrame, text="", font=fontMedium, borderwidth=1, relief="solid", padx=5, pady=5)
            visitedLabel.grid(row=(6+row), column=14, sticky="nsew", columnspan=2)
            self.tableData[vertex]["visited"] = visitedLabel
        
        
    def openHome(self):
        closeOpen(self.master, "home", self.username)
        
        
    def updateDijkstraGraph(self, visitedNodes, currentNode=None, checkingEdges=[]):
        print("in udpate dijkstra graph")
        self.ax.clear()
        pos = nx.get_node_attributes(self.graph, "pos")
        
        # draw base graph:
        nx.draw(self.graph, pos, with_labels=True, node_color='#606c38', edge_color='black', node_size=500, font_color='white', ax=self.ax)
        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=self.ax)
        
        # highlighted visited nodes:
        nx.draw_networkx_nodes(self.graph, pos, nodelist=visitedNodes, node_color="#eca400", ax=self.ax)
        
        # highlight current node:
        if currentNode:
            nx.draw_networkx_nodes(self.graph, pos, nodelist=[currentNode], node_color="#b2675e", ax=self.ax)
        
        # highlight edges being checked:
        nx.draw_networkx_edges(self.graph, pos, edgelist=checkingEdges, edge_color="#b2675e", width=2, ax=self.ax)
        
        self.dijkstraGraphCanvas.draw()
        
    def updateDijkstraTable(self, step):
        visitedNodes, currentNode, checkingEdges, distances, previous = step
        for vertex in self.graph.nodes():
            # update shortest distance:
            # if the vertex already has a shortest distance, change to that, otherwis infinity
            self.tableData[vertex]["shortest distance"]["text"] = (str(distances[vertex]) if distances[vertex] != float("inf") else "∞")
            # update previous vertex
            # if the vertex already has a previous vertex, change to that, otherwise -
            self.tableData[vertex]["previous vertex"]["text"] = (previous[vertex] if previous[vertex] else "-")
            # visited ndoes stay marked
            self.tableData[vertex]["visited"]["text"] = ("✓" if vertex in visitedNodes else "")

        
    def dijkstraSteps(self, startV=None, endV=None):
        print("in dijkstra steps")
        if startV:
            start = startV
        else:
            start = self.startVertexChoice.get()
        
        if endV:
            end = endV
        else:
            end = self.endVertexChoice.get()
        
        self.distances = {node: float("inf") for node in self.graph.nodes}
        self.previous = {node: None for node in self.graph.nodes}
        self.distances[start] = 0
        
        self.steps = []
        queue = [(0, start)] # this is a priority queue for storing (distance, vertex)
        visited = set()
        
        while queue:
            currentDistance, currentNode = heapq.heappop(queue)
            if currentNode in visited:
                # continue = go to process next vertex by going to the next iteration of while queue
                # this maintains Dijkstra's O((v+E)logV) complexity
                continue
            visited.add(currentNode)
            
            # store step for animation:
            checkingEdges = [(currentNode, neighbour) for neighbour in self.graph.neighbors(currentNode) if neighbour not in visited]
            self.steps.append((visited.copy(), currentNode, checkingEdges.copy(), dict(self.distances), dict(self.previous)))
            
            # check for shortest connected edge/node
            for neighbour in self.graph.neighbors(currentNode):
                if neighbour in visited:
                    continue
                edgeWeight = self.graph[currentNode][neighbour]["weight"]
                newDistance = currentDistance + edgeWeight
                if newDistance < self.distances[neighbour]:
                    self.distances[neighbour] = newDistance
                    self.previous[neighbour] = currentNode
                    heapq.heappush(queue, (newDistance, neighbour))
        
        # backtrack for shortest path:
        path = []
        current = end
        while current:
            path.append(current)
            current = self.previous[current]
        path.reverse()
        self.steps.append((("shortest path"), path))
        
        
    def dijkstraAnimate(self):
        print("in dijkstra animate")
        step = self.steps[self.currentStep]
        if not self.isPaused and step[0]=="shortest path":
            # step[1] contains the shortest path as a list of vertices
            # therefore adding the combos of edges into the list path_edges
            # e.g. if step[1] = [A, B, C] then path_edges = [(A,B), {B,C)]
            pathEdges = [(step[1][i], step[1][i+1]) for i in range(len(step[1]) -1)]
            self.updateDijkstraGraph([], checkingEdges=pathEdges)
            shortestPathText = " -> ".join(step[1])
            self.invalidMessage["text"] = f'''Shortest path between {self.startVertexChoice.get()} and
{self.endVertexChoice.get()} is {shortestPathText} \nWeight: {self.distances[self.endVertexChoice.get()]}'''
        
        elif not self.isPaused and self.currentStep < len(self.steps):
            visitedNodes, currentNode, checkingEdges = step[0], step[1], step[2]
            self.updateDijkstraGraph(visitedNodes, currentNode, checkingEdges)
            # update table
            self.updateDijkstraTable(step)
            self.currentStep += 1
            self.master.after(750, self.dijkstraAnimate)
        
# for testing ------------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dijkstra's test")
    #root.geometry("800x595")
    graph_input = Dijkstra(root, "HelloWord!!!") #HellowWord!!! username for testing purposes
    root.mainloop()
