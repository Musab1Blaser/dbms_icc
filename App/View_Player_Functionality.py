from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pyodbc
from datetime import datetime
import sys

class ViewPlayerDialog(QDialog):
    def __init__(self, player_id, name, category, format, country, age, connection_string):
        super(ViewPlayerDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('View_Player_dlg.ui', self)

        self.connection_string = connection_string # Locally store connection string
        self.player_id = player_id
        self.name = name
        self.cat = category
        self.format = format
        self.age = age
        self.country = country
        # print("team id:", self.team_id)

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("SELECT PF.roll_no FROM Plays_For PF INNER JOIN Teams T ON PF.team_id = T.team_id INNER JOIN Countries C ON T.country_code = C.country_code WHERE T.category = ? AND T.format = ? AND C.country_name = ?", (self.cat, self.format, self.country))
        roll_no = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(bat_runs), SUM(bat_balls), SUM(bat_4s), SUM(bat_6s), SUM(balls_bowled), SUM(ball_wickets), SUM(ball_runs_conceded) FROM Player_Match_Stats WHERE roll_no = ?", (roll_no))

        print(roll_no)
        val_list = [player_id, name, category, format, country, age]
        tmp = cursor.fetchone()
        print(tmp)
        val_list.extend(tmp)

        self.Player_Stats_Table.setRowCount(0)
        self.Player_Stats_Table.insertRow(0)

        for col, val in enumerate(val_list):
            # print("val:",val)
            # if (val == str(self.team_id)):
                # self.team_num = col - 7
            if val is None:
                val = 0
            item = QTableWidgetItem(str(val))
            self.Player_Stats_Table.setItem(0, col, item)
        self.Player_Stats_Table.resizeColumnsToContents()
        self.Ok_Button.clicked.connect(self.close)