import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import json
import sys
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget
import random
import os

class Window(qtw.QWidget):
	def __init__(self):
		super().__init__()
		layout = qtw.QGridLayout()
		layout.setContentsMargins (20, 20, 20, 20)
		layout.setSpacing (10)
		self.setWindowTitle("Vevox Editor")
		self.setLayout (layout)
		
		q_type = qtw.QLabel("Question Type: ")
		layout.addWidget(q_type, 1, 0)
		
		self.table = qtw.QTableWidget()
		layout.addWidget(self.table, 1, 9, 2,5)
  
		#Row count
		self.table.setRowCount(0) 
  
		#Column count
		self.table.setColumnCount(3)  
  
		self.table.setItem(0,0, qtw.QTableWidgetItem("Name"))

		self.table.setShowGrid(False)

		header = self.table.horizontalHeader()
		header.hide()

		self.deleteAnswerButton = qtw.QPushButton("Delete")
		self.deleteAnswerButton.clicked.connect(self.deleteAnswer)

		self.addRowButton = qtw.QPushButton("Add Row")
		self.addRowButton.clicked.connect(self.addRow)
		layout.addWidget(self.addRowButton, 4, 1)

		self.testButton = qtw.QPushButton("Add Row")
		self.testButton.clicked.connect(self.test)
		layout.addWidget(self.testButton, 5, 1)
		
		self.addRow()
		
	def test(self):
		j=0
		for i in range(self.table.rowCount()):
				print(self.table.item(i,0).text())
				if self.table.item(i,1).checkState() == 2:
					print("True")
				if self.table.item(i,1).checkState() == 0:
					print("False")
				i=i+1


	def deleteAnswer(self):
		button = self.sender()
		if button:
			row = self.table.indexAt(button.pos()).row()
			self.table.removeRow(row)
			
	def addRow(self):
		row = self.table.rowCount()
		self.table.insertRow(row)
		chkBoxItem = qtw.QTableWidgetItem()
		chkBoxItem.setFlags(qtc.Qt.ItemIsUserCheckable | qtc.Qt.ItemIsEnabled)
		chkBoxItem.setCheckState(qtc.Qt.Unchecked)       
		self.table.setItem(row,1,chkBoxItem)

		self.deleteAnswerButton = qtw.QTableWidgetItem()
		self.deleteAnswerButton = qtw.QPushButton("Delete")
		self.deleteAnswerButton.clicked.connect(self.deleteAnswer)
		self.table.setCellWidget(row,2,self.deleteAnswerButton)
		


            
app = qtw.QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())


# click add answer then type and edit it
# select which questions to add to poll