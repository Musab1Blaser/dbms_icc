from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pyodbc
import hashlib
import sys

from Add_Team_Functionality import AddTeamDialog
from Add_Player_Functionality import AddPlayerDialog

class LogOutDialog(QDialog):
    def __init__(self):
        super(LogOutDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Log_Out_Screen.ui', self)

class LogInDialog(QDialog):
    def __init__(self, connection_string):
        super(LogInDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Login_Screen.ui', self)
        self.connection_string = connection_string
        self.status = 0
        self.username = ""
        self.Error_Label.hide()
        self.Login_Button.clicked.connect(self.validate)

    def validate(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        uname = self.Username_Entry.text()
        pwd = self.Password_Entry.text()
        enc_pwd = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
 
        # check uname and pwd
        cursor.execute("SELECT username, team_id FROM Power_Users WHERE username = ? AND encrypted_password = ?", (uname, enc_pwd))
        result = cursor.fetchone()
        connection.close()

        # login to respective account
        if result and not result[1]:
            self.status = 0 # icc manager
            self.accept()
        elif result and result[1]:
            self.status = int(result[1]) # country manager
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

        self.status = -1 #User role -1 -> guest, 0 -> icc manager, 1.. -> team_id

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

        # Update tables
        self.populate_teams_table()
        self.populate_players_table()

        # connect log in and log out buttons to their respective dialogs
        self.Log_In_Button.clicked.connect(self.login_attempt)
        self.Log_Out_Button.clicked.connect(self.logout_attempt)

        # connect add team button
        self.Add_Team_Button.clicked.connect(self.add_team)
        self.Add_Player_Button.clicked.connect(self.add_player)

    def login_attempt(self): # manages the change in option visibility between users
        dlg = LogInDialog(connection_string)
        if dlg.exec():
            if dlg.status == 0:
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
            else:
                self.status = dlg.status
                print("Logged in as Country Manager")
                connection = pyodbc.connect(self.connection_string)
                cursor = connection.cursor()
                cursor.execute("SELECT username FROM Power_Users WHERE team_id = ?", (self.status))
                result = cursor.fetchone()[0].strip()
                self.Logged_in_as_Label.setText(result)
                self.Pending_Matches_Remove_Match_Button.hide()
                self.Pending_Matches_Add_Match_Button.hide()
                self.Pending_Matches_Respond_Button.show()
                self.Menu_Buttons[-3].show()
                self.Menu_Buttons[-2].hide()
                self.Menu_Buttons[-1].show()
                self.Log_In_Button.hide()
                self.Log_Out_Button.show()

    def logout_attempt(self):  # manages the change in option visibility between users
        dlg = LogOutDialog()
        if dlg.exec():
            self.status = -1
            self.Menu_Pages_Widget.setCurrentIndex(0)
            self.Menu_Buttons[-1].hide()
            self.Menu_Buttons[-2].hide()
            self.Menu_Buttons[-3].hide()
            self.Log_Out_Button.hide()
            self.Log_In_Button.show()
            self.Logged_in_as_Label.setText("GUEST")

    def populate_teams_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("select * from Teams")

        self.Teams_Ranking_Table.setRowCount(0)

        result = cursor.fetchall()

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(result):
            self.Teams_Ranking_Table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                if (col_index == 1):
                    cell_data = str(cell_data)
                    tmp = cursor.execute("SELECT country_name FROM Countries WHERE country_code = ?", (cell_data))
                    cell_data = tmp.fetchone()[0]
                item = QTableWidgetItem(str(cell_data))
                self.Teams_Ranking_Table.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()

    def populate_players_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("select * from Players")

        self.Players_Ranking_Table.setRowCount(0)

        result = cursor.fetchall()

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(result):
            self.Players_Ranking_Table.insertRow(row_index)
            offset = 0
            country = ""
            for col_index, cell_data in enumerate(row_data):
                if (col_index == 2):
                    cell_data = str(cell_data)
                    tmp = cursor.execute("SELECT country_name FROM Countries WHERE country_code = ?", (cell_data))
                    cell_data = tmp.fetchone()[0]

                item = QTableWidgetItem(str(cell_data))
                self.Players_Ranking_Table.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()


    def add_team(self):
        dlg = AddTeamDialog(self.connection_string)
        if dlg.exec():
            self.populate_teams_table()

    def add_player(self):
        dlg = AddPlayerDialog(self.status, self.connection_string)
        if dlg.exec():
            self.populate_players_table()



server = "LAPTOP-D5M397KF\DBMS_LAB6"
database = "ICC_Cricket_Management"
username = "sa"
password = "password123"
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = UI(connection_string) # Create an instance of our window
window.show()
app.exec() # Start the application