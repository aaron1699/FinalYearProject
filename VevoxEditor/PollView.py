import PyQt5.QtWidgets as qtw


class View(qtw.QWidget):
	def __init__(self):
		super().__init__()
		layout = qtw.QGridLayout()
		layout.setContentsMargins(20, 20, 20, 20)
		layout.setSpacing(10)
		self.setWindowTitle("Vevox Editor")
		self.setLayout(layout)

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
		layout.addWidget(question_group, 2, 0, 4, 3)

		self.questionText = qtw.QLabel("Question Text: ")
		question_layout.addWidget(self.questionText, 0, 0)

		self.questionInput = qtw.QLineEdit()
		question_layout.addWidget(self.questionInput, 0, 1, 1, 6)

		self.answer_here = qtw.QLabel("Enter Choices")
		question_layout.addWidget(self.answer_here, 1, 0)

		self.table = qtw.QTableWidget()

		question_layout.addWidget(self.table, 1, 1, 3, 6)

		self.table.setRowCount(0)
		self.table.setColumnCount(4)
		self.table.hideColumn(3)
		self.table.setItem(0, 0, qtw.QTableWidgetItem("Name"))
		self.table.horizontalHeader().setHidden(True)

		self.addRowButton = qtw.QPushButton("Add Row")
		question_layout.addWidget(self.addRowButton, 2, 0)

		self.answerExplanation = qtw.QLabel("Answer Explanation")
		question_layout.addWidget(self.answerExplanation, 4, 0)

		self.answerExplanationInput = qtw.QLineEdit()
		question_layout.addWidget(self.answerExplanationInput, 4, 1, 1, 6)

		#box for create question and opening image
		actions_group = qtw.QGroupBox("Actions")
		actions_layout = qtw.QVBoxLayout()
		actions_group.setLayout(actions_layout)
		layout.addWidget(actions_group, 6, 0, 2, 3)

		self.createButton = qtw.QPushButton("Create")
		actions_layout.addWidget(self.createButton)

		self.imageButton = qtw.QPushButton("Add image")
		actions_layout.addWidget(self.imageButton)

		self.addAnswerstoImageButton = qtw.QPushButton("Add Image")
		actions_layout.addWidget(self.addAnswerstoImageButton)
		
		self.deleteImageButton = qtw.QPushButton("Delete Image")
		actions_layout.addWidget(self.deleteImageButton)


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
		question_bank_actions_layout.addWidget(self.createPoll)

		self.deleteQuestionButton = qtw.QPushButton("Delete Question")
		question_bank_actions_layout.addWidget(self.deleteQuestionButton)

		self.pdfgeneratorButton = qtw.QPushButton("Generate PDF")
		layout.addWidget(self.pdfgeneratorButton, 6, 6, 1, 2)

		self.importPollButton = qtw.QPushButton("Import Poll")
		layout.addWidget(self.importPollButton, 6, 8, 1, 1)

		