from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pyodbc
import hashlib
import sys

class AddPlayerDialog(QDialog):
    def __init__(self, team_id, connection_string):
        super(AddPlayerDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Add_Player_dlg.ui', self)

        self.connection_string = connection_string # Locally store connection string
        self.team_id = team_id

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT country_code, category FROM Teams WHERE team_id = ?", (self.team_id))
        self.country_code, self.category = cursor.fetchone()
        connection.close()

        self.Error_Label.hide()
        self.populatePlayers()
        self.New_Player_Button.clicked.connect(self.new_player)
        self.Add_to_Team_Button.clicked.connect(self.validate)

    def populatePlayers(self):
        # Connect to db
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        
        cursor.execute("SELECT P.player_id, P.player_name, P.age, P.gender, P.role FROM Players P INNER JOIN Teams T ON P.country_code = T.country_code WHERE (CASE WHEN P.Gender = 'M' AND T.Category = 'Mens' THEN 1 WHEN P.Gender = 'F' AND T.Category = 'Womens' THEN 1 ELSE 0 END) = 1 AND T.team_id = ? AND P.player_id NOT IN (SELECT player_id FROM Plays_FOR WHERE team_id = ?)", (self.team_id, self.team_id))

        self.Player_Table.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.Player_Table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.Player_Table.setItem(row_index, col_index, item)

        connection.close()

    def new_player(self):
        dlg = NewPlayerDialog(self.country_code, self.category, self.connection_string)
        if dlg.exec():
            self.populatePlayers()
    
    def validate(self):
        selected_row = -1
        if not len(self.Player_Table.selectedIndexes()): # If no record selected then do nothing
            self.Error_Label.show()
        else:
            selected_row = self.Player_Table.currentRow()
            player_id = self.Player_Table.item(selected_row, 0).text()
            player_name = self.Player_Table.item(selected_row, 1).text()
        
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()

            # add player to team
            cursor.execute("INSERT INTO Plays_For (player_id, team_id) VALUES (?, ?)", (player_id, self.team_id))
            cursor.commit()

            # get roll no
            cursor.execute("SELECT MAX(roll_no) FROM Plays_For") 
            roll_no = cursor.fetchone()[0]
            # print(team_id)

            # get team name
            cursor.execute("SELECT Username FROM Power_Users WHERE team_id = ?", (self.team_id))
            team_name = cursor.fetchone()[0]

            QtWidgets.QMessageBox.information(self, "Player Inserted", f"Player : {player_name} added to team: {team_name} with roll no: {roll_no}.")

            connection.close()
            self.accept()


class NewPlayerDialog(QDialog):
    def __init__(self, country_code, category, connection_string):
        super(NewPlayerDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('New_Player_dlg.ui', self)
        self.country_code = country_code
        self.gender = 'M' if category[0] == 'M' else 'F'

        self.connection_string = connection_string # store connection string locally

        self.Add_Player_Button.clicked.connect(self.add_player)

    def add_player(self):
        player_name = self.Name_Entry.text()
        player_age = int(self.Age_Entry.text())
        player_role = self.Role_ComboBox.currentText()

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Players (player_name, country_code, age, gender, role) VALUES (?, ?, ?, ?, ?)", (player_name, self.country_code, player_age, self.gender, player_role))
        cursor.commit()

        # Show a message box with the order ID
        QtWidgets.QMessageBox.information(
            self, "Player Added", f"Player Name: {player_name} has been inserted successfully.")

        connection.close()
        self.accept()