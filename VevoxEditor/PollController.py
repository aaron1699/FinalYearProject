import sys
import os
import json
import random
#from PollModel import PollModel
from PollView import PollView
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


class PollController:
	def __init__(self, view):
		#self.model = PollModel
		self.view = PollView(self)

		# Connect the view signals to the controller methods
	#def set_controller(self):
		self.view.createButton.clicked.connect(self.view.createQuestion)
		self.view.deleteQuestionButton.clicked.connect(self.view.deleteQuestion)
		self.view.createPoll.clicked.connect(self.view.createpoll)
		self.view.imageButton.clicked.connect(self.view.getfile)
		self.view.q_typeBox.currentTextChanged.connect(self.view.showhide)
		# Connect other view signals to the corresponding methods

			

	

def main():
    app = qtw.QApplication(sys.argv)

    #model = PollModel()
    view = PollView()
    controller = PollController(view)

    #controller(controller)
    view.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()