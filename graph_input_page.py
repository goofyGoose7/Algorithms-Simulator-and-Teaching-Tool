from tkinter import *
import tkinter as tk
from tkinter import simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from NEA_utilities import fontLarge, fontMedium, fontSmall


class GraphInput:
    def __init__(self, master):
        self.master = master
        self.graph = nx.Graph()
        self.validated = False
        self.selected_vertex = None
        #self.target_vertex = None
        self.selected_edge = None
        
        
    def graphInputPageWidgets(self):
        #self.graphInputFrame = Frame(self.master, bg="#eaebed")
        self.master.configure(bg="#eaebed")
        self.master.geometry("1200x815")
        
        
        Label(self.master, text="Input a Graph", font=fontLarge, bg="#eaebed", fg="#1b263b").grid(row=0, column=0, columnspan=10)
        
        Label(self.master,
              text="  • Double click on the canvas to add a vertex. Enter a unique identifier.\n"
                   "  • Click once on one vertex and once on another vertex to create an edge between them. Enter a weight greater than 0.\n"
                   "  • Click on an element once and press delete to remove it.\n"
                   " When you are happy with your graph, check that it has 4-10 vertices, each with at least 1 edge connected to it. Then press submit",
              font = fontMedium,
              fg="#1b263b",
              bg="#eaebed",
              justify="left").grid(row=1, column=0, columnspan=10, sticky="w")
        
        Label(self.master, text="Canvas:", font=fontMedium, bg="#eaebed").grid(row=2, column=0, columnspan=2)
        Label(self.master, text="Graph:", font=fontMedium, bg="#eaebed").grid(row=2, column=5, columnspan=2)
        
        self.canvasFrame = Frame(self.master, bg="#eaebed")
        self.canvasFrame.grid(row=3, column=0)
        
        self.canvas = Canvas(self.canvasFrame, width=600, height=600, bg="white")
        self.canvas.grid(row=3, column=0, columnspan=5, rowspan=5)
        
        self.fig, self.ax = plt.subplots(figsize=(5,5))
        self.graphCanvas = FigureCanvasTkAgg(self.fig, self.master)
        self.graphCanvas.get_tk_widget().grid(row=3, column=5, columnspan=5, rowspan=5)
        
        self.invalidMessage = Label(self.master, text="", font=fontMedium, bg="#eaebed", fg="#990000")
        self.invalidMessage.grid(row=8, column=0, columnspan=8)
        
        Button(self.master, text="Submit", font=fontMedium, fg="white", bg="#1b263b", command=self.validateGraph).grid(row=8, column=8, columnspan=2)
        
        self.canvas.focus_set()
        # set up the keyboard/user clicks/inputs:
        self.canvas.bind("<Double-Button-1>", self.add_vertex)
        self.canvas.bind("<Button-1>", self.select_or_create_edge)
        self.canvas.bind("<Delete>", self.delete_element)


    def validateGraph(self):
        #print("in validate graph")
        # check for 4 to 10 vertices:
        if len(self.graph.nodes) < 4 or len(self.graph.nodes) > 10:
            self.invalidMessage["text"] = "Invalid graph: Ensure that the graph has between 4 and 10 vertices."
            self.validated = False
            return
        
        # check each vertex has at least 1 edge to it
        for vertex in self.graph.nodes:
            if len(list(self.graph.neighbors(vertex))) == 0:
                self.invalidMessage["text"] = "Invalid graph: Ensure that each vertex has at least 1 edge connected to it."
                self.validated = False
                return
        
        # check weight edges greater than 0
        for start, end, data in self.graph.edges(data=True):
            if data.get("weight", 0) <= 0:
                self.invalidMessage["text"] = "Invalid graph: Ensure that the weight of each edge is greater than 0."
                self.validated = False
                return
        
        # check connected:
        if not nx.is_connected(self.graph):
            self.invalidMessage["text"] = "Invalid graph: Ensure that the graph is fully connected."
            self.validated = False
            return
        
        self.invalidMessage["text"] = " "
        self.validated = True
        self.backToPage()
        
    def backToPage(self):
        if self.validated == True:
            self.graphInputHideWidgets()
            if hasattr(self, "primWidgets"):
                self.primWidgets()
                self.primExtraWidgets()
            elif hasattr(self, "dijkstraWidgets"):
                self.dijkstraWidgets()
                self.dijkstraExtraWidgets()
        

    def add_vertex(self, event):
        #print("in add vertex")
        if len(self.graph.nodes) < 10:
            vertex_id = simpledialog.askstring("Vertex Input", "Enter a unique vertex identifier (1 character):")
            if vertex_id and len(vertex_id) == 1 and vertex_id not in self.graph.nodes and vertex_id != '"':
                x, y = event.x, event.y
                self.graph.add_node(vertex_id, pos=(x, y))
                
                self.canvas.create_oval(x-10, y-10, x+10, y+10, fill='blue', outline='black')
                self.canvas.create_text(x, y, text=vertex_id, fill='white')
                
                #print(f"Added vertex: {vertex_id} at position ({x}, {y})")
                self.update_visualization()
                

    def select_or_create_edge(self, event):
        #print("in select or create edge")
        for node, (x, y) in nx.get_node_attributes(self.graph, 'pos').items():
            if abs(event.x - x) < 10 and abs(event.y - y) < 10:
                if self.selected_vertex is None:
                    self.selected_vertex = node
                    #print(f"selected vertex: {node}")
                elif self.selected_vertex != node:
                    self.target_vertex = node
                    weight = simpledialog.askinteger("Edge Weight", "Enter a positive integer weight:")
                    if weight and weight > 0:
                        self.graph.add_edge(self.selected_vertex, self.target_vertex, weight=weight)
                        # Draw the edge visually on the canvas
                        self.canvas.create_line(
                            self.graph.nodes[self.selected_vertex]['pos'][0], 
                            self.graph.nodes[self.selected_vertex]['pos'][1],
                            self.graph.nodes[self.target_vertex]['pos'][0],
                            self.graph.nodes[self.target_vertex]['pos'][1],
                            fill="black", width=2, tags=(self.selected_vertex, self.target_vertex)
                        )
                        #print(f"Created edge between {self.selected_vertex} and {self.target_vertex} with weight {weight}")
                        self.update_visualization()
                    self.selected_vertex = None
                    self.target_vertex = None
                return
        # Check if the click is on an edge
        for edge in self.graph.edges:
            x1, y1 = self.graph.nodes[edge[0]]['pos']
            x2, y2 = self.graph.nodes[edge[1]]['pos']
            if min(x1, x2) <= event.x <= max(x1, x2) and min(y1, y2) <= event.y <= max(y1, y2):
                self.selected_edge = edge
                #print(f"Selected edge: {self.selected_edge} for deletion")
                return
        
        self.selected_vertex = None
        self.target_vertex = None

    def delete_element(self, event):
        #print("in delete element")
        if self.selected_vertex is not None:
            #print(f"Selected vertex: {self.selected_vertex} for deletion")
            for node, (x, y) in nx.get_node_attributes(self.graph, 'pos').items():
                #print("in for")
                #print(f"node to delete: {node}")
                #print(f"node position : {(x,y)}")
                #print(f"event position: ({event.x},{event.y})")
                #print(f"Difference: ({abs(event.x - x)},{abs(event.y - y)})")
                if abs(event.x - x) < 500 and abs(event.y - y) < 500:
                    #print("in if")
                    self.graph.remove_node(node)
                    # Remove the vertex from the canvas
                    self.canvas.delete(node)
                    
                    #print(f"Deleted vertex: {node}")
                    self.update_visualization()
                    self.selected_vertex = None
                    return
        if self.selected_edge is not None:
            #print(f"Selected edge: {self.selected_edge} for deletion")
            for edge in list(self.graph.edges):
                x1, y1 = self.graph.nodes[edge[0]]['pos']
                x2, y2 = self.graph.nodes[edge[1]]['pos']
                
                if min(x1, x2) <= event.x <= max(x1, x2) and min(y1, y2) <= event.y <= max(y1, y2):
                    self.graph.remove_edge(*self.selected_edge)
                    # Remove the edge from the canvas
                    edge_tag = self.selected_edge
                    self.canvas.delete(edge_tag)
                    #self.canvas.delete(edge)
                    #print(f"Deleted edge between {edge[0]} and {edge[1]}")
                    self.update_visualization()
                    self.selected_edge = None
                    return

    def update_visualization(self):
        #print("in update visualisation")
        self.ax.clear()
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, with_labels=True, node_color='#606c38', edge_color='black', node_size=500, font_color='white', ax=self.ax)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=self.ax)
        self.graphCanvas.draw()
        self.redraw_canvas()
        
        
    def redraw_canvas(self):
        #print("Redrawing canvas...")
        self.canvas.delete("all")  # Clear the canvas
        
        # Redraw vertices
        for node, (x, y) in nx.get_node_attributes(self.graph, 'pos').items():
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="#606c38", outline='black', tags=node)
            self.canvas.create_text(x, y, text=node, fill='white', tags=node)
        
        # Redraw edges
        for edge in self.graph.edges:
            x1, y1 = self.graph.nodes[edge[0]]['pos']
            x2, y2 = self.graph.nodes[edge[1]]['pos']
            edge_tag = (edge[0], edge[1])
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2, tags=edge_tag)
          
    
    def graphInputHideWidgets(self):
        for widget in self.master.winfo_children():
            widget.grid_forget()