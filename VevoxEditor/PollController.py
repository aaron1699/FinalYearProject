import sys
import os
import json
import zipfile
import glob
from PollView import View
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from ViewHandler import ViewHandler
from VevoxPDFGenerator import PDFgenerator
from PinOnImageWindow import PinOnImageWindow
import shutil
import time
from createQuestion import QuestionHandler

def delete_folder_on_exit(folder_path):
    # delete the folder if it exists
		if os.path.exists(folder_path):
			shutil.rmtree(folder_path)

try:
	shutil.rmtree("resources")
except Exception: pass

class PollController():
	def __init__(self, view, viewHandler, PDFgenerator):
		self.view = view
		self.viewHandler = viewHandler
		self.generator = PDFgenerator
		self.answers = []
		self.check = []
		self.randint = None
		self.polls = []
		self.rank = []

		self.view.createButton.clicked.connect(self.addQuestionToPoll)
		self.view.deleteQuestionButton.clicked.connect(self.deleteQuestion)
		self.view.createPoll.clicked.connect(self.create_poll)
		self.view.imageButton.clicked.connect(self.getfile)
		self.view.pdfgeneratorButton.clicked.connect(self.generator.main)
		self.view.questionTypeBox.currentTextChanged.connect(self.viewHandler.showhide)
		self.view.deleteImageButton.clicked.connect(self.deleteImage)
		self.view.addAnswerstoImageButton.clicked.connect(self.POIgetfile)
		self.view.importPollButton.clicked.connect(self.importPoll)
		self.view.deleteAllButton.clicked.connect(self.deleteAll)

		self.viewHandler.showhide('MultipleChoice')
		os.mkdir('resources')

		
	def loadData(self):
		try:
			filename, _ = qtw.QFileDialog.getOpenFileName(None, "Select a zip file", ".", "Zip files (*.zip)")

			zfile = zipfile.ZipFile(filename)

			for file in zfile.namelist():
				zfile.extract(file)

			poll_file = zfile.open('polls.json')
            
		except Exception as e:
			error = str(e)
			self.display_message_box(error)
			return

		self.poll_data = json.load(poll_file)

		return self.poll_data
		

	def deleteImage(self):
		return self.view.image_label.clear()
			

	def getfile(self):
		self.fname, _ = qtw.QFileDialog.getOpenFileName(
			None, 'Open file', 'c:\\', "Image files (*.jpg *.gif *.png)")

		if self.fname:
			pixmap = qtg.QPixmap(self.fname)
			scaledPixmap = pixmap.scaled(900, 300, qtc.Qt.KeepAspectRatio)
			self.view.image_label.setPixmap(scaledPixmap)

		
	def POIgetfile(self): # get image for Pin On Image (POI) question 
		self.pinOnImage = PinOnImageWindow()
		self.pinOnImage.show()
		pixmap = qtg.QPixmap(self.pinOnImage.fname)
		scaledPixmap = pixmap.scaled(900, 300, qtc.Qt.KeepAspectRatio)
		self.view.image_label.setPixmap(scaledPixmap)
		print(os.path.basename(self.pinOnImage.fname))
		return


	def deleteQuestion(self):

		selected_row = self.view.questionBank.currentRow()

		if selected_row != -1:
			self.view.questionBank.takeItem(selected_row)

			if self.polls:

				image_name = self.polls[selected_row]['image']

				if image_name != None:
					for file_path in glob.glob("resources/*"):
						if os.path.basename(file_path).startswith(image_name):
							os.remove(file_path)

				self.polls.pop(selected_row)

	def deleteAll(self):
		self.polls.clear()
		self.view.questionBank.clear()
		self.delete_files_in_folder("resources")


	def importPoll(self):
		polldata = self.loadData()
		if polldata != None:
			for item in polldata:
				self.polls.append(item)
				self.view.questionBank.addItem(item['text'])

		
	def addQuestionToPoll(self): 
		try:
			questionHandler = QuestionHandler(self.view, self.pinOnImage)

		except Exception:
			questionHandler = QuestionHandler(self.view)

		createdQuestion = questionHandler.create_question()
		self.addQuestionToBank(createdQuestion)
		self.resetInputs()


	def addQuestionToBank(self, question):
		self.polls.append(question)
		self.view.questionBank.addItem(question['text'])

	def resetInputs(self):
		self.answers.clear()
		self.check.clear()
		self.view.table.clear()
		self.view.questionInput.clear()
		self.view.answerExplanationInput.clear()
		self.view.image_label.clear()
		self.viewHandler.showhide(self.view.questionTypeBox.currentText())
		self.view.maxNumberOfSelectionsInput.clear()
		self.randint = None


	def write_polls_to_file(self, polls):
		with open("polls.json", "w") as outfile:
			json.dump(polls, outfile)


	def create_zip_file(self, folder_path, json_path, output_path):
		with zipfile.ZipFile(output_path, 'w') as zip_file:
			for root, dirs, files in os.walk(folder_path):
				for file in files:
					file_path = os.path.join(root, file)
					zip_file.write(file_path)
			zip_file.write(json_path)


	def delete_files_in_folder(self, folder_path):
		file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
		for file_name in file_list:
			file_path = os.path.join(folder_path, file_name)
			os.remove(file_path)
			time.sleep(1)

	def clear_data(self, polls, question_bank):
		polls.clear()
		question_bank.clear()


	def display_message_box(self, text):
		msg_box = qtw.QMessageBox()
		msg_box.setText(text)
		#msg_box.setIcon(qtw.QMessageBox.Critical)
		msg_box.setWindowTitle("Information")
		msg_box.exec_()


	def create_poll(self):
		folder_path = os.path.join('resources')
		json_path = os.path.join(os.path.dirname(folder_path), 'polls.json')
		filename, _ = qtw.QFileDialog.getSaveFileName(None, "Save zip file", ".", "Zip files (*.zip)")
		output_path = os.path.join(filename)

		self.write_polls_to_file(self.polls)

		self.create_zip_file(folder_path, json_path, output_path)

		self.delete_files_in_folder(folder_path)

		self.clear_data(self.polls, self.view.questionBank)

		self.display_message_box("Poll Created!")


def main():

	app = qtw.QApplication(sys.argv)
	app.setStyleSheet("QComboBox { font-size: 12px; }")
	font = qtg.QFont("Arial", 12)
	#font.setBold(True)
	app.setFont(font)
	view = View()
	viewHandler = ViewHandler(view)
	controller = PollController(view, viewHandler, PDFgenerator)

	view.show()

	app.aboutToQuit.connect(lambda: delete_folder_on_exit('resources'))

	sys.exit(app.exec())


if __name__ == '__main__':
    main()