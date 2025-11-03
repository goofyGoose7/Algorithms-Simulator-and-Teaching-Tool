# NEA_utilities: file for closing one page and opening another, contains the fonts

# tkinter import:
from tkinter import *
import tkinter as tk


def closeOpen(root, newType, username=None):
    #print("in closeOpen")
    root.destroy()
    if newType == "home":
        try:
            from home_page import HomeMain
            homeRoot = Tk()
            homeRoot.geometry('1150x740') # to change
            homeRoot.title("Algorithms Simulator and Teaching Tool")
            running = HomeMain(homeRoot, username)
            homeRoot.mainloop()
        except ImportError as e:
            print(f"Failed import HomeMain: {e}")
            return
    
    elif newType == "login":
        try:
            from login_register_page import LoginRegister
            loginRoot = Tk()
            loginRoot.geometry('625x400')
            loginRoot.title("Algorithms Simulator & Teaching Tool")
            running = LoginRegister(loginRoot)
            loginRoot.mainloop()
        except ImportError as e:
            print(f"Failed import LoginRegister: {e}")
            return
        
    elif newType == "bubble sort":
        try:
            from bubble_sort_page import BubbleSort
            bubbleSortRoot = Tk()
            bubbleSortRoot.geometry('400x1000') # to change
            bubbleSortRoot.title("Algorithms Simulator and Teaching Tool")
            running = BubbleSort(bubbleSortRoot, username)
            bubbleSortRoot.mainloop()
        except ImportError as e:
            print(f"Failed import BubbleSort: {e}")
            return
        
    elif newType == "prim":
        try:
            from prim_page import Prim
            primRoot = Tk()
            primRoot.geometry('500x350') # to change
            primRoot.title("Algorithms Simulator and Teaching Tool")
            running = Prim(primRoot, username)
            primRoot.mainloop()
        except ImportError as e:
            print(f"Failed import Prim: {e}")
            return
        
    elif newType == "dijkstra":
        try:
            from dijkstra_page import Dijkstra
            dijkstraRoot = Tk()
            dijkstraRoot.geometry('500x350') # to change
            dijkstraRoot.title("Algorithms Simulator and Teaching Tool")
            running = Dijkstra(dijkstraRoot, username)
            dijkstraRoot.mainloop()
        except ImportError as e:
            print(f"Failed import Dijkstra: {e}")
            return
        
    elif newType == "simplex":
        try:
            from simplex_page import Simplex
            simplexRoot = Tk()
            simplexRoot.geometry('500x350') # to change
            simplexRoot.title("Algorithms Simulator and Teaching Tool")
            running = Simplex(simplexRoot, username)
            simplexRoot.mainloop()
        except ImportError as e:
            print(f"Failed import Simplex: {e}")
            return
        
    elif newType == "quiz":
        try:
            from quiz_page import Quiz
            quizRoot = Tk()
            quizRoot.geometry('500x350') # to change
            quizRoot.title("Algorithms Simulator and Teaching Tool")
            running = Quiz(quizRoot, username)
            quizRoot.mainloop()
        except ImportError as e:
            print(f"Failed import Quiz: {e}")
            return

# fonts:
fontLarge = ("Calibri", 16, "bold")
fontMedium = ("Calibri", 12)
fontSmall = ("Calibri", 10)




