import random
import uuid
import os
from abc import ABC, abstractmethod


class BaseQuestion(ABC):
    def __init__(self, view):
        self.view = view
        self.answers = []
        self.randint = None
        self.saveImage() if self.view.image_label.pixmap() is not None else None

    @abstractmethod
    def create_question(self):
        pass

    def saveImage(self):
        os.chdir("resources")
        self.randint = str(uuid.uuid4())
        self.pixmap = self.view.image_label.pixmap()
        self.pixmap.save(self.randint + ".png")
        os.chdir("..")
        print(self.randint)


class MultipleChoiceQuestion(BaseQuestion):
    def __init__(self, view):
        super().__init__(view)
        self.check = []

    def create_question(self):
        for row in range(self.view.table.rowCount()):
            self.answers.append(self.view.table.item(row, 0).text())
            if self.view.table.item(row, 1).checkState() == 2:
                self.check.append(True)
            if self.view.table.item(row, 1).checkState() == 0:
                self.check.append(False)

        # Implement the MultipleChoice question type specific details here
        question = {
            "@type": "MultipleChoiceQuestion",
            "lowerCaseAlias" : "",
			"id" : random.randint(1000000,10000000),
			"alias" : "",
			"text" : self.view.questionInput.text(),
            "image" : self.randint if self.randint is not None else None,
            "choices": self.populateMCQChoices(),
            "minNumberSelections" : 0,
            "maxNumberSelections": self.view.maxNumberOfSelectionsInput.text(),
            "resultFormat": "%",
            "weightingSetting": None,
            "weightingFactor": None,
            "correctAnswerExplanation": self.view.answerExplanationInput.text()
        }

        return question
    
    def populateMCQChoices(self):
        choices = []
        for x in range(len(self.answers)):
            choice = {
                "id": random.randint(1000000,10000000),
                "alias": None, "text": self.answers[x], 
                "isCorrectAnswer": self.check[x], 
                "excludeFromResults": False, 
                "image": None
            }
            choices.append(choice)

        return choices

class WordCloudQuestion(BaseQuestion):
    def __init__(self, view):
        super().__init__(view)

    def create_question(self):
        # Implement the WordCloud question type specific details here
        question = {
            "@type": "OpenTextQuestion",
            "wordCloudQuestion": True,
            "lowerCaseAlias" : "",
			"id" : random.randint(1000000,10000000),
			"alias" : "",
			"text" : self.view.questionInput.text(),
            "image" : self.randint if self.randint is not None else None,
            "maxLength": 2000,
			"maxWords": 150,
			"resultFormat": "WORD_CLOUD",
			"maxWordCount": None,
			"maxWordLength": None,
			'correctAnswers': [],
            "correctAnswerExplanation": None
        }

        return question


class TextQuestion(BaseQuestion):
    def __init__(self, view):
        super().__init__(view)

    def create_question(self):
        for row in range(self.view.table.rowCount()):
            self.answers.append(self.view.table.item(row, 0).text())

        # Implement the TextQuestion question type specific details here
        question = {
            "@type": "OpenTextQuestion",
            "wordCloudQuestion": False,
            "lowerCaseAlias" : "",
            "id" : random.randint(1000000,10000000),
            "alias" : "",
            "text": self.view.questionInput.text(),
            "image" : self.randint if self.randint is not None else None,
            "maxLength": 2000,
			"maxWords": 150,
			"resultFormat": "RESPONSE_LIST",
			"maxWordCount": None,
			"maxWordLength": None,
            "correctAnswers": self.answers,
            "correctAnswerExplanation": self.view.answerExplanationInput.text()
        }

        return question

