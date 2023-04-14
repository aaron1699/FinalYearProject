import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import json
import sys
import random
import os
import zipfile
import shutil
from PinOnImageWindow import PinOnImageWindow
from VevoxPDFGenerator import generator


def delete_folder_on_exit(folder_path):
    # Delete the folder if it exists
		if os.path.exists(folder_path):
			shutil.rmtree(folder_path)

class Window(qtw.QWidget):
	def __init__(self):
		super().__init__()
		layout = qtw.QGridLayout()
		layout.setContentsMargins(10, 10, 10, 10)
		layout.setSpacing(10)
		self.setWindowTitle("Vevox Editor")
		self.setLayout(layout)

		#box for question type
		questionType_group = qtw.QGroupBox("Question Type")
		questionType_layout = qtw.QHBoxLayout()
		questionType_group.setLayout(questionType_layout)
		layout.addWidget(questionType_group, 1, 0, 1, 3)

		self.questionTypeBox = qtw.QComboBox(self)
		self.questionTypeBox.addItem("MultipleChoice")
		self.questionTypeBox.addItem("Word Cloud")
		self.questionTypeBox.addItem("Text Question")
		self.questionTypeBox.addItem("Ranking By Preference")
		self.questionTypeBox.addItem("Ranking By Order")
		self.questionTypeBox.addItem("Numeric")
		self.questionTypeBox.addItem("Rating")
		self.questionTypeBox.addItem("XY Plot")
		self.questionTypeBox.addItem("Pin on Image")
		questionType_layout.addWidget(self.questionTypeBox)

		#box for question details
		question_group = qtw.QGroupBox("Question Details")
		question_layout = qtw.QGridLayout()
		question_group.setLayout(question_layout)
		layout.addWidget(question_group, 2, 0, 3, 3)

		self.questionText = qtw.QLabel("Question Text: ")
		question_layout.addWidget(self.questionText, 0, 0)

		self.questionInput = qtw.QLineEdit()
		question_layout.addWidget(self.questionInput, 0, 1, 1, 2)

		self.answer_here = qtw.QLabel("Enter Choices")
		question_layout.addWidget(self.answer_here, 1, 0)

		self.table = qtw.QTableWidget()

		question_layout.addWidget(self.table, 1, 1, 3, 6)

		self.table.setRowCount(0)
		self.table.setColumnCount(4)
		self.table.hideColumn(3)
		#self.table.setItem(0, 0, qtw.QTableWidgetItem("Name"))
		header = self.table.horizontalHeader()
		header.hide()

		self.addRowButton = qtw.QPushButton("Add Row")
		question_layout.addWidget(self.addRowButton, 2, 0)

		self.answerExplanation = qtw.QLabel("Answer Explanation")
		question_layout.addWidget(self.answerExplanation, 4, 0)

		self.answerExplanationInput = qtw.QLineEdit()
		question_layout.addWidget(self.answerExplanationInput, 4, 1, 1, 2)

		self.addAnswerstoImageButton = qtw.QPushButton("Add Image")
		question_layout.addWidget(self.addAnswerstoImageButton, 3, 0)

		#box for create question and opening image
		actions_group = qtw.QGroupBox("Actions")
		actions_layout = qtw.QVBoxLayout()
		actions_group.setLayout(actions_layout)
		layout.addWidget(actions_group, 5, 0, 2, 3)

		self.createButton = qtw.QPushButton("Create")
		self.createButton.clicked.connect(self.createQuestion)
		actions_layout.addWidget(self.createButton)

		self.imageButton = qtw.QPushButton("Open image file")
		self.imageButton.clicked.connect(self.getfile)
		actions_layout.addWidget(self.imageButton)

		self.image_label = qtw.QLabel(self)
		actions_layout.addWidget(self.image_label)

		#box for question bank
		question_bank_group = qtw.QGroupBox("Question Bank")
		question_bank_layout = qtw.QVBoxLayout()
		question_bank_group.setLayout(question_bank_layout)
		layout.addWidget(question_bank_group, 1, 6, 4, 3)

		self.questionBank = qtw.QListWidget()
		question_bank_layout.addWidget(self.questionBank)

		#box for creating poll and deleting questions
		question_bank_actions_group = qtw.QGroupBox("Question Bank Actions")
		question_bank_actions_layout = qtw.QHBoxLayout()
		question_bank_actions_group.setLayout(question_bank_actions_layout)
		layout.addWidget(question_bank_actions_group, 5, 6, 1, 3)

		self.createPoll = qtw.QPushButton("Create Poll")
		self.createPoll.clicked.connect(self.createpoll)
		question_bank_actions_layout.addWidget(self.createPoll)

		self.deleteQuestionButton = qtw.QPushButton("Delete Question")
		self.deleteQuestionButton.clicked.connect(self.deleteQuestion)
		question_bank_actions_layout.addWidget(self.deleteQuestionButton)

		self.pdfgeneratorButton = qtw.QPushButton("Generate PDF")
		self.pdfgeneratorButton.clicked.connect(self.pdfgen)
		layout.addWidget(self.pdfgeneratorButton, 6, 6, 1, 3)

		self.questionTypeBox.currentTextChanged.connect(self.showhide)

		self.answers = []
		self.check = []
		self.randint = None
		self.polls = []
		self.rank = []

		os.mkdir('resources')

		self.showhide('MultipleChoice')


	def pdfgen(self):
		self.generator = generator()


	#ViewHandler
	def MCQView(self):
		self.table.showColumn(1)
		self.table.hideColumn(3)
		self.table.setRowCount(0)
		self.answer_here.show()
		self.table.show()
		self.answerExplanation.show()
		self.answerExplanationInput.show()
		self.addAnswerstoImageButton.hide()
		self.addRowButton.show()
		try: self.addRowButton.disconnect()
		except Exception: pass
		self.addRowButton.clicked.connect(self.addRowMCQ)

	def wordCloudView(self):
		self.answer_here.hide()
		self.table.hide()
		self.answerExplanation.hide()
		self.answerExplanationInput.hide()
		self.addAnswerstoImageButton.hide()
		self.addRowButton.hide()


	def textQuestionView(self):
		self.table.setRowCount(0)
		self.answer_here.show()
		self.table.show()
		self.answerExplanation.show()
		self.answerExplanationInput.show()
		self.addAnswerstoImageButton.hide()
		self.addRowButton.show()
		try: self.addRowButton.disconnect()
		except Exception: pass
		self.addRowButton.clicked.connect(self.addRowTXT)

	def rankingPreferenceView(self):
		self.table.setRowCount(0)
		self.answer_here.show()
		self.table.show()
		self.answerExplanation.show()
		self.answerExplanationInput.show()
		self.addAnswerstoImageButton.hide()
		self.addRowButton.show()
		try: self.addRowButton.disconnect()
		except Exception: pass
		self.addRowButton.clicked.connect(self.addRowTXT)

	def rankingOrderingView(self):
		self.table.setRowCount(0)
		self.answer_here.show()
		self.table.show()
		self.answerExplanation.show()
		self.answerExplanationInput.show()
		self.addAnswerstoImageButton.hide()
		self.addRowButton.show()
		try: self.addRowButton.disconnect()
		except Exception: pass
		self.addRowButton.clicked.connect(self.addRowORD)

	def numericView(self):
		self.table.setRowCount(0)
		self.answer_here.show()
		self.table.show()
		self.answerExplanation.show()
		self.answerExplanationInput.show()
		self.addAnswerstoImageButton.hide()
		self.addRowButton.hide()
		try: self.addRowButton.disconnect()
		except Exception: pass
		self.addRowNUM()

	def ratingView(self):
		self.table.setRowCount(0)
		self.answer_here.hide()
		self.table.hide()
		self.answerExplanation.hide()
		self.answerExplanationInput.hide()
		self.addRowButton.hide()
		self.addAnswerstoImageButton.hide()

	def xyPlotView(self):
		self.table.setRowCount(0)
		self.answer_here.show()
		self.table.show()
		self.addAnswerstoImageButton.hide()
		self.addRowButton.show()
		try: self.addRowButton.disconnect()
		except Exception: pass
		self.addRowButton.clicked.connect(self.addRowTXT)
		#self.table.hideColumn(1)
		#self.table.hideColumn(3)
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

	def pinOnImageView(self):
		self.table.hide()
		self.addRowButton.hide()
		try: self.addRowButton.disconnect()
		except Exception: pass
		self.addAnswerstoImageButton.show()
		self.addAnswerstoImageButton.clicked.connect(self.POIgetfile)
		#self.addAnswerstoImageButton.clicked.connect(self.imageAnswersWindow)


	def showhide(self, text):
		if text == 'MultipleChoice':
			self.MCQView()
		elif text == 'Word Cloud':
			self.wordCloudView()
		elif text == 'Text Question':
			self.textQuestionView()
		elif text == 'Ranking By Preference':
			self.rankingPreferenceView()
		elif text == 'Ranking By Order':
			self.rankingOrderingView()
		elif text == 'Numeric':
			self.numericView()
		elif text == 'Rating':
			self.ratingView()
		elif text == 'XY Plot':
			self.xyPlotView()
		elif text == 'Pin on Image':
			self.pinOnImageView()


	#addingRowsLogicHandler

	def addRowMCQ(self):
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
		self.rank_boxes = []
		for i in range(self.table.rowCount()):
			rank_box = qtw.QComboBox()
			rank_box.addItems([str(j+1) for j in range(self.table.rowCount())])
			self.table.setCellWidget(i, 2, rank_box)
			self.rank_boxes.append(rank_box)

		# Create a rank dropdown menu for the new row
		row_count_options = [str(i+1) for i in range(row+1)]
		self.rank_box = qtw.QComboBox()
		self.rank_box.addItems(row_count_options)
		self.table.setCellWidget(row, 2, self.rank_box)
		self.rank_boxes.append(self.rank_box)
		

		# Update the items in the existing dropdown menus
		for box in self.rank_boxes:
			box.clear()
			box.addItems([str(i+1) for i in range(self.table.rowCount())])
			

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
		self.fname, _ = qtw.QFileDialog.getOpenFileName(
			self, 'Open file', 'c:\\', "Image files (*.jpg *.gif *.png)")
		self.image_label.setPixmap(qtg.QPixmap(self.fname))
		#self.image_label.scaled(300, 300)
		print(os.path.basename(self.fname))
		
	def POIgetfile(self):
		self.view = PinOnImageWindow()
		self.view.show()
		self.image_label.setPixmap(qtg.QPixmap(self.view.fname))
		#self.image_label.scaled(300, 300)
		print(os.path.basename(self.view.fname))

	def getfiles(self):
		os.chdir("resources")
		self.randint = str(random.randint(1000000,3000000))
		self.pixmap = self.image_label.pixmap()
		self.pixmap.save(self.randint + ".png")
		os.chdir("..")
		print(self.randint)

	def deleteQuestion(self):
		selected_row = self.questionBank.currentRow()
		self.questionBank.takeItem(selected_row)
		self.polls.pop(selected_row)
			

	def createQuestion(self):
		i = 0
		for i in range(self.table.rowCount()):
			if self.questionTypeBox.currentText() == 'MultipleChoice':
				self.answers.append(self.table.item(i,0).text())
				if self.table.item(i,1).checkState() == 2:
					self.check.append(True)
					print("True")
				if self.table.item(i,1).checkState() == 0:
					self.check.append(False)
					print("False")

			if self.questionTypeBox.currentText() == 'XY Plot':
				try: self.answers.append(self.table.item(i,0).text())
				except Exception: pass
			if self.questionTypeBox.currentText() == 'Ranking By Preference' or self.questionTypeBox.currentText() == 'Text Question':
				self.answers.append(self.table.item(i,0).text())
			if  self.questionTypeBox.currentText() == 'Ranking By Order':
				self.answers.append(self.table.item(i,0).text())
				orderId = self.table.cellWidget(i, 2)
				self.rank.append(orderId.currentText())

			i=i+1
		print(i)

		print(len(self.answers))
		print(self.answers)
		print(self.check)
		print(self.rank)

		if self.image_label.pixmap() != None:
			self.getfiles()

		
		question = {}
		question.clear()
		if self.questionTypeBox.currentText() == 'MultipleChoice':
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
			
		if self.questionTypeBox.currentText() == 'Word Cloud':
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

		if self.questionTypeBox.currentText() == 'Text Question':
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
				question['correctAnswers'].append(self.answers[x])
				x= x+1
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		if self.questionTypeBox.currentText() == 'Ranking By Preference':
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
			question['correctAnswer'] = ({"choices" : choices})
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		if self.questionTypeBox.currentText() == 'Ranking By Order':
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
			choices = []
			question['choices'] = []
			x=0
			
			for x in range(len(self.answers)):
				rankId = random.randint(1000000,3000000)
				question['choices'].append({"id": rankId, "sequence": x, "alias": None, "text": self.answers[x], "image": None})
				choices.append({"choiceId": rankId, "rank": self.rank[x]})
				x=x+1

			question['minNumberSelections'] = len(self.answers)
			question['maxNumberSelections'] = len(self.answers)
			question['correctAnswer'] = {}
			question['correctAnswer'] = ({"choices" : choices})
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		if self.questionTypeBox.currentText() == 'Numeric':
			question['@type'] = "NumericQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['uiType'] = "inputfield"
			question['resultFormat'] = "%"
			question['min'] = self.table.item(0,2).text()
			question['max'] = self.table.item(1,2).text()
			question['minLabel'] = ""
			question['maxLabel'] = ""
			question['correctAnswers'] = []
			correctAnswer = None
			errorMargin = None
			if self.table.item(3,2) != None or self.table.item(3,2) != None:
				correctAnswer = float(self.table.item(3,2).text())
				errorMargin = float(self.table.item(4,2).text())				
				question['correctAnswers'].append({"min" : round(correctAnswer - errorMargin, int(self.table.item(2,2).text())), "max" : round(correctAnswer + errorMargin, int(self.table.item(2,2).text()))})
			
			question['numberOfDecimals'] = self.table.item(2,2).text()
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		if self.questionTypeBox.currentText() == 'Rating':
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

		if self.questionTypeBox.currentText() == 'XY Plot':
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

		if self.questionTypeBox.currentText() == 'Pin on Image':
			question['@type'] = "ClickMapQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['options'] = []
			question['maxNumberSelections'] = 1
			question['correctAnswers'] = self.view.correctItems
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		self.polls.append(question)
		self.questionBank.addItem(question['text'])
		self.answers.clear()
		self.check.clear()
		self.table.clear()
		self.questionInput.clear()
		self.answerExplanationInput.clear()
		self.image_label.clear()
		self.showhide(self.questionTypeBox.currentText())
		self.randint = None
		print(self.polls)
		

	def createpoll(self):
		json_object = json.dumps(self.polls)

		with open("polls.json", "w") as outfile:
			outfile.write(json_object)

		folder_path = 'resources'
		json_path = 'polls.json'
		output_path = 'test.zip'
		with zipfile.ZipFile(output_path, 'w') as zip_file:
			for root, dirs, files in os.walk(folder_path):
				for file in files:
					file_path = os.path.join(root, file)
					zip_file.write(file_path)
    
			zip_file.write(json_path)
		

		shutil.rmtree("resources")
		os.mkdir("resources")
            


app = qtw.QApplication(sys.argv)
window = Window()
window.show()
app.aboutToQuit.connect(lambda: delete_folder_on_exit('resources'))
sys.exit(app.exec())


# click add answer then type and edit it
# select which questions to add to poll
# clear aspects of table
# images view and add?
# pin on image answers
# saving and deleting images
# text order and numeric dont work
# View, viewLogic, addRowLogic, deleteAnswer/deleteRow, deleteQuestion, CreateQuestion(for7 types of q diff functions), CreatePoll

#delete images from poll
#add pdfgenerator
#add min/maxselections
