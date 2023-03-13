import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import json
import sys
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget
import random
import os


class CheckBoxListWidget(qtw.QListWidget):
    def __init__(self):
        super().__init__()

    def getCheckedRows(self):
        checkedItems = []
        for index in range(self.count()):
            item = self.item(index)
            if item.checkState() == qtc.Qt.Checked:
                checkedItems.append(index)
        return checkedItems

    def getUncheckedRows(self):
        uncheckedItems = []
        for index in range(self.count()):
            item = self.item(index)
            if item.checkState() != qtc.Qt.Checked:
                uncheckedItems.append(index)
        return uncheckedItems


class Window(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vevox Editor")
        self.answers = []
        self.check = []

        self.layout = qtw.QGridLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.create_question_type_dropdown()
        self.create_question_text_input()
        self.create_answer_explanation_input()
        self.create_answer_input()
        self.create_add_delete_answer_buttons()
        self.create_create_button()
        self.create_checkbox_list_widget()
        self.create_image_widgets()
        self.create_question_bank_widget()

        self.q_typeBox.currentTextChanged.connect(self.showhide)

    def create_question_type_dropdown(self):
        q_type = qtw.QLabel("Question Type: ")
        self.layout.addWidget(q_type, 1, 0)

        self.q_typeBox = qtw.QComboBox(self)
        self.q_typeBox.addItem("MultipleChoiceQuestion")
        self.q_typeBox.addItem("ClickMapQuestion")
        self.q_typeBox.addItem("OpenTextQuestion")
        self.q_typeBox.addItem("RankingQuestion")
        self.q_typeBox.addItem("NumericQuestion")
        self.q_typeBox.addItem("ScatterPlotQuestion")
        self.layout.addWidget(self.q_typeBox, 1, 1, 1, 2)

    def create_question_text_input(self):
        self.questionText = qtw.QLabel("Question Text: ")
        self.layout.addWidget(self.questionText, 2, 0)

        self.questionInput = qtw.QLineEdit()
        self.layout.addWidget(self.questionInput, 2, 1, 1, 2)

    def create_answer_explanation_input(self):
        self.answerExplanation = qtw.QLabel("Answer Explanation")
        self.layout.addWidget(self.answerExplanation, 7, 0)

        self.explanation = qtw.QLineEdit()
        self.layout.addWidget(self.explanation, 7, 1, 1, 2)

    def create_answer_input(self):
        answer_here = qtw.QLabel("Enter Answers")
        self.layout.addWidget(answer_here, 3, 0)

        self.AnswerInput = qtw.QLineEdit()
        self.layout.addWidget(self.AnswerInput, 3, 1, 1, 2)

    def create_add_delete_answer_buttons(self):
        addAnswerButton = qtw.QPushButton("Add Answer")
        addAnswerButton.clicked.connect(self.addAnswer)
        self.layout.addWidget(addAnswerButton, 4, 1)

        deleteAnswerButton = qtw.QPushButton("Delete")
        deleteAnswerButton.clicked.connect(self.deleteAnswer)
        self.layout.addWidget(deleteAnswerButton, 4, 2)