from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pyodbc
import hashlib
import sys

from Add_Team_Functionality import AddTeamDialog
from Add_Player_Functionality import AddPlayerDialog
from Add_Match_Results_Functionality import AddMatchResultsDialog
from Add_Match_Functionality import AddMatchDialog, RemoveMatchDialog, RespondMatchDialog
from Filter_Matches_functionality import FilterMatchDialog

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
        
        self.populate_uname()
        self.Error_Label.hide()
        self.Login_Button.clicked.connect(self.validate)

    def populate_uname(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM Power_Users WHERE team_id IS NOT NULL")
        self.Username_ComboBox.clear()
        self.Username_ComboBox.addItem("ICC_Manager")
        for res in cursor.fetchall():
            self.Username_ComboBox.addItem(res[0])


    def validate(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        uname = self.Username_ComboBox.currentText()
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
            # self.Username_Entry.setText("")
            self.Password_Entry.setText("")        

class UI(QMainWindow):
    def __init__(self, connection_string):
        # Call the inherited classes __init__ method
        super(UI, self).__init__() 
        # Load the .ui file
        uic.loadUi('Main_App.ui', self)

        self.connection_string = connection_string # store connection string locally

        self.status = -1 #User role -1 -> guest, 0 -> icc manager, 1.. -> team_id
        self.cur_uname = "Guest"

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

        # connect filter buttons in Teams
        self.normal_style = """/* Normal state */
            QPushButton {
                background-color: #fff; /* Default background color */
            }

            /* Hover state */
            QPushButton:hover {
                background-color: #ddf; /* Background color when hovered */
            }
            """
        
        self.highlighted_style = """/* Normal state */
            QPushButton {
                background-color: #aaf; /* Default background color */
            }

            /* Hover state */
            QPushButton:hover {
                background-color: #aaf; /* Background color when hovered */
            }
            """

        self.teams_table_cat = "Mens"
        self.teams_table_format = "T20I"
        self.teams_table_country = "%%"

        self.players_table_cat = "Mens"
        self.players_table_format = "T20I"
        self.players_table_role = "Batsman"
        self.players_table_country = "%%"
        self.player_table_name = '%%'
        self.player_table_year = '%%'

        self.teams_cat_highlight(self.Teams_Category_Mens_Button)
        self.Teams_Category_Mens_Button.clicked.connect(lambda: self.teams_cat_highlight(self.Teams_Category_Mens_Button))
        self.Teams_Category_Womens_Button.clicked.connect(lambda: self.teams_cat_highlight(self.Teams_Category_Womens_Button))

        self.players_cat_highlight(self.Players_Category_Mens_Button)
        self.Players_Category_Mens_Button.clicked.connect(lambda: self.players_cat_highlight(self.Players_Category_Mens_Button))
        self.Players_Category_Womens_Button.clicked.connect(lambda: self.players_cat_highlight(self.Players_Category_Womens_Button))

        # function for player role highlight
        self.players_role_highlight(self.Players_Role_Batsman_Button)
        self.Players_Role_AllRounder_Button.clicked.connect(lambda: self.players_role_highlight(self.Players_Role_AllRounder_Button)) #function is being called here
        self.Players_Role_Batsman_Button.clicked.connect(lambda: self.players_role_highlight(self.Players_Role_Batsman_Button)) #function is being called here
        self.Players_Role_Bowler_Button.clicked.connect(lambda: self.players_role_highlight(self.Players_Role_Bowler_Button)) #function is being called here

        self.his_cat_highlight(self.His_Category_Mens_Button)
        self.His_Category_Mens_Button.clicked.connect(lambda: self.his_cat_highlight(self.His_Category_Mens_Button))
        self.His_Category_Womens_Button.clicked.connect(lambda: self.his_cat_highlight(self.His_Category_Womens_Button))

        self.sch_cat_highlight(self.Sch_Category_Mens_Button)
        self.Sch_Category_Mens_Button.clicked.connect(lambda: self.sch_cat_highlight(self.Sch_Category_Mens_Button))
        self.Sch_Category_Womens_Button.clicked.connect(lambda: self.sch_cat_highlight(self.Sch_Category_Womens_Button))



        self.teams_format_highlight(self.Teams_Format_T20I_Button)
        self.Teams_Format_T20I_Button.clicked.connect(lambda: self.teams_format_highlight(self.Teams_Format_T20I_Button))
        self.Teams_Format_ODI_Button.clicked.connect(lambda: self.teams_format_highlight(self.Teams_Format_ODI_Button))
        self.Teams_Format_Test_Button.clicked.connect(lambda: self.teams_format_highlight(self.Teams_Format_Test_Button))

        self.players_format_highlight(self.Players_Format_T20I_Button)
        self.Players_Format_T20I_Button.clicked.connect(lambda: self.players_format_highlight(self.Players_Format_T20I_Button))
        self.Players_Format_ODI_Button.clicked.connect(lambda: self.players_format_highlight(self.Players_Format_ODI_Button))
        self.Players_Format_Test_Button.clicked.connect(lambda: self.players_format_highlight(self.Players_Format_Test_Button))

        self.his_format_highlight(self.His_Format_T20I_Button)
        self.His_Format_T20I_Button.clicked.connect(lambda: self.his_format_highlight(self.His_Format_T20I_Button))
        self.His_Format_ODI_Button.clicked.connect(lambda: self.his_format_highlight(self.His_Format_ODI_Button))
        self.His_Format_Test_Button.clicked.connect(lambda: self.his_format_highlight(self.His_Format_Test_Button))

        self.sch_format_highlight(self.Sch_Format_T20I_Button)
        self.Sch_Format_T20I_Button.clicked.connect(lambda: self.sch_format_highlight(self.Sch_Format_T20I_Button))
        self.Sch_Format_ODI_Button.clicked.connect(lambda: self.sch_format_highlight(self.Sch_Format_ODI_Button))
        self.Sch_Format_Test_Button.clicked.connect(lambda: self.sch_format_highlight(self.Sch_Format_Test_Button))

        # connect search in Teams
        self.Teams_Search_Country_Entry.textChanged.connect(self.teams_country_change)

        # Update tables
        self.populate_teams_table()
        self.populate_players_table()
        self.populate_matches_table()
        self.populate_scheduled_fixtures_table()
        self.populate_pending_matches_table()
        

        

        # connect log in and log out buttons to their respective dialogs
        self.Log_In_Button.clicked.connect(self.login_attempt)
        self.Log_Out_Button.clicked.connect(self.logout_attempt)
        
        

        # connect add team button
        self.Add_Team_Button.clicked.connect(self.add_team)
        self.Add_Player_Button.clicked.connect(self.add_player)    

        #connect Match History Buttons
        self.Filter_Match_Button.clicked.connect(self.filter_match_history)
        
        # connect internal buttons
        self.Players_Search_Button.clicked.connect(self.search_player)

        # Scheduled Fixtures
        self.Scheduled_Matches_Upload_Button.hide()
        self.Scheduled_Matches_Upload_Button.clicked.connect(self.upload_match_results)

        # Pending Matches
        self.Pending_Matches_Add_Match_Button.clicked.connect(self.add_pending_match)
        self.Pending_Matches_Respond_Button.clicked.connect(self.respond_pending_match)

    def login_attempt(self): # manages the change in option visibility between users
        dlg = LogInDialog(connection_string)
        if dlg.exec():
            if dlg.status == 0:
                self.status = dlg.status
                print("Logged in as ICC Manager")
                self.cur_uname = "ICC_Manager"
                self.Logged_in_as_Label.setText(self.cur_uname)

                self.Scheduled_Matches_Upload_Button.show()

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
                self.cur_uname = cursor.fetchone()[0].strip()
                self.Logged_in_as_Label.setText(self.cur_uname)

                self.Scheduled_Matches_Upload_Button.hide()

                self.Pending_Matches_Remove_Match_Button.hide()
                self.Pending_Matches_Add_Match_Button.hide()
                self.Pending_Matches_Respond_Button.show()

                self.Menu_Buttons[-3].show()
                self.Menu_Buttons[-2].hide()
                self.Menu_Buttons[-1].show()

                self.Log_In_Button.hide()
                self.Log_Out_Button.show()
            
            self.populate_pending_matches_table()
            
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
            self.Scheduled_Matches_Upload_Button.hide()
            self.cur_uname = "Guest"
            self.Logged_in_as_Label.setText(self.cur_uname)

    def populate_teams_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("select T.team_id, C.country_name, T.category, T.format from Teams T INNER JOIN Countries C ON T.country_code = C.country_code WHERE T.category = ? AND T.format = ? AND LOWER(C.country_name) like ?", (self.teams_table_cat, self.teams_table_format, self.teams_table_country))

        self.Teams_Ranking_Table.setRowCount(0)

        result = cursor.fetchall()

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(result):
            self.Teams_Ranking_Table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                # if (col_index == 1):
                    # cell_data = str(cell_data)
                    # tmp = cursor.execute("SELECT country_name FROM Countries WHERE country_code = ?", (cell_data))
                    # cell_data = tmp.fetchone()[0]
                item = QTableWidgetItem(str(cell_data))
                self.Teams_Ranking_Table.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()

    def populate_players_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("select distinct P.player_ID, P.player_name, C.country_name, P.age, P.gender, P.role from Players P INNER JOIN Countries C ON P.country_code=C.country_code INNER JOIN Plays_For F ON P.player_id=F.player_id INNER JOIN Teams T ON F.team_id=T.team_id WHERE T.category = ? AND T.format = ? AND P.role= ? AND LOWER(P.player_name) like ? AND LOWER(C.country_name) like ?", (self.players_table_cat, self.players_table_format,self.players_table_role, self.player_table_name, self.players_table_country))
        # cursor.execute("select * from players")
        self.Players_Ranking_Table.setRowCount(0)

        result = cursor.fetchall()
        print("players found: ", len(result))

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(result):
            self.Players_Ranking_Table.insertRow(row_index)
            offset = 0
            country = ""
            for col_index, cell_data in enumerate(row_data):
                # if (col_index == 2):
                #     cell_data = str(cell_data)
                #     tmp = cursor.execute("SELECT country_name FROM Countries WHERE country_code = ?", (cell_data))
                #     cell_data = tmp.fetchone()[0]

                item = QTableWidgetItem(str(cell_data))
                self.Players_Ranking_Table.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()
        
    def populate_matches_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("select M.match_id, M.match_id, M.venue, CAST(M.date_time AS DATE), CAST(M.date_time AS TIME), T1.category, T1.format, C1.country_name, C2.country_name from Matches M INNER JOIN Teams T1 ON M.team_1_id = T1.team_id INNER JOIN Teams T2 ON M.team_2_id = T2.team_id INNER JOIN Countries C1 ON C1.country_code = T1.country_code INNER JOIN Countries C2 ON C2.country_code = T2.country_code WHERE M.completed IS NOT NULL AND M.completed = 1")

        self.Match_History_Table.setRowCount(0)

        result = cursor.fetchall()
        # print(result)

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(result):
            self.Match_History_Table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                if col_index == 1:
                    match_id = int(row_data[0])
                    cursor.execute("SELECT series_name FROM Series_Matches WHERE match_id = ?", (match_id))
                    match_name = cursor.fetchone()
                    # print("series:", match_name)

                    if match_name is None:
                        cursor.execute("SELECT tournament_name + ' - ' + tournament_stage  FROM Tournament_Matches WHERE match_id = ?", (match_id))
                        match_name = cursor.fetchone()
                        # print("tournament:", match_name)
                        cell_data = "Tournament - " + match_name[0]
                    else:
                        cell_data = "Series - " + match_name[0]

                    # cell_data = match_name[0]
                item = QTableWidgetItem(str(cell_data))
                self.Match_History_Table.setItem(row_index, col_index, item)

    def populate_scheduled_fixtures_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("select M.match_id, M.match_id, M.venue, CAST(M.date_time AS DATE), CAST(M.date_time AS TIME), T1.category, T1.format, C1.country_name, C2.country_name from Matches M INNER JOIN Teams T1 ON M.team_1_id = T1.team_id INNER JOIN Teams T2 ON M.team_2_id = T2.team_id INNER JOIN Countries C1 ON C1.country_code = T1.country_code INNER JOIN Countries C2 ON C2.country_code = T2.country_code WHERE M.team_1_confirmation = 1 AND M.team_2_confirmation = 1 AND (M.completed IS NULL OR M.completed = 0)")


        self.Scheduled_Fixtures_Table.setRowCount(0)

        result = cursor.fetchall()
        # print(result)

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(result):
            self.Scheduled_Fixtures_Table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                if col_index == 1:
                    match_id = int(row_data[0])
                    cursor.execute("SELECT series_name FROM Series_Matches WHERE match_id = ?", (match_id))
                    match_name = cursor.fetchone()
                    # print("series:", match_name)

                    if match_name is None:
                        cursor.execute("SELECT tournament_name + ' - ' + tournament_stage  FROM Tournament_Matches WHERE match_id = ?", (match_id))
                        match_name = cursor.fetchone()
                        # print("tournament:", match_name)
                        cell_data = "Tournament - " + match_name[0]
                    else:
                        cell_data = "Series - " + match_name[0]

                    # cell_data = match_name[0]
                item = QTableWidgetItem(str(cell_data))
                self.Scheduled_Fixtures_Table.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()
        
    def populate_pending_matches_table(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # cursor.execute("select")
        print("current status:", self.status)
        if self.status == 0:
            cursor.execute("select M.match_id, M.match_id, M.venue, CAST(M.date_time AS DATE), CAST(M.date_time AS TIME), T1.category, T1.format, C1.country_name, C2.country_name, CASE WHEN M.team_1_confirmation = 1 THEN 'YES' WHEN M.team_1_confirmation = 0 THEN 'NO' ELSE 'Not Responded' END AS Team_1_Response, CASE WHEN M.team_2_confirmation = 1 THEN 'YES' WHEN M.team_2_confirmation = 0 THEN 'NO' ELSE 'Not Responded' END AS Team_2_Response from Matches M INNER JOIN Teams T1 ON M.team_1_id = T1.team_id INNER JOIN Teams T2 ON M.team_2_id = T2.team_id INNER JOIN Countries C1 ON C1.country_code = T1.country_code INNER JOIN Countries C2 ON C2.country_code = T2.country_code WHERE M.team_1_confirmation is NULL OR M.team_2_confirmation is NULL OR M.team_1_confirmation = 0 OR M.team_2_confirmation = 0")
        else:
            cursor.execute("select M.match_id, M.match_id, M.venue, CAST(M.date_time AS DATE), CAST(M.date_time AS TIME), T1.category, T1.format, C1.country_name, C2.country_name, CASE WHEN M.team_1_confirmation = 1 THEN 'YES' WHEN M.team_1_confirmation = 0 THEN 'NO' ELSE 'Not Responded' END AS Team_1_Response, CASE WHEN M.team_2_confirmation = 1 THEN 'YES' WHEN M.team_2_confirmation = 0 THEN 'NO' ELSE 'Not Responded' END AS Team_2_Response from Matches M INNER JOIN Teams T1 ON M.team_1_id = T1.team_id INNER JOIN Teams T2 ON M.team_2_id = T2.team_id INNER JOIN Countries C1 ON C1.country_code = T1.country_code INNER JOIN Countries C2 ON C2.country_code = T2.country_code WHERE (M.team_1_id = ? OR M.team_2_id = ?) AND (M.team_1_confirmation is NULL OR M.team_2_confirmation is NULL OR M.team_1_confirmation = 0 OR M.team_2_confirmation = 0)", (self.status, self.status))

        self.Pending_Matches_Table.setRowCount(0)

        result = cursor.fetchall()
        # print(result)

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(result):
            self.Pending_Matches_Table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                if col_index == 1:
                    match_id = int(row_data[0])
                    cursor.execute("SELECT series_name FROM Series_Matches WHERE match_id = ?", (match_id))
                    match_name = cursor.fetchone()
                    # print("series:", match_name)

                    if match_name is None:
                        cursor.execute("SELECT tournament_name + ' - ' + tournament_stage  FROM Tournament_Matches WHERE match_id = ?", (match_id))
                        match_name = cursor.fetchone()
                        # print("tournament:", match_name)
                        cell_data = "Tournament - " + match_name[0]
                    else:
                        cell_data = "Series - " + match_name[0]

                    # cell_data = match_name[0]
                item = QTableWidgetItem(str(cell_data))
                self.Pending_Matches_Table.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()

    def teams_cat_highlight(self, button):
        self.Teams_Category_Mens_Button.setStyleSheet(self.normal_style)
        self.Teams_Category_Womens_Button.setStyleSheet(self.normal_style)
        button.setStyleSheet(self.highlighted_style)
        self.teams_table_cat = button.text()
        self.populate_teams_table()

    # work completed
    def players_cat_highlight(self, button):
        self.Players_Category_Mens_Button.setStyleSheet(self.normal_style)
        self.Players_Category_Womens_Button.setStyleSheet(self.normal_style)
        button.setStyleSheet(self.highlighted_style)
        self.players_table_cat = button.text()
        self.populate_players_table()

    # work completed
    def his_cat_highlight(self, button):
        self.His_Category_Mens_Button.setStyleSheet(self.normal_style)
        self.His_Category_Womens_Button.setStyleSheet(self.normal_style)
        button.setStyleSheet(self.highlighted_style)
        self.his_table_cat = button.text()
        self.populate_matches_table()

    # work completed
    def sch_cat_highlight(self, button):
        self.Sch_Category_Mens_Button.setStyleSheet(self.normal_style)
        self.Sch_Category_Womens_Button.setStyleSheet(self.normal_style)
        button.setStyleSheet(self.highlighted_style)
        self.sch_table_cat = button.text()
        self.populate_scheduled_fixtures_table()
        
    def teams_format_highlight(self, button):
        self.Teams_Format_T20I_Button.setStyleSheet(self.normal_style)
        self.Teams_Format_ODI_Button.setStyleSheet(self.normal_style)
        self.Teams_Format_Test_Button.setStyleSheet(self.normal_style)
        button.setStyleSheet(self.highlighted_style)
        self.teams_table_format = button.text()
        self.populate_teams_table()


    # work completed
    def players_format_highlight(self, button):
        self.Players_Format_T20I_Button.setStyleSheet(self.normal_style)
        self.Players_Format_ODI_Button.setStyleSheet(self.normal_style)
        self.Players_Format_Test_Button.setStyleSheet(self.normal_style)
        button.setStyleSheet(self.highlighted_style)
        self.players_table_format = button.text()
        self.populate_players_table()

    # work completed
    def his_format_highlight(self, button):
        self.His_Format_T20I_Button.setStyleSheet(self.normal_style)
        self.His_Format_ODI_Button.setStyleSheet(self.normal_style)
        self.His_Format_Test_Button.setStyleSheet(self.normal_style)
        button.setStyleSheet(self.highlighted_style)
        self.his_table_format = button.text()
        self.populate_matches_table()

    # work completed
    def sch_format_highlight(self, button):
        self.Sch_Format_T20I_Button.setStyleSheet(self.normal_style)
        self.Sch_Format_ODI_Button.setStyleSheet(self.normal_style)
        self.Sch_Format_Test_Button.setStyleSheet(self.normal_style)
        button.setStyleSheet(self.highlighted_style)
        self.sch_table_format = button.text()
        self.populate_scheduled_fixtures_table()

    # work in progress
    def players_role_highlight(self, button):
        self.Players_Role_AllRounder_Button.setStyleSheet(self.normal_style)
        self.Players_Role_Batsman_Button.setStyleSheet(self.normal_style)
        self.Players_Role_Bowler_Button.setStyleSheet(self.normal_style)
        button.setStyleSheet(self.highlighted_style)
        self.players_table_role = button.text()
        self.populate_players_table()    

    def teams_country_change(self):
        self.teams_table_country = "%" + (self.Teams_Search_Country_Entry.text()).lower() + "%"
        self.populate_teams_table()

    def add_team(self):
        dlg = AddTeamDialog(self.connection_string)
        if dlg.exec():
            self.populate_teams_table()

    def add_player(self):
        dlg = AddPlayerDialog(self.status, self.connection_string)
        if dlg.exec():
            self.populate_players_table()

    def upload_match_results(self):
        selected_row = -1
        if not len(self.Scheduled_Fixtures_Table.selectedIndexes()):
            return

        selected_row = self.Scheduled_Fixtures_Table.currentRow()
        match_id = int(self.Scheduled_Fixtures_Table.item(selected_row, 0).text())
        cat = self.Scheduled_Fixtures_Table.item(selected_row, 5).text()
        form = self.Scheduled_Fixtures_Table.item(selected_row, 6).text()
        count1 = self.Scheduled_Fixtures_Table.item(selected_row, 7).text()
        count2 = self.Scheduled_Fixtures_Table.item(selected_row, 8).text()

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        print(count1, cat, form)
        cursor.execute("SELECT team_id FROM Teams T INNER JOIN Countries C ON T.country_code = C.country_code WHERE C.country_name = ? AND T.category = ? AND T.format = ?", (count1, cat, form))
        t1 = int(cursor.fetchone()[0])

        cursor.execute("SELECT team_id FROM Teams T INNER JOIN Countries C ON T.country_code = C.country_code WHERE C.country_name = ? AND T.category = ? AND T.format = ?", (count2, cat, form))
        t2 = int(cursor.fetchone()[0])

        connection.close()
        
        dlg = AddMatchResultsDialog(match_id, t1, t2, self.connection_string)
        if dlg.exec():
            self.populate_matches_table()
            self.populate_pending_matches_table()
            self.populate_players_table()
            self.populate_teams_table()

    def add_pending_match(self):
        dlg = AddMatchDialog(self.connection_string)
        if dlg.exec():
            self.populate_pending_matches_table()

    def remove_pending_match(self):
        selected_row = -1
        if not len(self.Pending_Matches_Table.selectedIndexes()):
            return

        selected_row = self.Pending_Matches_Table.currentRow()
        val_list = []
        for col in range(self.Pending_Matches_Table.columnCount()):
            item = self.Pending_Matches_Table.item(selected_row, col)
            val_list.append(item.text())

        dlg = RemoveMatchDialog(self.connection_string, val_list)
        if dlg.exec():
            self.populate_pending_matches_table()

    def respond_pending_match(self):
        selected_row = -1
        if not len(self.Pending_Matches_Table.selectedIndexes()):
            return

        selected_row = self.Pending_Matches_Table.currentRow()
        val_list = []
        for col in range(self.Pending_Matches_Table.columnCount()):
            item = self.Pending_Matches_Table.item(selected_row, col)
            val_list.append(item.text())

        dlg = RespondMatchDialog(self.connection_string, self.status, val_list)
        if dlg.exec():
            self.populate_pending_matches_table()
            print("populating scheduled fixtures")
            self.populate_scheduled_fixtures_table()
            
            
    def filter_match_history(self):
        dlg = FilterMatchDialog(self.connection_string)
        if dlg.exec():
            self.populate_matches_table()
         

    def search_player(self):
        self.player_table_name ="%" + (self.Players_Search_Name_Entry.text()).lower() + "%"
        self.players_table_country ="%" + (self.Players_Search_Country_Entry.text()).lower() + "%"
        self.player_table_year ="%" + (self.Players_Search_Year_Entry.text()).lower() + "%"
        
        self.populate_players_table()

# Rohaan's credentials
# server = 'desktop-f0ere45'
# database = "ICC_Cricket_Management"
# windows_authentication = True 
# username = "sa"
# password = "password123"
# connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Musab's credentials
server = "LAPTOP-D5M397KF\DBMS_LAB6"
database = "ICC_Cricket_Management"
username = "sa"
password = "password123"
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'

# Hamza's credentials
# server = 'LAPTOP-2LF8R7KR'
# database = "ICC_Cricket_Management"
# connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'


# if windows_authentication:
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQLServer}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
# else:    
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = UI(connection_string) # Create an instance of our window
window.show()
app.exec() # Start the application