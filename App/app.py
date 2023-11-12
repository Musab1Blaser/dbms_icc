from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pyodbc
import sys

from Add_Team_Functionality import AddTeamDialog, AddCountryDialog

class LogOutDialog(QDialog):
    def __init__(self):
        super(LogOutDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Log_Out_Screen.ui', self)

class LogInDialog(QDialog):
    def __init__(self):
        super(LogInDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Login_Screen.ui', self)
        self.status = 0
        self.Error_Label.hide()
        self.Login_Button.clicked.connect(self.validate)

    def validate(self):
        if self.Username_Entry.text() == "pak" and self.Password_Entry.text() == "abc123":
            self.status = 1 # country manager
            self.accept()
        elif self.Username_Entry.text() == "icc" and self.Password_Entry.text() == "icc123":
            self.status = 2 # icc manager
            self.accept()
        else:
            # invalid details
            self.Error_Label.show()
            self.Username_Entry.setText("")
            self.Password_Entry.setText("")
        

class UI(QMainWindow):
    def __init__(self, connection_string):
        # Call the inherited classes __init__ method
        super(UI, self).__init__() 
        # Load the .ui file
        uic.loadUi('Main_App.ui', self)

        self.connection_string = connection_string # store connection string locally

        self.status = 0 #User role 0 -> guest, 1 -> country manager, 2 -> icc manager

        self.Menu_Pages_Widget.setCurrentIndex(0)
        self.Menu_Buttons = [self.Teams_Button, self.Players_Button, self.Match_History_Button, self.Scheduled_Fixtures_Button, self.Pending_Matches_Button, self.Add_Team_Button, self.Add_Player_Button]
        self.Menu_Buttons[-1].hide()
        self.Menu_Buttons[-2].hide()
        self.Menu_Buttons[-3].hide()
        self.Log_Out_Button.hide()

        self.Menu_Pages = [self.Teams_Page, self.Players_Page, self.Match_History_Page, self.Scheduled_Fixtures_Page, self.Pending_Matches_Page]

        # Connect each menu button to its corresponding page
        self.Menu_Buttons[0].clicked.connect(lambda: self.Menu_Pages_Widget.setCurrentIndex(0))
        self.Menu_Buttons[1].clicked.connect(lambda: self.Menu_Pages_Widget.setCurrentIndex(1))
        self.Menu_Buttons[2].clicked.connect(lambda: self.Menu_Pages_Widget.setCurrentIndex(2))
        self.Menu_Buttons[3].clicked.connect(lambda: self.Menu_Pages_Widget.setCurrentIndex(3))
        self.Menu_Buttons[4].clicked.connect(lambda: self.Menu_Pages_Widget.setCurrentIndex(4))

        # connect log in and log out buttons to their respective dialogs
        self.Log_In_Button.clicked.connect(self.login_attempt)
        self.Log_Out_Button.clicked.connect(self.logout_attempt)

        # connect add team button
        self.Add_Team_Button.clicked.connect(self.add_team)

    def login_attempt(self): # manages the change in option visibility between users
        dlg = LogInDialog()
        if dlg.exec():
            if dlg.status == 1:
                self.status = dlg.status
                print("Logged in as Country Manager")
                self.Logged_in_as_Label.setText("PAK_M_ODI_Manager")
                self.Pending_Matches_Remove_Match_Button.hide()
                self.Pending_Matches_Add_Match_Button.hide()
                self.Pending_Matches_Respond_Button.show()
                self.Menu_Buttons[-3].show()
                self.Menu_Buttons[-2].hide()
                self.Menu_Buttons[-1].show()
                self.Log_In_Button.hide()
                self.Log_Out_Button.show()
            if dlg.status == 2:
                self.status = dlg.status
                print("Logged in as ICC Manager")
                self.Logged_in_as_Label.setText("ICC_Manager")
                self.Pending_Matches_Remove_Match_Button.show()
                self.Pending_Matches_Add_Match_Button.show()
                self.Pending_Matches_Respond_Button.hide()
                self.Menu_Buttons[-3].show()
                self.Menu_Buttons[-2].show()
                self.Menu_Buttons[-1].hide()
                self.Log_In_Button.hide()
                self.Log_Out_Button.show()

    def logout_attempt(self):  # manages the change in option visibility between users
        dlg = LogOutDialog()
        if dlg.exec():
            self.status = 0
            self.Menu_Pages_Widget.setCurrentIndex(0)
            self.Menu_Buttons[-1].hide()
            self.Menu_Buttons[-2].hide()
            self.Menu_Buttons[-3].hide()
            self.Log_Out_Button.hide()
            self.Log_In_Button.show()
            self.Logged_in_as_Label.setText("GUEST")

    def add_team(self):
        dlg = AddTeamDialog(self.connection_string)
        dlg.exec()

server = "LAPTOP-D5M397KF\DBMS_LAB6"
database = "ICC_Cricket_Management"
username = "sa"
password = "password123"
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = UI(connection_string) # Create an instance of our window
window.show()
app.exec() # Start the application