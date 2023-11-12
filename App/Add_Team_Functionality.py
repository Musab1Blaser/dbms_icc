from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pyodbc
import hashlib
import sys

class AddTeamDialog(QDialog):
    def __init__(self, connection_string):
        super(AddTeamDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Add_Team_dlg.ui', self)

        self.connection_string = connection_string # Locally store connection string

        self.Error_Label.hide()
        self.populateCountries()
        self.Add_Country_Button.clicked.connect(self.add_country)
        self.Add_Team_Button.clicked.connect(self.validate)

    def populateCountries(self):
        # Connect to db
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM Countries")

        self.Country_Table.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.Country_Table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.Country_Table.setItem(row_index, col_index, item)

        connection.close()

    def add_country(self):
        dlg = AddCountryDialog(self.connection_string)
        if dlg.exec():
            self.populateCountries()
    
    def validate(self):
        errors = []
        selected_row = -1
        if not len(self.Country_Table.selectedIndexes()): # If no record selected then do nothing
            errors.append("Country")
        else:
            selected_row = self.Country_Table.currentRow()
            selected_country_code = self.Country_Table.item(selected_row, 0).text()
        
        if not len(self.Password_Entry.text()):
            errors.append("Password")

        if len(errors): # Incomplete Info
            self.Error_Label.setText("Please specify " + ", ".join(errors))
            self.Error_Label.show()
        elif not self.Password_Entry.text() == self.Confirm_Password_Entry.text():
            self.Error_Label.setText("Password must match")
            self.Error_Label.show()

        else:
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()

            team_category = self.Category_ComboBox.currentText()
            team_format = self.Format_ComboBox.currentText()

            # add new team
            cursor.execute("INSERT INTO Teams (country_code, category, format) VALUES (?, ?, ?)", (selected_country_code, team_category, team_format))
            cursor.commit()

            # get team id
            cursor.execute("SELECT MAX(team_id) FROM TEAMS") 
            team_id = cursor.fetchone()[0]
            # print(team_id)

            # Generate username from provided details
            uname = f"{selected_country_code.strip()}_{team_category[0]}_{team_format}"
            # print(uname)

            # encrypt password
            pwd = self.Password_Entry.text()
            enc_pwd = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
            # print(len(enc_pwd))

            # add power user
            cursor.execute("INSERT INTO Power_Users (username, encrypted_password, team_id) VALUES (?, ?, ?)", (uname, enc_pwd, team_id))
            cursor.commit()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Team Inserted", f"New Team created with username: {uname}.")

            self.accept()


class AddCountryDialog(QDialog):
    def __init__(self, connection_string):
        super(AddCountryDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Add_Country_dlg.ui', self)

        self.connection_string = connection_string # store connection string locally

        self.Add_Country_Button.clicked.connect(self.add_country)

    def add_country(self):
        country_name = self.Country_Entry.text()
        country_code = self.Country_Code_Entry.text()
        print(country_name, country_code)

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Countries (country_code, country_name) VALUES (?, ?)", (country_code, country_name))
        cursor.commit()

        # Show a message box with the order ID
        QtWidgets.QMessageBox.information(
            self, "Country Added", f"Country Name: {country_name}, Code: {country_code} has been inserted successfully.")

        connection.close()
        self.accept()