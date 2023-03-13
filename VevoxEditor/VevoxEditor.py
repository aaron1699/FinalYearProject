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

		#self.AnswerInput = qtw.QLineEdit()
		#layout.addWidget (self.AnswerInput,3 ,1 ,1 , 2)

		#self.addAnswerButton = qtw.QPushButton("Add Answer")
		#self.addAnswerButton.clicked.connect(self.addAnswer)
		#layout.addWidget(self.addAnswerButton, 4, 1)

		#self.deleteAnswerButton = qtw.QPushButton("Delete")
		#self.deleteAnswerButton.clicked.connect (self.deleteAnswer)
		#layout.addWidget(self.deleteAnswerButton, 4, 2)		
		
		
		self.answerExplanation = qtw.QLabel("Answer Explanation")
		layout.addWidget(self.answerExplanation, 8, 0)

		self.answerExplanationInput = qtw.QLineEdit()
		layout.addWidget (self.answerExplanationInput, 8, 1, 1, 2)


		#self.checkBoxListWidget = CheckBoxListWidget()
		#layout.addWidget(self.checkBoxListWidget, 6, 1, 2, 2)
		#self.checkBoxListWidget.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
		#self.checkBoxListWidget.itemDoubleClicked.connect(self.editItem)
		self.table = qtw.QTableWidget()
		layout.addWidget(self.table, 6, 1, 2, 6)

		self.table.setRowCount(0) 
		self.table.setColumnCount(3) 
		self.table.setItem(0,0, qtw.QTableWidgetItem("Name"))
		header = self.table.horizontalHeader()
		header.hide()

		self.deleteAnswerButton = qtw.QPushButton("Delete")
		self.deleteAnswerButton.clicked.connect(self.deleteAnswer)

		self.addRowButton = qtw.QPushButton("Add Row")
		self.addRowButton.clicked.connect(self.addRow)
		layout.addWidget(self.addRowButton, 4, 1)

		#self.testButton = qtw.QPushButton("Add Row")
		#self.testButton.clicked.connect(self.test)
		#layout.addWidget(self.testButton, 5, 1)

		#self.correctAnswerBox = qtw.QListWidget()
		#layout.addWidget(self.correctAnswerBox, 6, 1, 2, 2)

		#self.minTextLabel = qtw.QLabel("Min: ")
		#layout.addWidget(self.minTextLabel, 5, 0)

		#self.minTextInput = qtw.QLineEdit()
		#layout.addWidget (self.minTextInput, 5, 1, 1, 1)

		#self.maxTextLabel = qtw.QLabel("Max: ")
		#layout.addWidget(self.maxTextLabel, 5, 0)

		#self.maxTextInput = qtw.QLineEdit()
		#layout.addWidget (self.maxTextInput, 5, 1, 1, 1)

		#self.horizontalXLabel = qtw.QLabel("Horizontal (x axis): ")
		#layout.addWidget(self.horizontalXLabel, 5, 0)

		#self.horizontalXInput = qtw.QLineEdit()
		#layout.addWidget (self.horizontalXInput, 5, 1, 1, 1)

		#self.verticalYLabel = qtw.QLabel("Vertical (y axis): ")
		#layout.addWidget(self.verticalYLabel, 5, 0)

		#self.verticalYLabelInput = qtw.QLineEdit()
		#layout.addWidget (self.verticalYLabelInput, 5, 1, 1, 1)

		#self.XYMax = qtw.QLabel("Max Value: ")
		#layout.addWidget(self.XYMax, 5, 0)

		#self.XYMaxInput = qtw.QLineEdit()
		#layout.addWidget (self.XYMaxInput, 5, 1, 1, 1)
		self.createButton = qtw.QPushButton("Create")
		self.createButton.clicked.connect (self.createQuestion)
		#self.createButton.clicked.connect (self.addQuestion)
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

	def showhide(self, text):
		if text == 'MultipleChoice':
			self.answer_here.show()
			self.table.show()
			self.answerExplanation.show()
			self.answerExplanationInput.show()
			#hide
		elif text == 'Word Cloud':
			self.answer_here.hide()
			self.table.hide()
			self.answerExplanation.hide()
			self.answerExplanationInput.hide()
			#hide
			pass

		elif text == 'Text Question':
			#hide
			pass
		elif text == 'Ranking By Preference':
			pass
		elif text == 'Ranking By Order':
			pass
		elif text == 'Numeric':
			pass
		elif text == 'Rating':
			pass
		elif text == 'XY Plot':
			pass
		elif text == 'Pin on Image':
			pass
			#hide
	#	elif text == 'S':
	#		#text
	#		#image
	#		#xtext
	#		#ytext
	#		#minx
	#		#maxx
	#		#miny
	#		#maxy
	#		#items[sequence, text]
	#	elif text == 'ClickMapQuestion':
	#		#text
	#		#image
	#		#options[]
	#		#maxnumberselections
	#		#correctanswers
	#		#correctanswerexplanation

	#def addAnswer(self):
	#	if len(self.AnswerInput.text()) != 0:
	#		self.checkBoxListWidget.addItem(self.AnswerInput.text())
	#		self.answers.append(self.AnswerInput.text())
	#		print(self.answers)


	#def deleteAnswer(self):
	#	if len(self.answers) > 0:
	#		self.clicked = self.checkBoxListWidget.currentRow()
	#		if self.clicked >= 0:
	#			print(self.clicked)
	#			self.answers.pop(self.clicked)
	#			self.checkBoxListWidget.takeItem(self.clicked)
	#		print(self.answers)

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

	def editItem(self, item):
		item.setFlags(item.flags() | qtc.Qt.ItemIsEditable)
		self.checkBoxListWidget.editItem(item)
		

	def getfiles(self):
		#change directory then change back
		self.randint = str(random.randint(1000000,3000000))
		self.pixmap.save(self.randint + ".png")
		print(self.randint)
			

	def createQuestion(self):
		i = 0
		for i in range(self.table.rowCount()):
			self.answers.append(self.table.item(i,0).text())
			print(self.table.item(i,0).text())
			if self.table.item(i,1).checkState() == 2:
				self.check.append(True)
				print("True")
			if self.table.item(i,1).checkState() == 0:
				self.check.append(False)
				print("False")
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
				question['correctAnswers'].append({"text": self.answers[x]})
				x= x+1

			question['minNumberSelections'] = 1
			question['maxNumberSelections'] = 2
			question['resultFormat'] = "%"
			question['distributableWeight'] = None
			question['weightingSetting'] = None
			question['weightingFactor'] = None
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
			rankId = random.randint(1000000,3000000)
			for x in range(len(self.answers)):
				question['choices'].append({"id": rankId, "sequence": x, "alias": None, "text": self.answers[x], "image": None})
				x= x+1

			question['minNumberSelections'] = 1
			question['maxNumberSelections'] = 2
			choices = []
			choices.append({"choiceId": rankId, "rank": 1})
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
			question['min'] = self.minTextInput.text()
			question['max'] = self.maxTextInput.text()
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()
		if self.q_typeBox.currentText() == 'Rating':
			question['@type'] = self.q_typeBox.currentText()
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
		if self.q_typeBox.currentText() == 'XY Plot':
			question['@type'] = self.q_typeBox.currentText()
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
		if self.q_typeBox.currentText() == 'Pin on Image':
			question['@type'] = self.q_typeBox.currentText()
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