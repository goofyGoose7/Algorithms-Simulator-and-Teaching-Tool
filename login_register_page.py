# imports required specific to the LoginRegister class
from tkinter import *
import tkinter as tk
import sqlite3
import string
from main_class_code import Main
from NEA_utilities import closeOpen, fontLarge, fontMedium, fontSmall


class LoginRegister(Main):
    def __init__(self, master):
        super().__init__(master) # inherits all attribtues of Main class
        
        # login frame variables
        self.loginFrame = None
        self.username = StringVar()
        self.password = StringVar()
        self.loginInvalid = None
        
        # register frame variables
        self.regFrame = None
        self.newUsername = StringVar()
        self.newPassword = StringVar()
        self.newConfirmPassword = StringVar()
        
        # invalid message variables
        self.usernameInvalid = None
        self.passwordInvalid = None
        self.passwordsMatchInvalid = None
        self.invalidMessageReg = None
        
        # algorithm selection variables - 1 is onvalue, 0 is offvalue
        self.bubbleSortSelect = IntVar()
        self.primSelect = IntVar()
        self.dijkstraSelect = IntVar()
        self.simplexSelect = IntVar()
        self.algorithmsChosen = {"Bubble Sort": self.bubbleSortSelect,
                                 "Prim's": self.primSelect,
                                 "Dijkstra's": self.dijkstraSelect,
                                 "Simplex": self.simplexSelect}
        self.accountType = StringVar() # account selection
        self.loginRegisterWidgets()
        self.master.configure(bg="#eaebed")
    
    def loginRegisterWidgets(self):
        self.title = Label(self.master, text="Login", font=fontLarge, fg="#1b263b", bg="#eaebed")
        self.title.grid(row=0, column=0, columnspan=5)
        
        # login frame widgets
        self.loginFrame = Frame(self.master, bg="#eaebed")
        Label(self.loginFrame, text="Username:", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=2, column=0, columnspan=2)
        Label(self.loginFrame, text="Password:", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=3, column=0, columnspan=2)
        Entry(self.loginFrame, textvariable=self.username).grid(row=2, column=2, columnspan=3)
        Entry(self.loginFrame, textvariable=self.password, show="•").grid(row=3, column=2, columnspan=3)
        self.loginInvalid = Label(self.loginFrame, text="", font=fontSmall, fg="#990000", bg="#eaebed") # unsuccessful login text
        self.loginInvalid.grid(row=5, column=0, columnspan=5)
        Button(self.loginFrame, text="Login", command=self.loginCheck, activebackground="white", activeforeground="#1b263b",
               bg="#1b263b", fg="white", font=fontMedium, width=10).grid(row=6, column=1, padx=10, pady=5)
        Button(self.loginFrame, text="Register", command=self.newRegistrationPage, activebackground="white", activeforeground="#1b263b",
               bg="#1b263b", fg="white", font=fontMedium, width=10).grid(row=6, column=3, padx=10, pady=5)
        
        self.loginFrame.grid(row=1, column=0, columnspan=5) # first frame accessed 
        
        # register frame widgets
        self.regFrame = Frame(self.master, bg="#eaebed")
        Label(self.regFrame, text="Usernames should be unique. Passwords should have at least 8 characters,\nuppercase and lowercase letters and contain numbers and special characters.",
              font=fontSmall, fg="#1b263b", bg="#eaebed").grid(row=1, column=0, columnspan=6, pady=10)
        Label(self.regFrame, text="Username:", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=2, column=0, columnspan=2)
        Label(self.regFrame, text="Password:", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=3, column=0, columnspan=2)
        Label(self.regFrame, text="Password confirmation:", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=4, column=0, columnspan=2, padx=10)
        Label(self.regFrame, text="Select algorithms\nto study:", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=5, column=0, columnspan=2)
        Label(self.regFrame, text="Select account type:", font=fontMedium, fg="#1b263b", bg="#eaebed").grid(row=7, column=0, columnspan=2)
        # entry fields:
        Entry(self.regFrame, textvariable=self.newUsername).grid(row=2, column=2, columnspan=2)
        Entry(self.regFrame, textvariable=self.newPassword, show="•").grid(row=3, column=2, columnspan=2)
        Entry(self.regFrame, textvariable=self.newConfirmPassword, show="•").grid(row=4, column=2, columnspan=2)
        # invalid messages:
        self.usernameInvalid = Label(self.regFrame, text="", font=fontSmall, fg="#990000", bg="#eaebed")
        self.usernameInvalid.grid(row=2, column=4, columnspan=2)
        self.passwordInvalid = Label(self.regFrame, text="", font=fontSmall, fg="#990000", bg="#eaebed")
        self.passwordInvalid.grid(row=3, column=4, columnspan=2)
        self.passwordsMatchInvalid = Label(self.regFrame, text="", font=fontSmall, fg="#990000", bg="#eaebed")
        self.passwordsMatchInvalid.grid(row=4, column=4, columnspan=2)
        self.invalidMessageReg = Label(self.regFrame, text="", font=fontSmall, fg="#990000", bg="#eaebed")
        self.invalidMessageReg.grid(row=8, column=0, columnspan=4)
        # algorithm checkboxes:
        Checkbutton(self.regFrame, text="Bubble Sort", variable=self.bubbleSortSelect, onvalue=1, offvalue=0,
                    font=fontSmall, fg="#1b263b", bg="#eaebed").grid(row=5, column=2, columnspan=2)
        Checkbutton(self.regFrame, text="Prim's Algorithm", variable=self.primSelect, onvalue=1, offvalue=0,
                    font=fontSmall, fg="#1b263b", bg="#eaebed").grid(row=5, column=4, columnspan=2)
        Checkbutton(self.regFrame, text="Dijkstra's Algorithm", variable=self.dijkstraSelect, onvalue=1, offvalue=0,
                    font=fontSmall, fg="#1b263b", bg="#eaebed").grid(row=6, column=2, columnspan=2)
        Checkbutton(self.regFrame, text="Simplex Algorithm", variable=self.simplexSelect, onvalue=1, offvalue=0, font=fontSmall, fg="#1b263b", bg="#eaebed").grid(row=6, column=4, columnspan=2)
        # account selection radiobutton:
        Radiobutton(self.regFrame, text="Student", variable=self.accountType, value="Student", font=fontSmall, fg="#1b263b", bg="#eaebed").grid(row=7, column=2, columnspan=2)
        Radiobutton(self.regFrame, text="Teacher", variable=self.accountType, value="Teacher", font=fontSmall, fg="#1b263b", bg="#eaebed").grid(row=7, column=4, columnspan=2)
        # buttons
        Button(self.regFrame, text="Register", command=self.registerCheck, activebackground="white", activeforeground="#1b263b",
               bg="#1b263b", fg="white", font=fontMedium, width=10).grid(row=8, column=4, padx=10, pady=5)
        Button(self.regFrame, text="Back to Login", command=self.newLoginPage, activebackground="white", activeforeground="#1b263b",
               bg="#1b263b", fg="white", font=fontMedium, width=10).grid(row=8, column=5, padx=10, pady=5)
        
    def loginCheck(self):
        # if pass - go to closeLoginOpenHome
        #print("in login check")
        usernameHolder = self.username.get()
        if self.validateLoginInput(): # is True
            #print("login validated")
            # clear input fields:
            self.loginInvalid["text"] = ""
            self.username.set("")
            self.password.set("")
            # open home page:
            closeOpen(self.master, "home", usernameHolder)
        #else:
            #print("login failed")
        
    
    def validateLoginInput(self):
        #print("in validate login input")
        username = self.username.get()
        password = self.password.get()
        # check for no username / password entered
        if not username or not password:
            self.loginInvalid["text"] = "Error: invalid username or password"#
            self.username.set("")
            self.password.set("")
            return False
        # select from database for entered username and password
        try:
            self.cursor.execute("SELECT * FROM Users WHERE Username = ? and Password = ?", (username, password))
            user = self.cursor.fetchone() # returns values or None
            if user: # not None
                #print("Login successful")
                return True
            else:
                #print("login unsuccessful: no values found")
                self.loginInvalid["text"] = "Error: invalid username or password"
                self.username.set("")
                self.password.set("")
                return False
        except sqlite3.Error as e:
            #print(f"Database error: {e}")
            self.loginInvalid["text"] = "Error: invalid username or password"
            self.username.set("")
            self.password.set("")
            return False


    def registerCheck(self):
        '''
        check username is unique - if not, self.usernameInvalid["text"] = "Username unavailable"
        check passwords match - if not, self.passwordsMatchInvalid["text"] = "Passwords do not match"
        check password valid - if not, self.passwordInvalid["text"] = "Password invalid"
        if pass - go to closeLoginOpenHome
        '''
        #print("in register check")
        usernameHolder = self.newUsername.get()
        passwordHolder = self.newPassword.get()
        confirmPasswordHolder = self.newConfirmPassword.get()
        accountHolder = self.accountType.get()
        valid = False
        
        if not usernameHolder or not passwordHolder or not confirmPasswordHolder:
            self.invalidMessageReg["text"] = "Unsuccessful registration\nCheck all fields have been filled in correctly"
            return
        else:
            self.invalidMessageReg["text"] = ""
        
        if not self.validateUsernameReg():
            self.usernameInvalid["text"] = "Username not available"
            self.newUsername.set("")
            return
        else:
            self.usernameInvalid["text"] = ""
        
        # validate password
        if not self.validatePasswordReg():
            self.passwordInvalid["text"] = "Password invalid"
            self.newPassword.set("")
            self.newConfirmPassword.set("")
            return
        else:
            self.passwordInvalid["text"] = ""
        
        if passwordHolder != confirmPasswordHolder:
            self.passwordsMatchInvalid["text"] = "Passwords do not match"
            self.newPassword.set("")
            self.newConfirmPassword.set("")
            return
        else:
            self.passwordsMatchInvalid["text"] = ""
        
        # validate algorithm choice
        algorithmValues = [var.get() for var in self.algorithmsChosen.values()]
        #print(algorithmValues)
        if not any(value == 1 for value in algorithmValues):
            self.invalidMessageReg["text"] = "Unsuccessful registration\nCheck all fields have been filled in correctly"
            #print("algorithms fails")
            return
        else:
            self.invalidMessageReg["text"] = ""
            
        # validate account type selection 
        if not accountHolder: # not None
            self.invalidMessageReg["text"] = "Unsuccessful registration\nCheck all fields have been filled in correctly"
            #print("account fails")
            return
        else:
            self.invalidMessageReg["text"] = ""
        
        # enter values into database
        try:
            self.cursor.execute("INSERT INTO Users (Username, Password, Account_type) VALUES (?, ?, ?)", (usernameHolder, passwordHolder, accountHolder))
            self.conn.commit()
            #print("inserted into Users")
            
            if accountHolder == "Student":
                for name, numValue in self.algorithmsChosen.items():
                    if numValue.get() == 1:
                        self.cursor.execute("INSERT INTO StudentEnrolment (Username, Algorithm, CorrectScore, IncorrectScore) VALUES (?, ?, ?, ?)", (usernameHolder, name, 0, 0))
                        self.conn.commit()
                #print("inserted into StudentEnrolment")
            
            elif accountHolder == "Teacher":
                for name, numValue in self.algorithmsChosen.items():
                    if numValue.get() == 1:
                        self.cursor.execute("INSERT INTO TeacherEnrolment (Username, Algorithm) VALUES (?, ?)", (usernameHolder, name))
                        self.conn.commit()
                 #print("inserted into TeacherEnrolment")
            
            #print("Registration successful")
            # clear inputs after successful registration:
            
            self.newUsername.set("")
            self.newPassword.set("")
            self.newConfirmPassword.set("")
            for value in self.algorithmsChosen.values():
                value.set(0)
            self.accountType.set("")
            self.usernameInvalid["text"] = ""
            self.passwordInvalid["text"] = ""
            self.passwordsMatchInvalid["text"] = ""
            self.invalidMessageReg["text"] = ""
            closeOpen(self.master, "home", usernameHolder)
        except sqlite3.Error as e:
            #print(f"Database error: {e}")
            self.invalidMessageReg["text"] = "Unsuccessful registration\nCheck all fields have been filled in correctly"
        
    
    def validateUsernameReg(self):
        #print("in validate username")
        usernameHolder = self.newUsername.get()
        self.cursor.execute("SELECT Username FROM Users WHERE Username = ?", (usernameHolder,)) # comma to make tuple
        usernameFound = self.cursor.fetchone()
        if usernameFound:
            return False
        else:
            return True
    
    def validatePasswordReg(self):
        #print("in valdiate password")
        passwordHolder = self.newPassword.get()
         # longer than 8 characters (inclusive)
        if len(passwordHolder) >= 8:
            # contains both uppercase and lowercase characters
            if any(character.isupper() for character in passwordHolder) == True and any(character.islower() for character in passwordHolder) == True:
                # contains special chars - held in string.punctuation
                if any(character in string.punctuation for character in passwordHolder) == True:
                    # contains number
                    if any(character.isdigit() for character in passwordHolder) == True:
                        return True # all tests passed
        return False # at least 1 test failed
                        
        
    def newRegistrationPage(self):
        self.title["text"] = "Create an account"
        self.newUsername.set("")
        self.newPassword.set("")
        self.newConfirmPassword.set("")
        for value in self.algorithmsChosen.values():
            value.set(0)
        self.accountType.set("")
        self.usernameInvalid["text"] = ""
        self.passwordInvalid["text"] = ""
        self.passwordsMatchInvalid["text"] = ""
        self.invalidMessageReg["text"] = ""
        print("in new registration page")
        self.loginFrame.grid_forget()
        self.regFrame.grid(row=1, column=0, columnspan=6)
        
        
    def newLoginPage(self):
        self.title["text"] = "Login"
        self.loginInvalid["text"] = ""
        self.username.set("")
        self.password.set("")
        print("in new login page")
        self.regFrame.grid_forget()
        self.loginFrame.grid(row=1, column=0, columnspan=6)


