# NEA_main_file: file for starting the system by taking the user to the login page

# imports specific to the initial main class
from tkinter import *
import tkinter as tk
import sqlite3
from login_register_page import LoginRegister


conn1 = sqlite3.connect("AlgorithmTeachingToolDB.db")
#print("open successful")

conn1.execute('''CREATE TABLE IF NOT EXISTS Users
            (Username		TEXT	NOT NULL	PRIMARY KEY,
            Password		TEXT	NOT NULL,
            Account_type	TEXT	NOT NULL ) ;''')

conn1.execute('''CREATE TABLE IF NOT EXISTS StudentEnrolment
            (StudentEnrolID	 INTEGER	PRIMARY KEY	 AUTOINCREMENT,
            Username 		TEXT	NOT NULL,
            Algorithm		TEXT	NOT NULL,
            CorrectScore	INT		NOT NULL,
            IncorrectScore  INT 	NOT NULL,
            FOREIGN KEY (Username) REFERENCES Users(Username) ) ; ''')

conn1.execute('''CREATE TABLE IF NOT EXISTS TeacherEnrolment
            (TeacherEnrolID	 INTEGER	 PRIMARY KEY  AUTOINCREMENT,
            Username 	TEXT	NOT NULL,
            Algorithm	TEXT	NOT NULL,
            FOREIGN KEY (Username) REFERENCES Users(Username) ) ; ''')
conn1.commit()
conn1.close()



if __name__ == "__main__":
    loginRoot = tk.Tk()
    loginRoot.geometry('625x400')
    loginRoot.title("Algorithms Simulator & Teaching Tool")
    running1 = LoginRegister(loginRoot)
    loginRoot.mainloop()


        
    
