from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pyodbc

class AddMatchResultsDialog(QDialog):
    def __init__(self, match_id, team_1_id, team_2_id, connection_string):
        super(AddMatchResultsDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Upload_Match_dlg.ui', self)


        self.connection_string = connection_string
        self.match_id = match_id
        self.team_1_id = team_1_id
        self.team_2_id = team_2_id

        self.team1_players = [self.Team1_Player01, self.Team1_Player02, self.Team1_Player03, self.Team1_Player04, self.Team1_Player05, self.Team1_Player06, self.Team1_Player07, self.Team1_Player08, self.Team1_Player09, self.Team1_Player10, self.Team1_Player11]
        self.team2_players = [self.Team2_Player01, self.Team2_Player02, self.Team2_Player03, self.Team2_Player04, self.Team2_Player05, self.Team2_Player06, self.Team2_Player07, self.Team2_Player08, self.Team2_Player09, self.Team2_Player10, self.Team2_Player11]

        self.team1_players_out = [self.Team1_Player01_Out, self.Team1_Player02_Out, self.Team1_Player03_Out, self.Team1_Player04_Out, self.Team1_Player05_Out, self.Team1_Player06_Out, self.Team1_Player07_Out, self.Team1_Player08_Out, self.Team1_Player09_Out, self.Team1_Player10_Out, self.Team1_Player11_Out]
        self.team2_players_out = [self.Team2_Player01_Out, self.Team2_Player02_Out, self.Team2_Player03_Out, self.Team2_Player04_Out, self.Team2_Player05_Out, self.Team2_Player06_Out, self.Team2_Player07_Out, self.Team2_Player08_Out, self.Team2_Player09_Out, self.Team2_Player10_Out, self.Team2_Player11_Out]

        self.flag = 0
        # self.count = 0
        for player in self.team1_players:
            player.currentIndexChanged.connect(self.update_comboboxes_team1)

        for player in self.team2_players:
            player.currentIndexChanged.connect(self.update_comboboxes_team2)

        self.Error_Label.hide()

        self.reset_comboboxes()

        self.Upload_Button.clicked.connect(self.upload)
        self.Cancel_Button.clicked.connect(self.close)
        # self.testing()

    def testing(self):
        for i in range(self.Team1_Player_Stats.rowCount()):
            for j in range(self.Team1_Player_Stats.columnCount()):
                item = QTableWidgetItem(str(1))
                self.Team1_Player_Stats.setItem(i, j, item)

        for i in range(self.Team2_Player_Stats.rowCount()):
            for j in range(self.Team2_Player_Stats.columnCount()):
                item = QTableWidgetItem(str(1))
                self.Team2_Player_Stats.setItem(i, j, item)

    def reset_comboboxes(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        # print(self.team_1_id)
        cursor.execute("SELECT PF.roll_no, P.player_name FROM Players P INNER JOIN Plays_For PF ON P.player_id = PF.player_id AND PF.team_id = ?", (self.team_1_id))
        self.team_1_player_list = [str(i[0]) + " - " + i[1] for i in cursor.fetchall()]
        # print(self.team_1_player_list)
        for idx, player in enumerate(self.team1_players):
            player.clear()
            player.addItem(f"Player {idx+1}")
            player.addItems(self.team_1_player_list)

        cursor.execute("SELECT PF.roll_no, P.player_name FROM Players P INNER JOIN Plays_For PF ON P.player_id = PF.player_id AND PF.team_id = ?", (self.team_2_id))
        self.team_2_player_list = [str(i[0]) + " - " + i[1] for i in cursor.fetchall()]

        for idx, player in enumerate(self.team2_players):
            player.clear()
            player.addItem(f"Player {idx+1}")
            player.addItems(self.team_2_player_list)

        connection.close()

    def update_comboboxes_team1(self):
        # print("yo")
        if self.flag:
            return
        self.flag = 1
        # self.count += 1
        # print(self.count)
        used_names = []
        for player in self.team1_players:
            if not player.currentText().startswith("Player"):
                used_names.append(player.currentText())

        remaining_names = [name for name in self.team_1_player_list if name not in used_names]
            
        for idx, player in enumerate(self.team1_players):
            tmp = player.currentText()
            player.clear()
            if not (tmp.startswith("Player")) and tmp:
                player.addItem(tmp)
            player.addItem(f"Player {idx+1}")
            player.addItems(remaining_names)

        self.flag = 0

    def update_comboboxes_team2(self):
        # print("yo")
        if self.flag:
            return
        self.flag = 1
        # self.count += 1
        # print(self.count)
        used_names = []
        for player in self.team2_players:
            if not player.currentText().startswith("Player"):
                used_names.append(player.currentText())

        remaining_names = [name for name in self.team_2_player_list if name not in used_names]
            
        for idx, player in enumerate(self.team2_players):
            tmp = player.currentText()
            player.clear()
            if not (tmp.startswith("Player")) and tmp:
                player.addItem(tmp)
            player.addItem(f"Player {idx+1}")
            player.addItems(remaining_names)

        self.flag = 0
        
    def upload(self):
        if not self.validate():
            return
        
        team_1_score = 0
        team_1_wickets = 0
        team_1_balls_played = 0

        team_2_score = 0
        team_2_wickets = 0
        team_2_balls_played = 0

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        try:
            for row, player in enumerate(self.team1_players):
                roll_no = player.currentText().split("-")[0].strip()
                print(roll_no)
                values = []
                for col in range(self.Team1_Player_Stats.columnCount()):
                    values.append(int(self.Team1_Player_Stats.item(row, col).text()))
                team_1_score += values[0]
                team_1_balls_played += values[1]
                
                wasOut = self.team1_players_out[row].isChecked()
                team_1_wickets += wasOut

                cursor.execute("INSERT INTO Player_Match_Stats (match_id, roll_no, bat_runs, bat_balls, bat_6s, bat_4s, balls_bowled, ball_wickets, ball_runs_conceded, bat_was_out) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (self.match_id, roll_no, *values, wasOut))
                print("inserted team 1 player:", row)

            for row, player in enumerate(self.team2_players):
                roll_no = player.currentText().split("-")[0].strip()
                print(roll_no)
                values = []
                for col in range(self.Team2_Player_Stats.columnCount()):
                    values.append(int(self.Team2_Player_Stats.item(row, col).text()))
                team_2_score += values[0]
                team_2_balls_played += values[1]
                
                wasOut = self.team2_players_out[row].isChecked()
                team_2_wickets += wasOut
                cursor.execute("INSERT INTO Player_Match_Stats (match_id, roll_no, bat_runs, bat_balls, bat_6s, bat_4s, balls_bowled, ball_wickets, ball_runs_conceded, bat_was_out) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (self.match_id, roll_no, *values, wasOut))
                print("inserted team 2 player:", row)
            
            cursor.execute("INSERT INTO Match_Results (match_id, team_1_score, team_1_wickets, team_1_balls_played, team_2_score, team_2_wickets, team_2_balls_played) VALUES (?, ?, ?, ?, ?, ?, ?);", (self.match_id, team_1_score, team_1_wickets, team_1_balls_played, team_2_score, team_2_wickets, team_2_balls_played))
            print("inserted overall match results:")

            cursor.execute("UPDATE Matches SET completed = 1 WHERE match_id = ?", (self.match_id))
            print("updated match status")

            cursor.commit()
            connection.close()
            QtWidgets.QMessageBox.information(self, "Insertion Successful", f"Match Results added successfully.")
            self.accept()
        except:
            cursor.rollback()
            connection.close()
            QtWidgets.QMessageBox.warning(self, "Insertion Failed", f"An error occured.")
            
        
    def validate(self):
        # return True
        for player in self.team1_players:
            if player.currentText().startswith("Player"):
                self.Error_Label.setText("Please specify all players")
                self.Error_Label.show()
                return False
        for player in self.team2_players:
            if player.currentText().startswith("Player"):
                self.Error_Label.setText("Please specify all players")
                self.Error_Label.show()
                return False
            
        for i in range(self.Team1_Player_Stats.rowCount()):
            for j in range(self.Team1_Player_Stats.columnCount()):
                item = self.Team1_Player_Stats.item(i, j)
                if not item:
                    self.Error_Label.setText("Please fill all required data with integer values")
                    self.Error_Label.show()
                    return

                cell_data = item.text()
                if not len(cell_data) or not cell_data.isnumeric():
                    self.Error_Label.setText("Please fill all required data with integer values")
                    self.Error_Label.show()
                    return
            
        for i in range(self.Team2_Player_Stats.rowCount()):
            for j in range(self.Team2_Player_Stats.columnCount()):
                item = self.Team2_Player_Stats.item(i, j)
                if not item:
                    self.Error_Label.setText("Please fill all required data with integer values")
                    self.Error_Label.show()
                    return
                
                cell_data = item.text()
                if not len(cell_data) or not cell_data.isnumeric():
                    self.Error_Label.setText("Please fill all required data with integer values")
                    self.Error_Label.show()
                    return

        return True

 

 # Musab's credentials
# server = "LAPTOP-D5M397KF\DBMS_LAB6"
# database = "ICC_Cricket_Management"
# username = "sa"
# password = "password123"
# connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'

# app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
# window = AddMatchResultsDialog(3, 5, 8, connection_string) # match_id, team1_id, team2_id
# window.show()
# app.exec() # Start the application