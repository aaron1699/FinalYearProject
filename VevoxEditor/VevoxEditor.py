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

		self.q_typeBox = qtw.QComboBox(self)
		self.q_typeBox.addItem("MultipleChoice")
		self.q_typeBox.addItem("Word Cloud")
		self.q_typeBox.addItem("Text Question")
		self.q_typeBox.addItem("Ranking By Preference")
		self.q_typeBox.addItem("Ranking By Order")
		self.q_typeBox.addItem("Numeric")
		self.q_typeBox.addItem("Rating")
		self.q_typeBox.addItem("XY Plot")
		self.q_typeBox.addItem("Pin on Image")
		layout.addWidget(self.q_typeBox,1, 1, 1, 2)

		
		self.questionText = qtw.QLabel("Question Text: ")
		layout.addWidget(self.questionText, 2, 0)

		self.questionInput = qtw.QLineEdit()
		layout.addWidget (self.questionInput, 2, 1, 1, 2)

		self.answer_here = qtw.QLabel("Enter Choices")
		layout.addWidget(self.answer_here, 6, 0)
		
		
		self.answerExplanation = qtw.QLabel("Answer Explanation")
		layout.addWidget(self.answerExplanation, 8, 0)

		self.answerExplanationInput = qtw.QLineEdit()
		layout.addWidget (self.answerExplanationInput, 8, 1, 1, 2)


		self.table = qtw.QTableWidget()
		layout.addWidget(self.table, 6, 1, 2, 6)

		self.table.setRowCount(0) 
		self.table.setColumnCount(4) 
		self.table.hideColumn(3)
		self.table.setItem(0,0, qtw.QTableWidgetItem("Name"))
		header = self.table.horizontalHeader()
		header.hide()

		self.deleteAnswerButton = qtw.QPushButton("Delete")
		self.deleteAnswerButton.clicked.connect(self.deleteAnswer)

		self.addRowButton = qtw.QPushButton("Add Row")
		
		layout.addWidget(self.addRowButton, 4, 1)

		
		self.createButton = qtw.QPushButton("Create")
		self.createButton.clicked.connect (self.createQuestion)
		layout.addWidget(self.createButton, 9, 1, 2,2)

		self.btn = qtw.QPushButton("Open image file")
		self.btn.clicked.connect(self.getfile)
		


		layout.addWidget(self.btn, 11, 1, 2, 2)
		self.le = qtw.QLabel("")
		
		layout.addWidget(self.le)
		self.btn1 = qtw.QPushButton("button")
		self.btn1.clicked.connect(self.getfiles)
		layout.addWidget(self.btn1, 13, 1, 2, 2)

		question_bank = qtw.QLabel("Question Bank")
		layout.addWidget(question_bank, 1, 4)

		self.questionBank = qtw.QListWidget()
		layout.addWidget(self.questionBank, 1, 5, 2, 2)

		self.createPoll = qtw.QPushButton("Create Poll")
		self.createPoll.clicked.connect(self.createpoll)
		layout.addWidget(self.createPoll, 4, 5)
		
		self.q_typeBox.currentTextChanged.connect(self.showhide)

		self.answers = []
		self.check = []
		self.randint = None
		self.polls = []
		self.rank = []

		self.showhide('MultipleChoice')

	def showhide(self, text):
		if text == 'MultipleChoice':
			self.table.setRowCount(0)
			self.answer_here.show()
			self.table.show()
			self.answerExplanation.show()
			self.answerExplanationInput.show()
			self.addRowButton.show()
			try: self.addRowButton.disconnect()
			except Exception: pass
			self.addRowButton.clicked.connect(self.addRowMCQ)
			
			#hide
		elif text == 'Word Cloud':
			self.answer_here.hide()
			self.table.hide()
			self.answerExplanation.hide()
			self.answerExplanationInput.hide()
			self.addRowButton.hide()
			#hide
			pass

		elif text == 'Text Question':
			self.table.setRowCount(0)
			self.answer_here.show()
			self.table.show()
			self.answerExplanation.show()
			self.answerExplanationInput.show()
			self.addRowButton.show()
			try: self.addRowButton.disconnect()
			except Exception: pass
			self.addRowButton.clicked.connect(self.addRowTXT)
			
			#hide
			
		elif text == 'Ranking By Preference':
			self.table.setRowCount(0)
			self.answer_here.show()
			self.table.show()
			self.answerExplanation.show()
			self.answerExplanationInput.show()
			self.addRowButton.show()
			try: self.addRowButton.disconnect()
			except Exception: pass
			self.addRowButton.clicked.connect(self.addRowTXT)
		elif text == 'Ranking By Order':
			self.table.setRowCount(0)
			self.answer_here.show()
			self.table.show()
			self.answerExplanation.show()
			self.answerExplanationInput.show()
			self.addRowButton.show()
			try: self.addRowButton.disconnect()
			except Exception: pass
			self.addRowButton.clicked.connect(self.addRowORD)
		elif text == 'Numeric':
			self.table.setRowCount(0)
			self.answer_here.show()
			self.table.show()
			self.answerExplanation.show()
			self.answerExplanationInput.show()
			self.addRowButton.show()
			try: self.addRowButton.disconnect()
			except Exception: pass
			self.addRowNUM()
		elif text == 'Rating':
			self.table.setRowCount(0)
			self.answer_here.hide()
			self.table.hide()
			self.answerExplanation.hide()
			self.answerExplanationInput.hide()
			self.addRowButton.hide()
		elif text == 'XY Plot':
			self.table.setRowCount(0)
			self.answer_here.show()
			self.table.show()
			self.addRowButton.show()
			try: self.addRowButton.disconnect()
			except Exception: pass
			self.addRowButton.clicked.connect(self.addRowTXT)
			self.table.hideColumn(1)
			self.table.hideColumn(3)
			self.table.setRowCount(4)
			self.xText = qtw.QTableWidgetItem()
			self.xText = qtw.QLabel("Horizontal X axis")
			self.table.setCellWidget(0,0,self.xText)

			self.yText = qtw.QTableWidgetItem()
			self.yText = qtw.QLabel("vertical Y axis")
			self.table.setCellWidget(1,0,self.yText)

			self.maxX = qtw.QTableWidgetItem()
			self.maxX = qtw.QLabel("Max X value")
			self.table.setCellWidget(2,0,self.maxX)

			self.maxY = qtw.QTableWidgetItem()
			self.maxY = qtw.QLabel("Max Y value")
			self.table.setCellWidget(3,0,self.maxY)

		elif text == 'Pin on Image':
			try: self.addRowButton.disconnect()
			except Exception: pass



	def addRowMCQ(self):
		self.table.showColumn(1)
		self.table.hideColumn(3)
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

	def addRowTXT(self):
		self.table.hideColumn(1)
		self.table.hideColumn(3)
		row = self.table.rowCount()
		self.table.insertRow(row)
		
		self.deleteAnswerButton = qtw.QTableWidgetItem()
		self.deleteAnswerButton = qtw.QPushButton("Delete")
		self.deleteAnswerButton.clicked.connect(self.deleteAnswer)
		self.table.setCellWidget(row,2,self.deleteAnswerButton)

	def addRowORD(self):
		self.table.hideColumn(1)
		self.table.showColumn(3)
		row = self.table.rowCount()
		self.table.insertRow(row)
		

		self.deleteAnswerButton = qtw.QTableWidgetItem()
		self.deleteAnswerButton = qtw.QPushButton("Delete")
		self.deleteAnswerButton.clicked.connect(self.deleteAnswer)
		self.table.setCellWidget(row,3,self.deleteAnswerButton)

	def addRowNUM(self):
		self.table.hideColumn(1)
		self.table.hideColumn(3)
		self.table.setRowCount(5)
		self.minLabel = qtw.QTableWidgetItem()
		self.minLabel = qtw.QLabel("Minimum Value")
		self.table.setCellWidget(0,0,self.minLabel)

		self.maxLabel = qtw.QTableWidgetItem()
		self.maxLabel = qtw.QLabel("Maximum Value")
		self.table.setCellWidget(1,0,self.maxLabel)

		self.decimalPlaces = qtw.QTableWidgetItem()
		self.decimalPlaces = qtw.QLabel("Decimal Places")
		self.table.setCellWidget(2,0,self.decimalPlaces)

		self.correctAnswer = qtw.QTableWidgetItem()
		self.correctAnswer = qtw.QLabel("Correct Answer")
		self.table.setCellWidget(3,0,self.correctAnswer)

		self.errorMargin = qtw.QTableWidgetItem()
		self.errorMargin = qtw.QLabel("Error Margin")
		self.table.setCellWidget(4,0,self.errorMargin)


	def deleteAnswer(self):
		button = self.sender()
		if button:
			row = self.table.indexAt(button.pos()).row()
			self.table.removeRow(row)

	def getfile(self):
		fname, _ = qtw.QFileDialog.getOpenFileName(
			self, 'Open file', 'c:\\', "Image files (*.jpg *.gif *.png)")
		self.pixmap = qtg.QPixmap(fname)
		self.le.setText(os.path.basename(fname))
		print(os.path.basename(fname))
		

	def getfiles(self):
		#change directory then change back
		self.randint = str(random.randint(1000000,3000000))
		self.pixmap.save(self.randint + ".png")
		print(self.randint)
			

	def createQuestion(self):
		i = 0
		for i in range(self.table.rowCount()):
			if self.q_typeBox.currentText() == 'MultipleChoice':
				self.answers.append(self.table.item(i,0).text())
				if self.table.item(i,1).checkState() == 2:
					self.check.append(True)
					print("True")
				if self.table.item(i,1).checkState() == 0:
					self.check.append(False)
					print("False")
			#if self.q_typeBox.currentText() == 'Text Question':
			#	self.answers.append(self.table.item(i,0).text())
			if self.q_typeBox.currentText() == 'XY Plot':
				try: self.answers.append(self.table.item(i,0).text())
				except Exception: pass
			if self.q_typeBox.currentText() == 'Ranking By Preference' or self.q_typeBox.currentText() == 'Ranking By Order' or self.q_typeBox.currentText() == 'Text Question':
				self.answers.append(self.table.item(i,0).text())
			#print(self.table.item(4,0).text())

			i=i+1
		print(i)

		print(len(self.answers))
		print(self.answers)
		print(self.check)


		
		question = {}
		question.clear()
		if self.q_typeBox.currentText() == 'MultipleChoice':
			question['@type'] = "MultipleChoiceQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['choices'] = []
			x=0
			for x in range(len(self.answers)):
				#self.answers.append(self.table.item(x,0).text())
				question['choices'].append({"id": random.randint(1000000,3000000), "alias": None, "text": self.answers[x], "isCorrectAnswer": self.check[x], "excludeFromResults": False, "image": None})
				x= x+1
			question['minNumberSelections'] = 1
			question['maxNumberSelections'] = 2
			question['resultFormat'] = "%"
			question['distributableWeight'] = None
			question['weightingSetting'] = None
			question['weightingFactor'] = None
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()
			
		if self.q_typeBox.currentText() == 'Word Cloud':
			question['@type'] = "OpenTextQuestion"
			question['wordCloudQuestion'] = True
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['maxLength'] = 2000
			question['maxWords'] = 150
			question['resultFormat'] = "WORD_CLOUD"
			question['maxWordCount'] = None
			question['maxWordLength'] = None
			question['correctAnswers'] = []
			x=0
			for x in range(len(self.answers)):
				question['correctAnswers'].append({"text": self.answers[x]})
				x= x+1
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		if self.q_typeBox.currentText() == 'Text Question':
			question['@type'] = "OpenTextQuestion"
			question['wordCloudQuestion'] = False
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['maxLength'] = 2000
			question['maxWords'] = 150
			question['resultFormat'] = "RESPONSE_LIST"
			question['maxWordCount'] = None
			question['maxWordLength'] = None
			question['correctAnswers'] = []
			x=0
			for x in range(len(self.answers)):
				#self.answers.append(self.table.item(x,0).text())
				question['correctAnswers'].append({x : self.answers[x]})
				x= x+1
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		if self.q_typeBox.currentText() == 'Ranking By Preference':
			question['@type'] = "RankingQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.questionInput.text()
			question['uiType'] = "ranking"
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['choices'] = []
			x=0
			for x in range(len(self.answers)):
				question['choices'].append({"id": random.randint(1000000,3000000), "sequence": x, "alias": None, "text": self.answers[x], "image": None})
				x= x+1
			question['minNumberSelections'] = 1
			question['maxNumberSelections'] = 2
			choices = []
			question['correctAnswer'] = None
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		if self.q_typeBox.currentText() == 'Ranking By Order':
			question['@type'] = "RankingQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.questionInput.text()
			question['uiType'] = "ordering"
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['choices'] = []
			x=0
			choices = []
			for x in range(len(self.answers)):
				rankId = random.randint(1000000,3000000)
				question['choices'].append({"id": rankId, "sequence": x, "alias": None, "text": self.answers[x], "image": None})
				choices.append({"choiceId": rankId, "rank": self.table.item(x,2).text()})
				x=x+1
			question['minNumberSelections'] = 1
			question['maxNumberSelections'] = 2
			question['correctAnswer'] = choices
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		if self.q_typeBox.currentText() == 'Numeric':
			question['@type'] = "NumericQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['resultFormat'] = "%"
			question['min'] = self.table.item(0,2).text()
			question['max'] = self.table.item(1,2).text()
			question['minLabel'] = None
			question['maxLabel'] = None
			correctAnswer = None
			errorMargin = None
			if self.table.item(3,2) != None or self.table.item(3,2) != None:
				correctAnswer = float(self.table.item(3,2).text())
				errorMargin = float(self.table.item(4,2).text())				
				question['correctAnswers'] = {"min" : round(correctAnswer - errorMargin, int(self.table.item(2,2).text())), "max" : round(correctAnswer + errorMargin, int(self.table.item(2,2).text()))}
			else:
				question['correctAnswers'] = []
			question['numberOfDecimals'] = self.table.item(2,2).text()
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		if self.q_typeBox.currentText() == 'Rating':
			question['@type'] = "NumericQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['uiType'] = "rating"
			question['resultFormat'] = "%"
			question['min'] = 1
			question['max'] = 5
			question['resultFormat'] = "%"
			question['correctAnswers'] = []
			question['numberOfDecimals'] = 0
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		if self.q_typeBox.currentText() == 'XY Plot':
			question['@type'] = "ScatterPlotQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['xText'] = self.table.item(0,2).text()
			question['yText'] = self.table.item(1,2).text()
			question['minX'] = 0
			question['maxX'] = self.table.item(2,2).text()
			question['minY'] = 0
			question['maxY'] = self.table.item(3,2).text()
			question['items'] = []
			for x in range(len(self.answers)):
				rankId = random.randint(1000000,3000000)
				question['items'].append({"id": rankId, "alias": None, "sequence": x, "text": self.answers[x]})

		if self.q_typeBox.currentText() == 'Pin on Image':
			question['@type'] = "ClickMapQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['choices'] = []

			x=0
			for x in range(len(self.answers)):
				question['choices'].append({"id": random.randint(1000000,3000000), "alias": None, "text": self.answers[x], "isCorrectAnswer": self.check[x], "excludeFromResults": False, "image": None})
				x= x+1

			question['minNumberSelections'] = 1
			question['maxNumberSelections'] = 2
			question['resultFormat'] = "%"
			question['distributableWeight'] = None
			question['weightingSetting'] = None
			question['weightingFactor'] = None
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		self.polls.append(question)
		self.questionBank.addItem(question['text'])
		self.answers.clear()
		self.check.clear()
		self.table.clear()
		self.q_typeBox.setCurrentText(self.q_typeBox.currentText())
		print(self.polls)
		

	def createpoll(self):
		json_object = json.dumps(self.polls)

		with open("polls.json", "w") as outfile:
			outfile.write(json_object)

            
app = qtw.QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())


# click add answer then type and edit it
# select which questions to add to poll
#clear aspects of table