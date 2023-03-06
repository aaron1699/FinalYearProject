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

		self.q_typeBox.addItem("MultipleChoiceQuestion")
		self.q_typeBox.addItem("ClickMapQuestion")
		self.q_typeBox.addItem("OpenTextQuestion")
		self.q_typeBox.addItem("RankingQuestion")
		self.q_typeBox.addItem("NumericQuestion")
		self.q_typeBox.addItem("ScatterPlotQuestion")
		layout.addWidget(self.q_typeBox,1, 1, 1, 2)

		
		self.questionText = qtw.QLabel("Question Text: ")
		layout.addWidget(self.questionText, 2, 0)

		self.answerExplanation = qtw.QLabel("Answer Explanation")
		layout.addWidget(self.answerExplanation, 7, 0)

		answer_here = qtw.QLabel("Enter Correct Answers")
		layout.addWidget(answer_here, 3, 0)

		self.questionInput = qtw.QLineEdit()
		layout.addWidget (self.questionInput, 2, 1, 1, 2)

		self.explanation = qtw.QLineEdit()
		layout.addWidget (self.explanation, 7, 1, 1, 2)

		addAnswerButton = qtw.QPushButton("Add Answer")
		addAnswerButton.clicked.connect(self.addAnswer)
		layout.addWidget(addAnswerButton, 4, 1)

		deleteAnswerButton = qtw.QPushButton("Delete")
		deleteAnswerButton.clicked.connect (self.deleteAnswer)
		layout.addWidget(deleteAnswerButton, 4, 2)

		self.AnswerInput = qtw.QLineEdit()
		layout.addWidget (self.AnswerInput,3 ,1 ,1 , 2)

		self.createButton = qtw.QPushButton("Create")
		self.createButton.clicked.connect (self.createQuestion)
		layout.addWidget(self.createButton, 9, 1, 2,2)


		self.checkBoxListWidget = CheckBoxListWidget()
		layout.addWidget(self.checkBoxListWidget, 5, 1, 2, 2)

		self.btn = qtw.QPushButton("Open image file")
		self.btn.clicked.connect(self.getfile)
		
		layout.addWidget(self.btn, 11, 1, 2, 2)
		self.le = qtw.QLabel("")
		
		layout.addWidget(self.le)
		self.btn1 = qtw.QPushButton("button")
		self.btn1.clicked.connect(self.getfiles)
		layout.addWidget(self.btn1, 13, 1, 2, 2)
		


		self.answers = []
		self.check = []

	def addAnswer(self):
		self.checkBoxListWidget.addItem(self.AnswerInput.text())
		self.answers.append(self.AnswerInput.text())
		print(self.answers)

	def deleteAnswer(self):
		self.clicked = self.checkBoxListWidget.currentRow()
		self.answers.pop(self.clicked)
		self.checkBoxListWidget.takeItem(self.clicked)
		print(self.answers)

	def getfile(self):
		fname, _ = qtw.QFileDialog.getOpenFileName(
			self, 'Open file', 'c:\\', "Image files (*.jpg *.gif *.png)")
		self.pixmap = qtg.QPixmap(fname)
		self.le.setPixmap(self.pixmap)
		print(os.path.basename(fname))

		
	def getfiles(self):
		#default_dir = os.path.join(os.getcwd(), "resources")
		#os.chdir(default_dir)
		self.randint = str(random.randint(1000000,3000000))
		self.pixmap.save(self.randint + ".png")
		print(self.randint)

	def createQuestion(self):
		i =0
		correct = self.checkBoxListWidget.getCheckedRows()
		incorrect = self.checkBoxListWidget.getUncheckedRows()
		for i in range(len(self.answers)):
			if i in correct:
				print(self.answers[i] + "true")
				self.check.append(True)
			if i in incorrect:
				print(self.answers[i] + "false")
				self.check.append(False)
			i= i+1
			print(i)

		print(len(self.answers))
		print(self.checkBoxListWidget.getCheckedRows())
		print(self.checkBoxListWidget.getUncheckedRows())
		print(self.answers)
		print(self.check)


		polls = []
		question = {}
		question['@type'] = self.q_typeBox.currentText()
		question['wordCloudQuestion'] = False
		question['lowerCaseAlias'] = ""
		question['id'] = random.randint(1000000,3000000)
		question['alias'] = ""
		question['text'] = self.questionInput.text()
		question['image'] = self.randint
		question['correctAnswers'] = []

		#i=0
		#for i in range(len(self.answers)):
		#	question['choices'].append({"id": random.randint(1000000,3000000), "alias": None, "text": self.answers[i], "isCorrectAnswer": self.check[i], "excludeFromResults": False, "image": None})
		#	i= i+1

		question['maxLength'] = 2000
		question['maxWords'] = 150
		question['resultFormat'] = "RESPONSE_LIST"
		question['maxWordCount'] = None
		question['maxWordLength'] = None
		question['correctAnswerExplanation'] = self.explanation.text()
		polls.append(question)


		json_object = json.dumps(polls)

		with open("polls.json", "w") as outfile:
			outfile.write(json_object)

            
app = qtw.QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

