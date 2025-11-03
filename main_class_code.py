# imports specific to the Main class
import sqlite3

class Main:
    def __init__(self, master):
        self.master = master # this is the window
        self.title = None
        # database connection:
        self.conn = sqlite3.connect("AlgorithmTeachingToolDB.db") # actual database
        self.cursor = self.conn.cursor() # for selecting
    
    def closeConn (self):
        self.conn.close()