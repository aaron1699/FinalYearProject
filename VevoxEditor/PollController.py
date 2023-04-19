import sys
import os
import json
import random
import zipfile
#from PollModel import PollModel
from PollView import View
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from ViewHandler import ViewHandler
from VevoxPDFGenerator import generator
from PinOnImageWindow import PinOnImageWindow
import shutil


def delete_folder_on_exit(folder_path):
    # Delete the folder if it exists
		if os.path.exists(folder_path):
			shutil.rmtree(folder_path)

try:
	shutil.rmtree("resources")
except Exception: pass

class PollController():
	def __init__(self, view, viewHandler):
			#super().__init__()
		#self.model = PollModel
		self.view = view
		self.viewHandler = viewHandler
		self.answers = []
		self.check = []
		self.randint = None
		self.polls = []
		self.rank = []
		#self.generator = generator()
		# Connect the view signals to the controller methods
	#def set_controller(self):
		self.view.createButton.clicked.connect(self.createQuestion)
		self.view.deleteQuestionButton.clicked.connect(self.deleteQuestion)
		self.view.createPoll.clicked.connect(self.createpoll)
		self.view.imageButton.clicked.connect(self.getfile)
		self.view.pdfgeneratorButton.clicked.connect(self.pdfgen)
		self.view.questionTypeBox.currentTextChanged.connect(self.viewHandler.showhide)
		self.view.deleteImageButton.clicked.connect(self.deleteImage)
		self.view.addAnswerstoImageButton.clicked.connect(self.POIgetfile)
		#add poimage button connected
		# Connect other view signals to the corresponding methods

		self.viewHandler.showhide('MultipleChoice')
		os.mkdir('resources')

	def pdfgen(self):
		self.generator = generator()

	def deleteImage(self):
		self.view.image_label.clear()
			

	def getfile(self):
		self.fname, _ = qtw.QFileDialog.getOpenFileName(
			None, 'Open file', 'c:\\', "Image files (*.jpg *.gif *.png)")
		self.view.image_label.setPixmap(qtg.QPixmap(self.fname))
		#self.image_label.scaled(300, 300)
		print(os.path.basename(self.fname))
		
	def POIgetfile(self): # get image for Pin On Image (POI) question 
		self.pinOnImage = PinOnImageWindow()
		self.pinOnImage.show()
		self.view.image_label.setPixmap(qtg.QPixmap(self.pinOnImage.fname))
		#self.image_label.scaled(300, 300)
		print(os.path.basename(self.pinOnImage.fname))
		return

	def saveImage(self):
		os.chdir("resources")
		self.randint = str(random.randint(1000000,3000000))
		self.pixmap = self.view.image_label.pixmap()
		self.pixmap.save(self.randint + ".png")
		os.chdir("..")
		print(self.randint)

	def deleteQuestion(self):
		selected_row = self.view.questionBank.currentRow()
		if selected_row != -1:
			self.view.questionBank.takeItem(selected_row)
			if self.polls:
				self.polls.pop(selected_row)


	def createQuestion(self):		
		i = 0
		for i in range(self.view.table.rowCount()):
			if self.view.questionTypeBox.currentText() == 'MultipleChoice':
				self.answers.append(self.view.table.item(i,0).text())
				if self.view.table.item(i,1).checkState() == 2:
					self.check.append(True)
					print("True")
				if self.view.table.item(i,1).checkState() == 0:
					self.check.append(False)
					print("False")

			if self.view.questionTypeBox.currentText() == 'XY Plot':
				try: self.answers.append(self.view.table.item(i,0).text())
				except Exception: pass
			if self.view.questionTypeBox.currentText() == 'Ranking By Preference' or self.view.questionTypeBox.currentText() == 'Text Question':
				self.answers.append(self.view.table.item(i,0).text())
			if  self.view.questionTypeBox.currentText() == 'Ranking By Order':
				self.answers.append(self.view.table.item(i,0).text())
				orderId = self.view.table.cellWidget(i, 2)
				self.rank.append(orderId.currentText())

			i=i+1
		print(i)

		print(len(self.answers))
		print(self.answers)
		print(self.check)
		print(self.rank)

		if self.view.image_label.pixmap() != None:
			self.saveImage()

		
		question = {}
		question.clear()
		if self.view.questionTypeBox.currentText() == 'MultipleChoice':
			question['@type'] = "MultipleChoiceQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
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
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()
		if self.view.questionTypeBox.currentText() == 'Word Cloud':
			question['@type'] = "OpenTextQuestion"
			question['wordCloudQuestion'] = True
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
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
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

		if self.view.questionTypeBox.currentText() == 'Text Question':
			question['@type'] = "OpenTextQuestion"
			question['wordCloudQuestion'] = False
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
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
				#self.answers.append(self.view.table.item(x,0).text())
				question['correctAnswers'].append(self.answers[x])
				x= x+1
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

		if self.view.questionTypeBox.currentText() == 'Ranking By Preference':
			question['@type'] = "RankingQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
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
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

		if self.view.questionTypeBox.currentText() == 'Ranking By Order':
			question['@type'] = "RankingQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
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
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

		if self.view.questionTypeBox.currentText() == 'Numeric':
			question['@type'] = "NumericQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['uiType'] = "inputfield"
			question['resultFormat'] = "%"
			question['min'] = self.view.table.item(0,2).text()
			question['max'] = self.view.table.item(1,2).text()
			question['minLabel'] = ""
			question['maxLabel'] = ""
			question['correctAnswers'] = []
			correctAnswer = None
			errorMargin = None
			if self.view.table.item(3,2) != None or self.view.table.item(3,2) != None:
				correctAnswer = float(self.view.table.item(3,2).text())
				errorMargin = float(self.view.table.item(4,2).text())				
				question['correctAnswers'].append({"min" : round(correctAnswer - errorMargin, int(self.view.table.item(2,2).text())), "max" : round(correctAnswer + errorMargin, int(self.view.table.item(2,2).text()))})
			
			question['numberOfDecimals'] = self.view.table.item(2,2).text()
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

		if self.view.questionTypeBox.currentText() == 'Rating':
			question['@type'] = "NumericQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
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
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

		if self.view.questionTypeBox.currentText() == 'XY Plot':
			question['@type'] = "ScatterPlotQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['xText'] = self.view.table.item(0,2).text()
			question['yText'] = self.view.table.item(1,2).text()
			question['minX'] = 0
			question['maxX'] = self.view.table.item(2,2).text()
			question['minY'] = 0
			question['maxY'] = self.view.table.item(3,2).text()
			question['items'] = []
			for x in range(len(self.answers)):
				rankId = random.randint(1000000,3000000)
				question['items'].append({"id": rankId, "alias": None, "sequence": x, "text": self.answers[x]})

		if self.view.questionTypeBox.currentText() == 'Pin on Image':
			question['@type'] = "ClickMapQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
			if self.randint != None:
				question['image'] = self.randint
			else:
				question['image'] = None
			question['options'] = []
			question['maxNumberSelections'] = 1
			question['correctAnswers'] = self.pinOnImage.correctItems
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()


		self.polls.append(question)
		self.view.questionBank.addItem(question['text'])
		self.answers.clear()
		self.check.clear()
		self.view.table.clear()
		self.view.questionInput.clear()
		self.view.answerExplanationInput.clear()
		self.view.image_label.clear()
		self.viewHandler.showhide(self.view.questionTypeBox.currentText())
		self.randint = None
		print(self.polls)


	def createpoll(self):
		# Write the JSON data to a file
		with open("polls.json", "w") as outfile:
			json.dump(self.polls, outfile)

		# Create paths to the files
		folder_path = os.path.join('resources')
		json_path = os.path.join(os.path.dirname(folder_path), 'polls.json')
		output_path = os.path.join('test.zip')

		# Create the zip file and add files to it
		with zipfile.ZipFile(output_path, 'w') as zip_file:
			for root, dirs, files in os.walk(folder_path):
				for file in files:
					file_path = os.path.join(root, file)
					zip_file.write(file_path)
			zip_file.write(json_path)

		# Delete all the files in the folder
		file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
		for file_name in file_list:
			file_path = os.path.join(folder_path, file_name)
			os.remove(file_path)

		self.polls.clear()
		self.view.questionBank.clear()
		#shutil.rmtree("resources")
		#os.mkdir("resources")
           
		msg_box = qtw.QMessageBox()
		msg_box.setText("Poll Created!")
		msg_box.exec_()


def main():

	app = qtw.QApplication(sys.argv)
	
	#model = PollModel()
	view = View()
	viewHandler = ViewHandler(view)
	controller = PollController(view, viewHandler)

	view.show()

	app.aboutToQuit.connect(lambda: delete_folder_on_exit('resources'))

	sys.exit(app.exec())


if __name__ == '__main__':
    main()