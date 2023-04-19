from cgitb import html
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

global maxHeight
global maxWidth

def generator():
    try:
        filename, _ = qtw.QFileDialog.getOpenFileName(None, "Select a zip file", ".", "Zip files (*.zip)")

        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


            

        print("This is the name of the script ", sys.argv[0])

        #filepath = r"C:\Users\Aaron\source\repos\FinalYearProject\VevoxPDFGenerator\poll_week6_v2.zip"
        zfile = zipfile.ZipFile(filename)

        for file in zfile.namelist():
            zfile.extract(file)


        poll_file = zfile.open('polls.json')
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
    
    
    

    window = QWidget()
    height = QInputDialog.getInt(window, "Image size", "Enter maximum height:")
    width = QInputDialog.getInt(window, "Image size", "Enter maximum width:")
    maxWidth = width[0]
    maxHeight = height[0]
    window.show()
    window.hide()
    
    poll_data = json.load(poll_file)

    file_list = [f for f in listdir('resources/') if isfile(join('resources', f))]
    image_directory = 'resources/'
    #files = os.listdir(directory)
    print(file_list)
    new_list = [re.sub(r'\s*\.\d+\.', '.', x) for x in file_list]
    print(new_list)

    i = 0
    while i != len(new_list):
        os.rename(image_directory + file_list[i], image_directory + new_list[i])
        i = i + 1

    print(new_list)
    print(maxHeight)
    print(maxWidth)


    def findImage(name):
        if name.get('image'):
            for s in new_list:
                if name['image'] in s:
                    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", s)
        return ""

    #def findImage(name):
    #        imagestring = ''
    #        if name['image'] != None and any(name['image'] in s for s in new_list):
    #            matching = [s for s in new_list if name['image'] in s]
    #            imagestring = os.path.dirname(os.path.abspath(__file__)) + "\\resources\\" + str(matching[0])
    #        return imagestring

    def draw_ovals_on_image(image_path, ovals, image_name):
        # Load the image
        image = cv2.imread(image_path)

        # Iterate through the ovals and draw each one on the image
        for oval in ovals:
            x = int(oval["x"] * image.shape[1])
            y = int(oval["y"] * image.shape[0])
            x_radius = int(oval["xRadius"] * image.shape[1])
            y_radius = int(oval["yRadius"] * image.shape[0])
            color = (0, 0, 255)  # BGR color for red
            thickness = 2

            cv2.ellipse(image, (x, y), (x_radius, y_radius), 0, 0, 360, color, thickness)

        cv2.imwrite(image_name, image)

   

    class MultipleChoiceQuestion:
        def __init__(self, question):
            self.question = question
            

        def to_html(self):

            html = f"<h2>{question_number + 1}) {self.question['text']}</h2>"
            question_image = findImage(self.question)
            if self.question['image'] != None:
                html += f'<img src="{question_image}" style="max-width:{maxWidth}px;max-height:{maxHeight}px;"/>'

            for choices in self.question['choices']:
                    print(choices['text'], choices['isCorrectAnswer'])
                    tickOrCross = '&#10003;' if choices['isCorrectAnswer'] else '&#10007;'  # Unicode characters for tick and cross
                    color = 'green' if choices['isCorrectAnswer'] else 'red'
                    html += f'<p>{choices["text"]} <span style="color:{color};">{tickOrCross}</span></p>'
                    choices_image = findImage(choices)
                    if choices['image'] != None:
                        html += f'<img src="{choices_image}" style="max-width:{maxWidth}px;max-height:{maxHeight}px;"/>'
            if question['correctAnswerExplanation'] != None:
                    html += f"<p>{question['correctAnswerExplanation']}</p>"

            return html

    class RankingQuestion:
        def __init__(self, question):
            self.question = question

        def to_html(self):

            html = f"<h2>{question_number + 1}) {self.question['text']}</h2>"
            question_image = findImage(self.question)
            if self.question['image'] != None:
                html += f'<img src="{question_image}" style="max-width:{maxWidth}px;max-height:{maxHeight}px;"/>'

            for choices in self.question['choices']:
                html += f"<p>Rank: {choices['sequence'] + 1} <br> {choices['text']}</p>"
                choices_image = findImage(choices)
                if choices['image'] != None:
                    html += f'<img src="{choices_image}" style="max-width:{maxWidth}px;max-height:{maxHeight}px;"/>'

            return html

    class ClickMapQuestion:
        def __init__(self, question):
            self.question = question

        def to_html(self):

            html = f"<h2>{question_number + 1}) {self.question['text']}</h2>"
            question_image = findImage(self.question)
            if self.question['image'] != None:
                html += f'<img src="{question_image}" style="max-width:{maxWidth}px;max-height:{maxHeight}px;"/>'
                if bool(question["correctAnswers"]):
                    draw_ovals_on_image(question_image, question['correctAnswers'], question_image)
                    html += f'<img src="{question_image}" style="max-width:{maxWidth}px;max-height:{maxHeight}px;"/>'
                
                
            if len(question['options']) != 0:    
                    html += f"<p>{question['options']}</p>"
            #if len(question['correctAnswers']) != 0:
            #        html += f"<p>{question['correctAnswers']}</p>"
            if question['correctAnswerExplanation'] != None:
                    html += f"<p>{question['correctAnswerExplanation']}</p>"

            return html

    class OpenTextQuestion:
        def __init__(self, question):
            self.question = question

        def to_html(self):

            html = f"<h2>{question_number + 1}) {self.question['text']}</h2>"
            question_image = findImage(self.question)
            if self.question['image'] != None:
                html += f'<img src="{question_image}" style="max-width:{maxWidth}px;max-height:{maxHeight}px;"/>'

            for answers in self.question['correctAnswers']:
                tickOrCross = '&#10003;'  # Unicode characters for tick and cross
                color = 'green'
                html += f'<p>{answers} <span style="color:{color};">{tickOrCross}</span></p>'
            if question['correctAnswerExplanation'] != None:
                    html += f"<p>{question['correctAnswerExplanation']}</p>"

            return html

    class NumericQuestion:
        def __init__(self, question):
            self.question = question

        def to_html(self):

            html = f"<h2>{question_number + 1}) {self.question['text']}</h2>"
            question_image = findImage(self.question)
            if self.question['image'] != None:
                html += f'<img src="{question_image}" style="max-width:{maxWidth}px;max-height:{maxHeight}px;"/>'

            for answers in self.question['correctAnswers']:
                html += f"<p>Min: {answers['min']} <br> Max: {answers['max']}</p>"
            if question['correctAnswerExplanation'] != None:
                    html += f"<p>{question['correctAnswerExplanation']}</p>"

            return html

    class ScatterPlotQuestion:
        def __init__(self, question):
            self.question = question

        def to_html(self):

            question_maxX = question['maxX']
            question_maxY = question['maxY']
            question_xText = question['xText']
            question_yText = question['yText']
            html = f"<h2>{question_number + 1}) {self.question['text']}</h2>"
            question_image = findImage(self.question)
            if self.question['image'] != None:
                html += f'<img src="{question_image}" style="max-width:{maxWidth}px;max-height:{maxHeight}px;"/>'

            #html += f"<h3>{question['items']}</h3>"
            html += f'<div style="height: 200px; padding:400px 0px 0px 0px;" <br>'
            html += f'<div style="position: fixed; left:30px; height: 400px; width:3px; background:black; page-break-inside: avoid;" />'
            html += f'<h4 style="position: relative; left:-30px; bottom: 20px;">{question_maxY}</h4>'
            html += f'<h4 style="position: relative; left:-15px; top:150px; -webkit-transform: rotate(270deg); white-space:nowrap;">{question_yText}</h4>'
            html += f'<div style="position: relative; left:1px; top:295px; height: 3px; width:700px; background:black;" />'
            html += f'<h4 style="position: relative; left:680px; top:10px;">{question_maxX}</h4>'
            html += f'<h4 style="position: relative; left:350px; bottom:20px;">{question_xText}</h4>'
            html += f'<div style="height: 400px; padding:400px 0px 0px 0px;" <br>'

            return html

    #ask user how big image is i.e. % of page width
    # add tick/cross
    #title

    html = ''
    

    for question_number, question in enumerate(poll_data):

        if question['@type'] == "MultipleChoiceQuestion":
            MCQ_question = MultipleChoiceQuestion(question)
            html += MCQ_question.to_html()

        if question['@type'] == "ClickMapQuestion":
            ClickMap_question = ClickMapQuestion(question)
            html += ClickMap_question.to_html()

        if question['@type'] == "OpenTextQuestion":
            OpenText_question = OpenTextQuestion(question)
            html += OpenText_question.to_html()

        if question['@type'] == "RankingQuestion":
            Ranking_question = RankingQuestion(question)
            html += Ranking_question.to_html()

        if question['@type'] == "NumericQuestion":
            Numeric_question = NumericQuestion(question)
            html += Numeric_question.to_html()

        if question['@type'] == "ScatterPlotQuestion":
            ScatterPlot_question = ScatterPlotQuestion(question)
            html += ScatterPlot_question.to_html()

        html += f'<div style="height: 3px; width:100%; background:black; padding: 20px white;" />'
        html += f'<div style="height: 20px; width:100%; position: relative; top: 20px" />'


    #file = open('output.html', 'w')
    #file.write(html)
    #file.close()
    msgBox = qtw.QMessageBox(qtw.QMessageBox.NoIcon, "Generator", "PDF Generated!", qtw.QMessageBox.Ok, parent=None)
    msgBox.exec_()

    savefilename, _ = qtw.QFileDialog.getSaveFileName(None, "Save PDF file", ".", "PDF files (*.pdf)")
    try:
        pdfkit.from_string(html, savefilename, configuration=config, options={"enable-local-file-access": ""})
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

    shutil.rmtree(image_directory)


    #main()

#multiplechoice
#opentextquestion
#rankingquestion
#numericquestion 
#scatterplotquestion 
#clickmapquestion