class RankingByPreferenceQuestion(BaseQuestion):
    def __init__(self, view):
        super().__init__(view)

    def create_question(self):
        for i in range(self.view.table.rowCount()):
            self.answers.append(self.view.table.item(i, 0).text())


        # Implement the TextQuestion question type specific details here
        question = {
            "@type": "RankingQuestion",
            "lowerCaseAlias" : "",
            "id" : random.randint(1000000,10000000),
            "alias" : "",
            "text": self.view.questionInput.text(),
            "uiType": "ranking",
            "image" : self.randint if self.randint is not None else None,
            "choices": self.populatePreferenceChoices(),
            "minNumberSelections": 1,
			"maxNumberSelections": self.view.maxNumberOfSelectionsInput.text(),
            "correctAnswers": {"choices": ""},
            "correctAnswerExplanation": None
        }

        return question

    def populatePreferenceChoices(self):
        choices = []
        for x in range(len(self.answers)):
            choice = {
                "id": random.randint(1000000,10000000), 
                "sequence": x, "alias": None, 
                "text": self.answers[x], 
                "image": None
            }
            choices.append(choice)

        return choices

class RankingByOrderQuestion(BaseQuestion):
    def __init__(self, view):
        super().__init__(view)
        self.rankId = random.randint(1000000,10000000)
        self.rank = []

    def create_question(self):
        for row in range(self.view.table.rowCount()):
            self.answers.append(self.view.table.item(row,0).text())
            orderId = self.view.table.cellWidget(row, 2)
            self.rank.append(orderId.currentText())
        

        # Implement the TextQuestion question type specific details here
        question = {
            "@type": "RankingQuestion",
            "lowerCaseAlias" : "",
            "id" : random.randint(1000000,10000000),
            "alias" : "",
            "text": self.view.questionInput.text(),
            "uiType": "ordering",
            "image" : self.randint if self.randint is not None else None,
            "choices": self.populateRankingChoices(),
            "minNumberSelections": self.view.table.rowCount(),
			"maxNumberSelections": self.view.table.rowCount(),
            
            "correctAnswers": ({"choices" : self.correctChoices}),
            "correctAnswerExplanation": self.view.answerExplanationInput.text()
        }
        return question

    def populateRankingChoices(self):
        choices = []
        self.correctChoices = []
        for index in range(len(self.answers)):
            self.rankId = random.randint(1000000,10000000)
            choice = {
                "id": self.rankId,
                "sequence": index,
                "alias": None, 
                "text": self.answers[index], 
                "image": None
            }
            choices.append(choice)

            correctChoice = {
                "choiceId": self.rankId, 
                "rank": self.rank[index]
            }
            self.correctChoices.append(correctChoice)

        return choices


class NumericQuestion(BaseQuestion):
    def __init__(self, view):
        super().__init__(view)

    def create_question(self):

        # Implement the TextQuestion question type specific details here
        question = {
            "@type": "NumericQuestion",
            "lowerCaseAlias" : "",
            "id" : random.randint(1000000,10000000),
            "alias" : "",
            "text": self.view.questionInput.text(),
            "image" : self.randint if self.randint is not None else None,
            "uiType": "inputfield",
            "resultFormat": "%",
            "min": self.view.table.item(0,2).text(),
			"max": self.view.table.item(1,2).text(),
            "minLabel": "",
            "maxLabel": "",
            "correctAnswers": self.populateNumericAnswers(),
            "numberOfDecimals": self.view.table.item(2,2).text(),
            "correctAnswerExplanation": self.view.answerExplanationInput.text()
        }
        return question

    def populateNumericAnswers(self):
        correctAnswers = []
        if self.view.table.item(3,2) != None or self.view.table.item(3,2) != None:
            correctAnswer = float(self.view.table.item(3,2).text())
            errorMargin = float(self.view.table.item(4,2).text())
            correctAnswer = {
                "min" : round(correctAnswer - errorMargin, int(self.view.table.item(2,2).text())), 
                "max" : round(correctAnswer + errorMargin, int(self.view.table.item(2,2).text()))
                }
            correctAnswers.append(correctAnswer)

        return correctAnswers

