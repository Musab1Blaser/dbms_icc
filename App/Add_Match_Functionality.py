from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pyodbc
from datetime import datetime
import sys

class AddMatchDialog(QDialog):
    def __init__(self, connection_string):
        super(AddMatchDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Add_Match_dlg.ui', self)

        self.connection_string = connection_string # Locally store connection string

        self.update_series()
        self.update_tournaments()

        # Connect Buttons
        self.Add_Series_Button.clicked.connect(self.add_series)
        self.Add_Tournament_Button.clicked.connect(self.add_tournament)
        self.Add_Match_Button.clicked.connect(self.add_match)

        # Disable Fields
        # Series
        self.Series_ComboBox.setEnabled(False)
        self.Add_Series_Button.setEnabled(False)

        #Tournament
        self.Tournament_ComboBox.setEnabled(False)
        self.Stage_ComboBox.setEnabled(False)
        self.Team_1_ComboBox.setEnabled(False)
        self.Team_2_ComboBox.setEnabled(False)
        self.Add_Tournament_Button.setEnabled(False)


        self.Series_RadioButton.clicked.connect(self.activate_series)
        self.Tournament_RadioButton.clicked.connect(self.activate_tournaments)

        self.Error_Label.hide()

        # Change Tournament
        self.Tournament_ComboBox.currentIndexChanged.connect(self.update_tournament_teams)

        # self.Error_Label.hide()
        # self.populateCountries()
        # self.Add_Country_Button.clicked.connect(self.add_country)
        # self.Add_Team_Button.clicked.connect(self.validate)

    def add_match(self):
        date_time = self.Date_Time_Entry.dateTime().toPyDateTime()
        date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
        venue = self.Venue_Entry.text()

        if not len(venue):
            self.Error_Label.show()
            self.Error_Label.setText("Please provide all details")
            return
    
        if self.Series_RadioButton.isChecked():
            series_name = self.Series_ComboBox.currentText()
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()

            cursor.execute("SELECT team_1_id, team_2_id FROM Series WHERE series_name = ?", (series_name))
            t1_id, t2_id = cursor.fetchone()

            cursor.execute("INSERT INTO Matches (date_time, venue, team_1_id, team_2_id) VALUES (?, ?, ?, ?)", (date_time, venue, t1_id, t2_id))
            cursor.commit()

            cursor.execute("SELECT TOP 1 match_id FROM Matches ORDER BY match_id DESC")
            match_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO Series_Matches (match_id, series_name) VALUES (?, ?)", (match_id, series_name))
            cursor.commit()

            QtWidgets.QMessageBox.information(
            self, "Match Added", "Match has been inserted successfully.")

            connection.close()
            self.accept()

        elif self.Tournament_RadioButton.isChecked():
            tournament_name = self.Tournament_ComboBox.currentText()
            tournament_stage = self.Stage_ComboBox.currentText()
            tournament_t1 = self.Team_1_ComboBox.currentText()
            tournament_t2 = self.Team_2_ComboBox.currentText()
            if tournament_t1 == tournament_t2:
                self.Error_Label.setText("The teams must be different")
                return
            
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()

            tournament_category, tournament_format = cursor.execute("SELECT category, format FROM Tournaments WHERE tournament_name = ?", (tournament_name)).fetchone()
            cursor.execute("SELECT T.team_id FROM Teams T INNER JOIN Countries C ON C.country_code = T.country_code WHERE C.country_name = ? AND T.category = ? AND T.format = ?", (tournament_t1, tournament_category, tournament_format))
            t1_id = cursor.fetchone()[0]
            cursor.execute("SELECT T.team_id FROM Teams T INNER JOIN Countries C ON C.country_code = T.country_code WHERE C.country_name = ? AND T.category = ? AND T.format = ?", (tournament_t2, tournament_category, tournament_format))
            t2_id = cursor.fetchone()[0]
            print(t1_id, t2_id)
            
            cursor.execute("INSERT INTO Matches (date_time, venue, team_1_id, team_2_id) VALUES (?, ?, ?, ?)", (date_time, venue, t1_id, t2_id))
            cursor.commit()

            cursor.execute("SELECT TOP 1 match_id FROM Matches ORDER BY match_id DESC")
            match_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO Tournament_Matches (match_id, tournament_name, tournament_stage) VALUES (?, ?, ?)", (match_id, tournament_name, tournament_stage))
            cursor.commit()

            QtWidgets.QMessageBox.information(
            self, "Match Added", "Match has been inserted successfully.")

            connection.close()
            self.accept()        
            
    def update_series(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT S.series_name FROM Series S WHERE S.total_matches > (SELECT COUNT(*) FROM Series_Matches X WHERE X.series_name = S.series_name)")
        self.Series_ComboBox.clear()
        for res in cursor.fetchall():
            self.Series_ComboBox.addItem(res[0])
        connection.close()
        
    def update_tournaments(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT tournament_name FROM Tournaments")
        self.Tournament_ComboBox.clear()
        for res in cursor.fetchall():
            self.Tournament_ComboBox.addItem(res[0])
        connection.close()
        self.update_tournament_teams()

    def update_tournament_teams(self):
        tournament_name = self.Tournament_ComboBox.currentText()
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT category, format FROM Tournaments WHERE tournament_name = ?", (tournament_name))
        tournament_category, tournament_format = cursor.fetchone()

        cursor.execute("SELECT C.country_name FROM Countries C INNER JOIN Teams T ON C.country_code = T.country_code AND T.category = ? and T.format = ?", (tournament_category, tournament_format))
        
        self.Team_1_ComboBox.clear()
        self.Team_2_ComboBox.clear()

        for item in cursor.fetchall():
            self.Team_1_ComboBox.addItem(item[0])
            self.Team_2_ComboBox.addItem(item[0])

    def activate_series(self):
        # Enable Series
        self.Series_ComboBox.setEnabled(True)
        self.Add_Series_Button.setEnabled(True)

        # Disable Tournament
        self.Tournament_ComboBox.setEnabled(False)
        self.Stage_ComboBox.setEnabled(False)
        self.Team_1_ComboBox.setEnabled(False)
        self.Team_2_ComboBox.setEnabled(False)
        self.Add_Tournament_Button.setEnabled(False)

    def activate_tournaments(self):
        # Disable Series
        self.Series_ComboBox.setEnabled(False)
        self.Add_Series_Button.setEnabled(False)

        # Enable Tournament
        self.Tournament_ComboBox.setEnabled(True)
        self.Stage_ComboBox.setEnabled(True)
        self.Team_1_ComboBox.setEnabled(True)
        self.Team_2_ComboBox.setEnabled(True)
        self.Add_Tournament_Button.setEnabled(True)

    def add_series(self):
        dlg = AddSeriesDialog(self.connection_string)
        if dlg.exec():
            self.update_series()

    def add_tournament(self):
        dlg = AddTournamentDialog(self.connection_string)
        if dlg.exec():
            self.update_tournaments()


class AddSeriesDialog(QDialog):
    def __init__(self, connection_string):
        super(AddSeriesDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Add_Series_dlg.ui', self)

        self.connection_string = connection_string # store connection string locally
        self.update_teams()

        self.Add_Series_Button.clicked.connect(self.add_series)
        self.Category_ComboBox.currentIndexChanged.connect(self.update_teams)
        self.Format_ComboBox.currentIndexChanged.connect(self.update_teams)

        self.Error_Label.hide()

    def add_series(self):
        series_name = self.Series_Entry.text()
        series_category = self.Category_ComboBox.currentText()
        series_format = self.Format_ComboBox.currentText()
        series_team_1 = self.Team_1_ComboBox.currentText()
        series_team_2 = self.Team_2_ComboBox.currentText()
        series_total_matches = self.Total_Matches_Entry.text()

        if not len(series_name) or not len(series_category) or not len(series_format) or not len(series_team_1) or not len(series_team_2) or not len(series_total_matches):
            self.Error_Label.setText("Please fill all fields")
            self.Error_Label.show()

        elif series_team_1 == series_team_2:
            self.Error_Label.setText("The teams must be different")
            self.Error_Label.show()

        elif not series_total_matches.isnumeric():
            self.Error_Label.setText("Matches must be a number")
            self.Error_Label.show()

        else:
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()
            cursor.execute("SELECT T.team_id FROM Teams T INNER JOIN Countries C ON T.country_code = C.country_code AND C.country_name = ? AND T.category = ? AND T.format = ?", (series_team_1, series_category, series_format))
            series_team_1_id = cursor.fetchone()[0]
            cursor.execute("SELECT T.team_id FROM Teams T INNER JOIN Countries C ON T.country_code = C.country_code AND C.country_name = ? AND T.category = ? AND T.format = ?", (series_team_2, series_category, series_format))
            series_team_2_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO Series (series_name, team_1_id, team_2_id, total_matches) VALUES (?, ?, ?, ?)", (series_name, series_team_1_id, series_team_2_id, series_total_matches))
            cursor.commit()
            QtWidgets.QMessageBox.information(
            self, "Series Added", f"Series: {series_name}, has been inserted successfully.")
            connection.close()
            self.accept()
        
    def update_teams(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT C.country_name FROM Countries C INNER JOIN Teams T ON C.country_code = T.country_code WHERE T.category = ? AND T.format = ?", (self.Category_ComboBox.currentText(), self. Format_ComboBox.currentText()))
        
        self.Team_1_ComboBox.clear()
        self.Team_2_ComboBox.clear()

        for item in cursor.fetchall():
            self.Team_1_ComboBox.addItem(item[0])
            self.Team_2_ComboBox.addItem(item[0])
        
        connection.close()

class AddTournamentDialog(QDialog):
    def __init__(self, connection_string):
        super(AddTournamentDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Add_Tournament_dlg.ui', self)

        self.connection_string = connection_string # store connection string locally

        self.Add_Tournament_Button.clicked.connect(self.add_tournament)

        self.Error_Label.hide()

    def add_tournament(self):
        tournament_name = self.Tournament_Entry.text()
        if not len(tournament_name):
            self.Error_Label.show()
            return
        tournament_category = self.Category_ComboBox.currentText()
        tournament_format = self.Format_ComboBox.currentText()

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Tournaments (tournament_name, category, format) VALUES (?, ?, ?)", (tournament_name, tournament_category, tournament_format))
        cursor.commit()

        # Show a message box with the order ID
        QtWidgets.QMessageBox.information(
            self, "Tournament Added", f"Tournament: {tournament_name}, has been inserted successfully.")

        connection.close()
        self.accept()

server = "LAPTOP-D5M397KF\DBMS_LAB6"
database = "ICC_Cricket_Management"
username = "sa"
password = "password123"
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = AddMatchDialog(connection_string) # Create an instance of our window
window.show()
app.exec() # Start the application