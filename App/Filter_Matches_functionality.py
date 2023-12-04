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