class RatingQuestion(BaseQuestion):
    def __init__(self, view):
        super().__init__(view)

    def create_question(self):

        # Implement the TextQuestion question type specific details here
        question = {
            "@type": "NumericQuestion",
            "lowerCaseAlias" : "",
            "id" : random.randint(1000000,10000000),
            "alias" : "",
            "text": self.view.questionInput.text(),
            "image" : self.randint if self.randint is not None else None,
            "uiType": "rating",
            "resultFormat": "%",
            "min": 1,
			"max": 5,
            "minLabel": "",
            "maxLabel": "",
            "correctAnswers": [],
            "numberOfDecimals": 0
        }
        return question


class XYPlotQuestion(BaseQuestion):
    def __init__(self, view):
        super().__init__(view)

    def create_question(self):
        for row in range(self.view.table.rowCount()):
            try: self.answers.append(self.view.table.item(row,0).text())
            except Exception: pass
        # Implement the TextQuestion question type specific details here
        question = {
            "@type": "ScatterPlotQuestion",
            "lowerCaseAlias" : "",
            "id" : random.randint(1000000,10000000),
            "alias" : "",
            "text": self.view.questionInput.text(),
            "image" : self.randint if self.randint is not None else None,
            "xText": self.view.table.item(0,2).text(),
            "yText": self.view.table.item(1,2).text(),
            "minX": 0,
            "maxX": self.view.table.item(2,2).text(),
            "minY": 0,
            "maxY": self.view.table.item(3,2).text(),
            "items": self.populateItems()
        }
        return question

    def populateItems(self):
        items = []
        for x in range(len(self.answers)):
                rankId = random.randint(1000000,10000000)
                item = {
                    "id": rankId, 
                    "alias": None, 
                    "sequence": x, 
                    "text": self.answers[x]
                }
                items.append(item)
        return items


class ClickMapQuestion(BaseQuestion):
    def __init__(self, view, pinOnImageWindow):
        super().__init__(view)
        self.pinOnImageWindow = pinOnImageWindow

    def create_question(self):
        for row in range(self.view.table.rowCount()):
            try: self.answers.append(self.view.table.item(row,0).text())
            except Exception: pass
        # Implement the TextQuestion question type specific details here
        question = {
            "@type": "ClickMapQuestion",
            "lowerCaseAlias" : "",
            "id" : random.randint(1000000,10000000),
            "alias" : "",
            "text": self.view.questionInput.text(),
            "image" : self.randint if self.randint is not None else None,
            "options": [],
            "maxNumberSelections": 0,
            "correctAnswers": self.pinOnImageWindow.correctItems,
            "correctAnswerExplanation": self.view.answerExplanationInput.text(),
        }
        return question

class QuestionFactory:
    @staticmethod
    def create_question(view, pinOnImageWindow = None):
        question_type = view.questionTypeBox.currentText()
        if question_type == "MultipleChoice":
            return MultipleChoiceQuestion(view)
        elif question_type == "Word Cloud":
            return WordCloudQuestion(view)
        elif question_type == "Text Question":
            return TextQuestion(view)
        elif question_type == "Ranking By Preference":
            return RankingByPreferenceQuestion(view)
        elif question_type == "Ranking By Order":
            return RankingByOrderQuestion(view)
        elif question_type == "Numeric":
            return NumericQuestion(view)
        elif question_type == "Rating":
            return RatingQuestion(view)
        elif question_type == "XY Plot":
            return XYPlotQuestion(view)
        elif question_type == "Pin on Image":
            return ClickMapQuestion(view, pinOnImageWindow)
        else:
            raise ValueError(f"Invalid question type: {question_type}")


class QuestionHandler:
    def __init__(self, view, pinOnImageWindow=None):
        self.view = view
        self.pinOnImageWindow = pinOnImageWindow

    def create_question(self):

        question_obj = QuestionFactory.create_question(self.view, self.pinOnImageWindow)
        question = question_obj.create_question()
        return question
      

