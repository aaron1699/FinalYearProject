import sys 
import json
import zipfile
import pdfkit
import os
from os import listdir
from os.path import isfile, join
import re
import shutil
import PyQt5.QtWidgets as qtw
import cv2
from PyQt5.QtWidgets import QInputDialog, QWidget

class PDFgenerator():
    def __init__(self):
        self.maxHeight = 0
        self.maxWidth = 0
        self.poll_data = None

    def run(self):
        try:
            filename, _ = qtw.QFileDialog.getOpenFileName(None, "Select a zip file", ".", "Zip files (*.zip)")

            path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
            self.config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

            zfile = zipfile.ZipFile(filename)

            for file in zfile.namelist():
                zfile.extract(file)


            poll_file = zfile.open('polls.json')

            self.poll_data = json.load(poll_file)
        except Exception as e:
        # display an error message box with the error message
            msg_box = qtw.QMessageBox()
            msg_box.setIcon(qtw.QMessageBox.Critical)
            msg_box.setText("An error has occurred")
            msg_box.setInformativeText(str(e))
            msg_box.setWindowTitle("Error")
            msg_box.setWindowModality(False)
            msg_box.exec_()

        
        print(self.poll_data)
    
    
 
    def renameImages(self):
        if self.poll_data != None:
            #remove suffix from image names
            file_list = [f for f in listdir('resources/') if isfile(join('resources', f))]
            self.image_directory = 'resources/'
            print(file_list)
            self.new_list = [re.sub(r'\s*\.\d+\.', '.', x) for x in file_list]

            i = 0
            while i != len(self.new_list):
                os.rename(self.image_directory + file_list[i], self.image_directory + self.new_list[i])
                i = i + 1
        


    def setMaxImageSize(self):
    # set max image height and width
        if self.poll_data != None:
            window = QWidget()
            height = QInputDialog.getInt(window, "Image size", "Enter maximum image height:")
            width = QInputDialog.getInt(window, "Image size", "Enter maximum image width:")
            self.maxWidth = width[0]
            self.maxHeight = height[0]
            window.show()
            window.hide()
        
            print(self.maxHeight)
            print(self.maxWidth)


    def findImage(self, name):
        if name.get('image'):
            for s in self.new_list:
                if name['image'] in s:
                    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", s)
        return ""


    def draw_ovals_on_image(self, image_path, ovals, image_name):

        image = cv2.imread(image_path)

        # Iterate through the ovals and draw each one on the image
        for oval in ovals:
            x = int(oval["x"] * image.shape[1])
            y = int(oval["y"] * image.shape[0])
            x_radius = int(oval["xRadius"] * image.shape[1])
            y_radius = int(oval["yRadius"] * image.shape[0])
            color = (0, 0, 255) 
            thickness = 2

            cv2.ellipse(image, (x, y), (x_radius, y_radius), 0, 0, 360, color, thickness)

        cv2.imwrite(image_name, image)


    class MultipleChoiceQuestion:
        def __init__(self, question, question_number, findImage, maxWidth, maxHeight):
            self.question = question
            self.question_number = question_number
            self.findImage = findImage
            self.maxWidth = maxWidth
            self.maxHeight = maxHeight
            

        def to_html(self):

            html = f"<h2>{self.question_number + 1}) {self.question['text']}</h2>"
            question_image = self.findImage(self.question)
            if self.question['image'] != None:
                html += f'<img src="{question_image}" style="max-width:{self.maxWidth}px;max-height:{self.maxHeight}px;"/>'

            for choices in self.question['choices']:
                    print(choices['text'], choices['isCorrectAnswer'])
                    tickOrCross = '&#10003;' if choices['isCorrectAnswer'] else '&#10007;'  # Unicode characters for tick and cross
                    color = 'green' if choices['isCorrectAnswer'] else 'red'
                    html += f'<p>{choices["text"]} <span style="color:{color};">{tickOrCross}</span></p>'
                    choices_image = self.findImage(choices)
                    if choices['image'] != None:
                        html += f'<img src="{choices_image}" style="max-width:{self.maxWidth}px;max-height:{self.maxHeight}px;"/>'
            if self.question['correctAnswerExplanation'] != None:
                    html += f"<p>{self.question['correctAnswerExplanation']}</p>"

            return html

    class RankingQuestion:
        def __init__(self, question, question_number, findImage, maxWidth, maxHeight):
            self.question = question
            self.question_number = question_number
            self.findImage = findImage
            self.maxWidth = maxWidth
            self.maxHeight = maxHeight

        def to_html(self):

            html = f"<h2>{self.question_number + 1}) {self.question['text']}</h2>"
            question_image = self.findImage(self.question)
            if self.question['image'] != None:
                html += f'<img src="{question_image}" style="max-width:{self.maxWidth}px;max-height:{self.maxHeight}px;"/>'

            for choices in self.question['choices']:
                html += f"<p>Rank: {choices['sequence'] + 1} <br> {choices['text']}</p>"
                choices_image = self.findImage(choices)
                if choices['image'] != None:
                    html += f'<img src="{choices_image}" style="max-width:{self.maxWidth}px;max-height:{self.maxHeight}px;"/>'

            return html

    class ClickMapQuestion:
        def __init__(self, question, question_number, findImage, maxWidth, maxHeight, draw_ovals_on_image):
            self.question = question
            self.question_number = question_number
            self.findImage = findImage
            self.maxWidth = maxWidth
            self.maxHeight = maxHeight
            self.draw_ovals_on_image = draw_ovals_on_image

        def to_html(self):

            html = f"<h2>{self.question_number + 1}) {self.question['text']}</h2>"
            correctAnswers = []
            correctAnswers = self.question['correctAnswers']
            question_image = self.findImage(self.question)
            if self.question['image'] != None:
                if bool(self.question['correctAnswers']):
                    print(self.question['correctAnswers'])
                    self.draw_ovals_on_image(question_image, correctAnswers, question_image)
                    html += f'<img src="{question_image}" style="page-break-inside: avoid;max-width:{self.maxWidth}px;max-height:{self.maxHeight}px;"/>'
                else:
                    html += f'<img src="{question_image}" style="page-break-inside: avoid; max-width:{self.maxWidth}px;max-height:{self.maxHeight}px;"/>'
                
                
            if len(self.question['options']) != 0:    
                html += f"<p>{self.question['options']}</p>"

            if self.question['correctAnswerExplanation'] != 0:
                html += f"<p>{self.question['correctAnswerExplanation']}</p>"

            html += f'<div style="height: 100px; padding:20px 0px 0px 0px;" <br>'

            return html

    class OpenTextQuestion:
        def __init__(self, question, question_number, findImage, maxWidth, maxHeight):
            self.question = question
            self.question_number = question_number
            self.findImage = findImage
            self.maxWidth = maxWidth
            self.maxHeight = maxHeight

        def to_html(self):

            html = f"<h2>{self.question_number + 1}) {self.question['text']}</h2>"
            question_image = self.findImage(self.question)
            if self.question['image'] != None:
                html += f'<img src="{question_image}" style="max-width:{self.maxWidth}px;max-height:{self.maxHeight}px;"/>'

            for answers in self.question['correctAnswers']:
                tickOrCross = '&#10003;' 
                color = 'green'
                html += f'<p>{answers} <span style="color:{color};">{tickOrCross}</span></p>'
            if self.question['correctAnswerExplanation'] != None:
                    html += f"<p>{self.question['correctAnswerExplanation']}</p>"

            return html

    class NumericQuestion:
        def __init__(self, question, question_number, findImage, maxWidth, maxHeight):
            self.question = question
            self.question_number = question_number
            self.findImage = findImage
            self.maxWidth = maxWidth
            self.maxHeight = maxHeight

        def to_html(self):

            html = f"<h2>{self.question_number + 1}) {self.question['text']}</h2>"
            question_image = self.findImage(self.question)
            if self.question['image'] != None:
                html += f'<img src="{question_image}" style="max-width:{self.maxWidth}px;max-height:{self.maxHeight}px;"/>'

            for answers in self.question['correctAnswers']:
                html += f"<p>Min: {answers['min']} <br> Max: {answers['max']}</p>"
            if self.question['correctAnswerExplanation'] != None:
                    html += f"<p>{self.question['correctAnswerExplanation']}</p>"

            return html

    class ScatterPlotQuestion:
        def __init__(self, question, question_number, findImage, maxWidth, maxHeight):
            self.question = question
            self.question_number = question_number
            self.findImage = findImage
            self.maxWidth = maxWidth
            self.maxHeight = maxHeight

        def to_html(self):

            question_maxX = self.question['maxX']
            question_maxY = self.question['maxY']
            question_xText = self.question['xText']
            question_yText = self.question['yText']
            question_items = self.question['items']
            html = f"<h2>{self.question_number + 1}) {self.question['text']}</h2>"
            question_image = self.findImage(self.question)
            if self.question['image'] != None:
                html += f'<img src="{question_image}" style="max-width:{self.maxWidth}px;max-height:{self.maxHeight}px;"/>'


            html += f'<div style="height: 200px; padding:400px 0px 0px 0px;" <br>'
            html += f'<div style="position: fixed; left:30px; height: 400px; width:3px; background:black; page-break-inside: avoid;" />'
            html += f'<h4 style="position: relative; left:-30px; bottom: 20px;">{question_maxY}</h4>'
            html += f'<h4 style="position: relative; left:-15px; top:150px; -webkit-transform: rotate(270deg); white-space:nowrap;">{question_yText}</h4>'
            html += f'<div style="position: relative; left:1px; top:295px; height: 3px; width:700px; background:black;" />'
            html += f'<h4 style="position: relative; left:680px; top:10px;">{question_maxX}</h4>'
            html += f'<h4 style="position: relative; left:350px; bottom:20px;">{question_xText}</h4>'
            html += f'<div style="height: 100px; padding:20px 0px 0px 0px;" <br>'
            for item in question_items:
                html += f"<h3>{item['text']}</h3>"
            html += f'<div style="height: 100px; padding:20px 0px 0px 0px;" <br>'
            html += f'<div style="page-break-inside: avoid;">'
            html += f'</div></div>'
            return html


    def generatePDF(self):
        if self.poll_data != None:

            html = ''
     
            for question_number, question in enumerate(self.poll_data):

                if question['@type'] == "MultipleChoiceQuestion":
                    MCQ_question = self.MultipleChoiceQuestion(question, question_number, self.findImage, self.maxWidth, self.maxHeight)
                    html += MCQ_question.to_html()

                if question['@type'] == "ClickMapQuestion":
                    ClickMap_question = self.ClickMapQuestion(question, question_number, self.findImage, self.maxWidth, self.maxHeight, self.draw_ovals_on_image)
                    html += ClickMap_question.to_html()

                if question['@type'] == "OpenTextQuestion":
                    OpenText_question = self.OpenTextQuestion(question, question_number, self.findImage, self.maxWidth, self.maxHeight)
                    html += OpenText_question.to_html()

                if question['@type'] == "RankingQuestion":
                    Ranking_question = self.RankingQuestion(question, question_number, self.findImage, self.maxWidth, self.maxHeight)
                    html += Ranking_question.to_html()

                if question['@type'] == "NumericQuestion":
                    Numeric_question = self.NumericQuestion(question, question_number, self.findImage, self.maxWidth, self.maxHeight)
                    html += Numeric_question.to_html()

                if question['@type'] == "ScatterPlotQuestion":
                    ScatterPlot_question = self.ScatterPlotQuestion(question, question_number, self.findImage, self.maxWidth, self.maxHeight)
                    html += ScatterPlot_question.to_html()

                html += f'<div style="height: 3px; width:100%; background:black; padding: 20px white;" />'
                html += f'<div style="height: 20px; width:100%; position: relative; top: 20px" />'
            html += f'<div style="width: 100%; height: 100vh; background-color: white;"></div>'

            msgBox = qtw.QMessageBox(qtw.QMessageBox.NoIcon, "Generator", "PDF Generated!", qtw.QMessageBox.Ok, parent=None)
            msgBox.exec_()

            savefilename, _ = qtw.QFileDialog.getSaveFileName(None, "Save PDF file", ".", "PDF files (*.pdf)")
            
            try:
                pdfkit.from_string(html, savefilename, configuration=self.config, options={"enable-local-file-access": ""})
            except Exception as e:
            # display an error message box with the error message
                msg_box = qtw.QMessageBox()
                msg_box.setIcon(qtw.QMessageBox.Critical)
                msg_box.setText("An error has occurred")
                msg_box.setInformativeText(str(e))
                msg_box.setWindowTitle("Error")
                msg_box.setWindowModality(False)
                msg_box.exec_()
                return

            shutil.rmtree(self.image_directory)

    def main():
        pdf_generator = PDFgenerator()
        pdf_generator.run()
        pdf_generator.renameImages()
        pdf_generator.setMaxImageSize()
        pdf_generator.generatePDF()
        

