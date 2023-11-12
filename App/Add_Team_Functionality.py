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
            selected_country = self.Country_Table.item(selected_row, 0).text()
            selected_country_code = self.Country_Table.item(selected_row, 1).text()
        
        # print(selected_row)

        # print(self.Password_Entry.text())

        if not len(self.Password_Entry.text()):
            errors.append("Password")

        if len(errors):
            self.Error_Label.setText("Please specify " + ", ".join(errors))
            self.Error_Label.show()
        elif not self.Password_Entry.text() == self.Confirm_Password_Entry.text():
            self.Error_Label.setText("Password must match")
            self.Error_Label.show()
        else:
            # connection = pyodbc.connect(self.connection_string)
            # cursor = connection.cursor()
            uname = f"{selected_country_code.strip()}_{self.Category_ComboBox.currentText()[0]}_{self.Format_ComboBox.currentText()}"
            print(uname)
            enc_pwd = hashlib.sha256(uname.encode("utf-8")).hexdigest()
            print(len(enc_pwd))
            # cursor.execute("INSERT INTO Power_Users (username, encrypted_password) VALUES (?, ?)", (uname, enc_pwd))

        # self.accept()


class AddCountryDialog(QDialog):
    def __init__(self, connection_string):
        super(AddCountryDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Add_Country_dlg.ui', self)

        self.connection_string = connection_string # store connection string locally

        self.Add_Country_Button.clicked.connect(self.add_country)

    def add_country(self):
        country = self.Country_Entry.text()
        country_code = self.Country_Code_Entry.text()
        print(country, country_code)

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Countries (country_name, country_code) VALUES (?, ?)", (country, country_code))
        cursor.commit()

        # Show a message box with the order ID
        QtWidgets.QMessageBox.information(
            self, "Country Added", f"Country Name: {country}, Code: {country_code} has been inserted successfully.")

        connection.close()
        self.accept()