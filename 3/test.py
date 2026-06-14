import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()




        self.square1 = QtWidgets.QLabel('this')
        self.square1.setStyleSheet("background-color: #FF5733; border: 2px solid black;")
        
        self.square2 = QtWidgets.QLabel()
        self.square2.setStyleSheet("background-color: #33FF57; border: 2px solid black;")
        
        # Setup the Grid Layout
        self.layout = QtWidgets.QGridLayout(self)
        
        # Add them to the grid (Row, Column)
        self.layout.addWidget(self.square1, 0, 0)
        self.layout.addWidget(self.square2, 0, 1)
        
        # To make sure they stretch evenly and fill the whole window:
        self.layout.setRowStretch(0, 1)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)


if __name__ == "__main__":


    # creats a application for the system
    app = QtWidgets.QApplication([])


    # creates hte window 
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())
