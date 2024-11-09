from typing import Any
from PyQt5.QtCore import *  # type: ignore \\ This is horrendous but im too lazy
from PyQt5.QtWidgets import *  # type: ignore \\ This is horrendous but im too lazy
from qfluentwidgets import TableWidget, EditableComboBox as ComboBox
from data.Database import getGroups, getStudents
from data.Const import SEX, GROUPS, DIFFICULTIES


# Child of TableWidget (which is child of QTableWidget indeed) 
# With added custom functions
class Table(TableWidget):
    def __init__(self, option, parent = None):
        super().__init__(parent)
        self.option = option

        # Edit mode in which user can only choose rows
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)


    # Get selected row(s)
    def selectedRow(self):
        row = [self.selectedItems()[i].row() for i in range(0, len(self.selectedItems()), 4) if self.selectedItems()[i].row() < self.rowSize]
        return row
    

    # Get data from database (Groups) and load it in the table
    def draw(self, filters=None) -> None:
        self.setRowCount(0)
        if self.option:
            data: list[list[str]] = getStudents(filters)
        else:
            data: list[list[str]] = getGroups(filters)
        self.rowSize= len(data)

        if not data:
            for lineIndex, lineData in enumerate([['' for _ in range(self.columnCount())] for _ in range(50)]):
                if lineIndex == 0:
                    self.setColumnCount(len(lineData))
                self.insertRow(lineIndex)
                for columnIndex, columnData in enumerate(lineData):
                    self.setItem(lineIndex, columnIndex, QTableWidgetItem(str(columnData)))
        else:
            for lineIndex, lineData in enumerate([['' for _ in range(self.columnCount())] for _ in range(50 - len(data))]):
                if lineIndex == 0:
                    self.setColumnCount(len(lineData))
                self.insertRow(lineIndex)
                for columnIndex, columnData in enumerate(lineData):
                    self.setItem(lineIndex, columnIndex, QTableWidgetItem(str(columnData)))
            for lineIndex, lineData in enumerate(data):
                if lineIndex == 0:
                    self.setColumnCount(len(lineData))
                self.insertRow(lineIndex)
                for columnIndex, columnData in enumerate(lineData):
                    self.setItem(lineIndex, columnIndex, QTableWidgetItem(str(columnData)))