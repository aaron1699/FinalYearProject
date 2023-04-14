import sys
import os
import json
import random
#import PollController
#import PollView
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class PollModel:
    def __init__(self):     
	def showhide(self, text):
		if text == 'MultipleChoice':
			self.view.table.setRowCount(0)
			self.view.answer_here.show()
			self.view.table.show()
			self.view.answerExplanation.show()
			self.view.answerExplanationInput.show()
			self.view.addRowButton.show()
			try: self.view.addRowButton.disconnect()
			except Exception: pass
			self.view.addRowButton.clicked.connect(self.addRowMCQ)
			
			#hide
		elif text == 'Word Cloud':
			self.view.answer_here.hide()
			self.view.table.hide()
			self.view.answerExplanation.hide()
			self.view.answerExplanationInput.hide()
			self.view.addRowButton.hide()
			#hide
			pass

		elif text == 'Text Question':
			self.view.table.setRowCount(0)
			self.view.answer_here.show()
			self.view.table.show()
			self.view.answerExplanation.show()
			self.view.answerExplanationInput.show()
			self.view.addRowButton.show()
			try: self.view.addRowButton.disconnect()
			except Exception: pass
			self.view.addRowButton.clicked.connect(self.addRowTXT)
			
			#hide
			
		elif text == 'Ranking By Preference':
			self.view.table.setRowCount(0)
			self.view.answer_here.show()
			self.view.table.show()
			self.view.answerExplanation.show()
			self.view.answerExplanationInput.show()
			self.view.addRowButton.show()
			try: self.view.addRowButton.disconnect()
			except Exception: pass
			self.view.addRowButton.clicked.connect(self.addRowTXT)
		elif text == 'Ranking By Order':
			self.view.table.setRowCount(0)
			self.view.answer_here.show()
			self.view.table.show()
			self.view.answerExplanation.show()
			self.view.answerExplanationInput.show()
			self.view.addRowButton.show()
			try: self.view.addRowButton.disconnect()
			except Exception: pass
			self.view.addRowButton.clicked.connect(self.addRowORD)
		elif text == 'Numeric':
			self.view.table.setRowCount(0)
			self.view.answer_here.show()
			self.view.table.show()
			self.view.answerExplanation.show()
			self.view.answerExplanationInput.show()
			self.view.addRowButton.hide()
			try: self.view.addRowButton.disconnect()
			except Exception: pass
			self.addRowNUM()
		elif text == 'Rating':
			self.view.table.setRowCount(0)
			self.view.answer_here.hide()
			self.view.table.hide()
			self.view.answerExplanation.hide()
			self.view.answerExplanationInput.hide()
			self.view.addRowButton.hide()
		elif text == 'XY Plot':
			self.view.table.setRowCount(0)
			self.view.answer_here.show()
			self.view.table.show()
			self.view.addRowButton.show()
			try: self.view.addRowButton.disconnect()
			except Exception: pass
			self.view.addRowButton.clicked.connect(self.addRowTXT)
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

		elif text == 'Pin on Image':
			self.view.table.hide()
			self.view.addRowButton.hide()
			try: self.view.addRowButton.disconnect()
			except Exception: pass



	def addRowMCQ(self):
		self.view.table.showColumn(1)
		self.view.table.hideColumn(3)
		row = self.view.table.rowCount()
		self.view.table.insertRow(row)
		chkBoxItem = qtw.QTableWidgetItem()
		chkBoxItem.setFlags(qtc.Qt.ItemIsUserCheckable | qtc.Qt.ItemIsEnabled)
		chkBoxItem.setCheckState(qtc.Qt.Unchecked)       
		self.view.table.setItem(row,1,chkBoxItem)

		self.deleteAnswerButton = qtw.QTableWidgetItem()
		self.deleteAnswerButton = qtw.QPushButton("Delete")
		self.deleteAnswerButton.clicked.connect(self.deleteAnswer)
		self.table.setCellWidget(row,2,self.deleteAnswerButton)

	def addRowTXT(self):
		self.view.table.hideColumn(1)
		self.view.table.hideColumn(3)
		row = self.view.table.rowCount()
		self.view.table.insertRow(row)
		
		self.deleteAnswerButton = qtw.QTableWidgetItem()
		self.deleteAnswerButton = qtw.QPushButton("Delete")
		self.deleteAnswerButton.clicked.connect(self.deleteAnswer)
		self.table.setCellWidget(row,2,self.deleteAnswerButton)

	def addRowORD(self):
		self.view.table.hideColumn(1)
		self.view.table.showColumn(3)
		row = self.view.table.rowCount()
		self.view.table.insertRow(row)
		self.rank_boxes = []
		for i in range(self.view.table.rowCount()):
			rank_box = qtw.QComboBox()
			rank_box.addItems([str(j+1) for j in range(self.view.table.rowCount())])
			self.view.table.setCellWidget(i, 2, rank_box)
			self.rank_boxes.append(rank_box)

		#row = self.table.rowCount()
		#self.table.setRowCount(row + 1)

		# Create a rank dropdown menu for the new row
		row_count_options = [str(i+1) for i in range(row+1)]
		self.rank_box = qtw.QComboBox()
		self.rank_box.addItems(row_count_options)
		self.table.setCellWidget(row, 2, self.rank_box)
		self.rank_boxes.append(self.rank_box)
		

		# Update the items in the existing dropdown menus
		for box in self.rank_boxes:
			box.clear()
			box.addItems([str(i+1) for i in range(self.view.table.rowCount())])
			

		self.deleteAnswerButton = qtw.QTableWidgetItem()
		self.deleteAnswerButton = qtw.QPushButton("Delete")
		self.deleteAnswerButton.clicked.connect(self.deleteAnswer)
		self.view.table.setCellWidget(row,3,self.deleteAnswerButton)

	def addRowNUM(self):
		self.view.table.hideColumn(1)
		self.view.table.hideColumn(3)
		self.view.table.setRowCount(5)
		self.minLabel = qtw.QTableWidgetItem()
		self.minLabel = qtw.QLabel("Minimum Value")
		self.view.table.setCellWidget(0,0,self.minLabel)

		self.maxLabel = qtw.QTableWidgetItem()
		self.maxLabel = qtw.QLabel("Maximum Value")
		self.view.table.setCellWidget(1,0,self.maxLabel)

		self.decimalPlaces = qtw.QTableWidgetItem()
		self.decimalPlaces = qtw.QLabel("Decimal Places")
		self.view.table.setCellWidget(2,0,self.decimalPlaces)

		self.correctAnswer = qtw.QTableWidgetItem()
		self.correctAnswer = qtw.QLabel("Correct Answer")
		self.view.table.setCellWidget(3,0,self.correctAnswer)

		self.errorMargin = qtw.QTableWidgetItem()
		self.errorMargin = qtw.QLabel("Error Margin")
		self.view.table.setCellWidget(4,0,self.errorMargin)


	def deleteAnswer(self):
		button = self.sender()
		if button:
			row = self.view.table.indexAt(button.pos()).row()
			self.view.table.removeRow(row)
			

	def getfile(self):
		fname, _ = qtw.QFileDialog.getOpenFileName(
			self, 'Open file', 'c:\\', "Image files (*.jpg *.gif *.png)")
		self.view.image_label.setPixmap(qtg.QPixmap(fname))
		#self.image_label.scaled(300, 300)
		print(os.path.basename(fname))
		

	def getfiles(self):
		os.chdir("resources")
		self.view.randint = str(random.randint(1000000,3000000))
		self.pixmap = self.view.image_label.pixmap()
		self.pixmap.save(self.randint + ".png")
		os.chdir("..")
		print(self.randint)

	def deleteQuestion(self):
		selected_row = self.view.questionBank.currentRow()
		self.view.questionBank.takeItem(selected_row)
		self.view.polls.pop(selected_row)
			

	def createQuestion(self):
		i = 0
		for i in range(self.view.table.rowCount()):
			if self.view.q_typeBox.currentText() == 'MultipleChoice':
				self.view.answers.append(self.view.table.item(i,0).text())
				if self.view.table.item(i,1).checkState() == 2:
					self.view.check.append(True)
					print("True")
				if self.view.table.item(i,1).checkState() == 0:
					self.view.check.append(False)
					print("False")

			if self.view.q_typeBox.currentText() == 'XY Plot':
				try: self.view.answers.append(self.view.table.item(i,0).text())
				except Exception: pass
			if self.view.q_typeBox.currentText() == 'Ranking By Preference' or self.q_typeBox.currentText() == 'Text Question':
				self.view.answers.append(self.view.table.item(i,0).text())
			if  self.view.q_typeBox.currentText() == 'Ranking By Order':
				self.view.answers.append(self.view.table.item(i,0).text())
				orderId = self.view.table.cellWidget(i, 2)
				self.view.rank.append(orderId.currentText())

			i=i+1
		print(i)

		print(len(self.view.answers))
		print(self.view.answers)
		print(self.view.check)
		print(self.view.rank)

		if self.view.image_label.pixmap() != None:
			self.getfiles()

		
		question = {}
		question.clear()
		if self.view.q_typeBox.currentText() == 'MultipleChoice':
			question['@type'] = "MultipleChoiceQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
			if self.view.randint != None:
				question['image'] = self.view.randint
			else:
				question['image'] = None
			question['choices'] = []
			x=0
			for x in range(len(self.view.answers)):
				question['choices'].append({"id": random.randint(1000000,3000000), "alias": None, "text": self.view.answers[x], "isCorrectAnswer": self.view.check[x], "excludeFromResults": False, "image": None})
				x= x+1
			question['minNumberSelections'] = 1
			question['maxNumberSelections'] = 2
			question['resultFormat'] = "%"
			question['distributableWeight'] = None
			question['weightingSetting'] = None
			question['weightingFactor'] = None
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()
			
		if self.view.q_typeBox.currentText() == 'Word Cloud':
			question['@type'] = "OpenTextQuestion"
			question['wordCloudQuestion'] = True
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
			if self.view.randint != None:
				question['image'] = self.view.randint
			else:
				question['image'] = None
			question['maxLength'] = 2000
			question['maxWords'] = 150
			question['resultFormat'] = "WORD_CLOUD"
			question['maxWordCount'] = None
			question['maxWordLength'] = None
			question['correctAnswers'] = []
			x=0
			for x in range(len(self.view.answers)):
				question['correctAnswers'].append({"text": self.view.answers[x]})
				x= x+1
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

		if self.view.q_typeBox.currentText() == 'Text Question':
			question['@type'] = "OpenTextQuestion"
			question['wordCloudQuestion'] = False
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
			if self.view.randint != None:
				question['image'] = self.view.randint
			else:
				question['image'] = None
			question['maxLength'] = 2000
			question['maxWords'] = 150
			question['resultFormat'] = "RESPONSE_LIST"
			question['maxWordCount'] = None
			question['maxWordLength'] = None
			question['correctAnswers'] = []
			x=0
			for x in range(len(self.view.answers)):
				#self.answers.append(self.table.item(x,0).text())
				question['correctAnswers'].append(self.view.answers[x])
				x= x+1
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

		if self.view.q_typeBox.currentText() == 'Ranking By Preference':
			question['@type'] = "RankingQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
			question['uiType'] = "ranking"
			if self.view.randint != None:
				question['image'] = self.view.randint
			else:
				question['image'] = None
			question['choices'] = []
			x=0
			for x in range(len(self.view.answers)):
				question['choices'].append({"id": random.randint(1000000,3000000), "sequence": x, "alias": None, "text": self.view.answers[x], "image": None})
				x= x+1
			question['minNumberSelections'] = 1
			question['maxNumberSelections'] = 2
			choices = []
			question['correctAnswer'] = choices
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

		if self.view.q_typeBox.currentText() == 'Ranking By Order':
			question['@type'] = "RankingQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
			question['uiType'] = "ordering"
			if self.view.randint != None:
				question['image'] = self.view.randint
			else:
				question['image'] = None
			choices = []
			question['choices'] = []
			x=0
			
			for x in range(len(self.view.answers)):
				rankId = random.randint(1000000,3000000)
				question['choices'].append({"id": rankId, "sequence": x, "alias": None, "text": self.view.answers[x], "image": None})
				choices.append({"choiceId": rankId, "rank": self.view.rank[x]})
				x=x+1
			question['minNumberSelections'] = 1
			question['maxNumberSelections'] = 2
			question['correctAnswer'] = choices
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

		if self.view.q_typeBox.currentText() == 'Numeric':
			question['@type'] = "NumericQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
			if self.view.randint != None:
				question['image'] = self.view.randint
			else:
				question['image'] = None
			question['uiType'] = "inputfield"
			question['resultFormat'] = "%"
			question['min'] = self.view.table.item(0,2).text()
			question['max'] = self.view.table.item(1,2).text()
			question['minLabel'] = ""
			question['maxLabel'] = ""
			correctAnswer = None
			errorMargin = None
			if self.view.table.item(3,2) != None or self.view.table.item(3,2) != None:
				correctAnswer = float(self.view.table.item(3,2).text())
				errorMargin = float(self.view.table.item(4,2).text())				
				question['correctAnswers'] = {"min" : round(correctAnswer - errorMargin, int(self.view.table.item(2,2).text())), "max" : round(correctAnswer + errorMargin, int(self.view.table.item(2,2).text()))}
			else:
				question['correctAnswers'] = []
			question['numberOfDecimals'] = self.view.table.item(2,2).text()
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

		if self.view.q_typeBox.currentText() == 'Rating':
			question['@type'] = "NumericQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
			if self.view.randint != None:
				question['image'] = self.view.randint
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

		if self.view.q_typeBox.currentText() == 'XY Plot':
			question['@type'] = "ScatterPlotQuestion"
			question['lowerCaseAlias'] = ""
			question['id'] = random.randint(1000000,3000000)
			question['alias'] = ""
			question['text'] = self.view.questionInput.text()
			if self.view.randint != None:
				question['image'] = self.view.randint
			else:
				question['image'] = None
			question['xText'] = self.view.table.item(0,2).text()
			question['yText'] = self.view.table.item(1,2).text()
			question['minX'] = 0
			question['maxX'] = self.view.table.item(2,2).text()
			question['minY'] = 0
			question['maxY'] = self.view.table.item(3,2).text()
			question['items'] = []
			for x in range(len(self.view.answers)):
				rankId = random.randint(1000000,3000000)
				question['items'].append({"id": rankId, "alias": None, "sequence": x, "text": self.view.answers[x]})

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
			question['options'] = []
			question['maxNumberSelections'] = 1
			question['correctAnswerExplanation'] = self.answerExplanationInput.text()

		self.view.polls.append(question)
		self.view.questionBank.addItem(question['text'])
		self.view.answers.clear()
		self.view.check.clear()
		self.view.table.clear()
		self.view.questionInput.clear()
		self.view.answerExplanationInput.clear()
		self.view.image_label.clear()
		self.showhide(self.view.q_typeBox.currentText())
		self.view.randint = None
		print(self.view.polls)
		

	def createpoll(self):
		json_object = json.dumps(self.view.polls)

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


