from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pyodbc
import hashlib
import sys

class FilterMatchDialog(QDialog):
    def __init__(self, connection_string):
        super(FilterMatchDialog, self).__init__() 
        # Load the .ui file
        uic.loadUi('Filter_matches.ui', self)

        self.connection_string = connection_string # Locally store connection string
        
        self.Apply_Filter_Button.clicked.connect(self.apply_filter)
        
        
    def apply_filter(self):
        cur_form = self.format_comboBox.currentText()
        cur_team = self.team_comboBox.currentText()
        cur_tourn = self.tournament_comboBOx.currentText()
        cur_year = self.year_comboBox.currentText()
        return cur_form, cur_team, cur_tourn, cur_year
