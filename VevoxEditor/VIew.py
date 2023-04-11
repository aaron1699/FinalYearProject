import os
from PyQt5 import QtWidgets as qtw

class PollView(qtw.QWidget):
	def __init__(self):
		super().__init__()
		layout = qtw.QGridLayout()
		layout.setContentsMargins(20, 20, 20, 20)
		layout.setSpacing(10)
		self.setWindowTitle("Vevox Editor")
		self.setLayout(layout)

		# Group box for question type
		q_type_group = qtw.QGroupBox("Question Type")
		q_type_layout = qtw.QHBoxLayout()
		q_type_group.setLayout(q_type_layout)
		layout.addWidget(q_type_group, 1, 0, 1, 3)

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
		q_type_layout.addWidget(self.q_typeBox)

		# Group box for question details
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
		question_layout.addWidget(self.table, 1, 1, 3, 2)

		self.table.setRowCount(0)
		self.table.setColumnCount(4)
		self.table.hideColumn(3)
		self.table.setItem(0, 0, qtw.QTableWidgetItem("Name"))
		header = self.table.horizontalHeader()
		header.hide()

		self.addRowButton = qtw.QPushButton("Add Row")
		question_layout.addWidget(self.addRowButton, 2, 0)

		self.answerExplanation = qtw.QLabel("Answer Explanation")
		question_layout.addWidget(self.answerExplanation, 4, 0)

		self.answerExplanationInput = qtw.QLineEdit()
		question_layout.addWidget(self.answerExplanationInput, 4, 1, 1, 2)

		# Group box for actions
		actions_group = qtw.QGroupBox("Actions")
		actions_layout = qtw.QVBoxLayout()
		actions_group.setLayout(actions_layout)
		layout.addWidget(actions_group, 5, 0, 2, 3)

		self.createButton = qtw.QPushButton("Create")
		actions_layout.addWidget(self.createButton)

		self.imageButton = qtw.QPushButton("Open image file")
		actions_layout.addWidget(self.imageButton)

		self.image_label = qtw.QLabel(self)
		actions_layout.addWidget(self.image_label)

		# Group box for question bank
		question_bank_group = qtw.QGroupBox("Question Bank")
		question_bank_layout = qtw.QVBoxLayout()
		question_bank_group.setLayout(question_bank_layout)
		layout.addWidget(question_bank_group, 1, 4, 4, 3)

		self.questionBank = qtw.QListWidget()
		question_bank_layout.addWidget(self.questionBank)

		# Group box for question bank actions
		question_bank_actions_group = qtw.QGroupBox("Question Bank Actions")
		question_bank_actions_layout = qtw.QHBoxLayout()
		question_bank_actions_group.setLayout(question_bank_actions_layout)
		layout.addWidget(question_bank_actions_group, 5, 4, 1, 3)

		self.createPoll = qtw.QPushButton("Create Poll")
		question_bank_actions_layout.addWidget(self.createPoll)

		self.deleteQuestionButton = qtw.QPushButton("Delete Question")
		question_bank_actions_layout.addWidget(self.deleteQuestionButton)


		self.answers = []
		self.check = []
		self.randint = None
		self.polls = []
		self.rank = []

		os.mkdir('resources')

		self.showhide('MultipleChoice')


