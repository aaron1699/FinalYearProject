import random

class createQuestion:
	def __init__(self, view):
		self.view = view
		self.answers = []
		self.check = []
		self.randint = None
		self.polls = []
		self.rank = []
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
			question['correctAnswers'] = self.view.correctItems
			question['correctAnswerExplanation'] = self.view.answerExplanationInput.text()

