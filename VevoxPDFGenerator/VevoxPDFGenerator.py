import sys 
import json
import zipfile
import pdfkit
import os
from os import listdir
from os.path import isfile, join
import re
import shutil

path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)




print("This is the name of the script ", sys.argv[0])

#filepath = r"C:\Users\Aaron\source\repos\FinalYearProject\VevoxPDFGenerator\poll_week6_v2.zip"
zfile = zipfile.ZipFile(sys.argv[1])

for file in zfile.namelist():
    zfile.extract(file)


poll_file = zfile.open('polls.json')
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


def findImage(name):
        imagestring = ''
        if name['image'] != None and any(name['image'] in s for s in new_list):
            matching = [s for s in new_list if name['image'] in s]
            imagestring = os.path.dirname(os.path.abspath(__file__)) + "\\resources\\" + str(matching[0])
        return imagestring

html = ''

for question_number, question in enumerate(poll_data):
    #print(question_number+1, question['@type'], question['text'], question['image'])
    html += f"<h2>{question['@type']}</h2>"
    html += f"<h2>{question_number+1} {question['text']} {question['image']}</h2>"
    question_image = findImage(question)
    if question['image'] != None:
           html += f'<img src="{question_image}"/>'

    if question['@type'] == "MultipleChoiceQuestion":
        for choices in question['choices']:
            print(choices['text'], choices['isCorrectAnswer'], choices['image'])
            html += f"<h3>{choices['text']} {choices['isCorrectAnswer']} {choices['image']}</h3>"
            choices_image = findImage(choices)
            if choices['image'] != None:
                html += f'<img src="{choices_image}"/>'
        html += f"<h3>{question['correctAnswerExplanation']}</h3>"

    if question['@type'] == "ClickMapQuestion":
        #for options in question['options']:
        html += f"<h3>{question['options']} {question['correctAnswers']} {question['correctAnswerExplanation']}</h3>"

    if question['@type'] == "OpenTextQuestion":
        for answers in question['correctAnswers']:
            html += f"<h3>{answers}</h3>"
        html += f"<h3>{question['correctAnswerExplanation']}</h3>"

    if question['@type'] == "RankingQuestion":
        for choices in question['choices']:
            html += f"<h3>{choices['sequence']} {choices['text']} {choices['image']}</h3>"
            choices_image = findImage(choices)
            if choices['image'] != None:
                html += f'<img src="{choices_image}"/>'

    if question['@type'] == "NumericQuestion":
        for answers in question['correctAnswers']:
            html += f"<h3>Min: {answers['min']} <br> Max: {answers['max']}</h3>"
        html += f"<h3>{question['correctAnswerExplanation']}</h3>"

    #if question['@type'] == "ScatterPlotQuestion":
    
#html += f'<img src="C:\\Users\\Aaron\\Downloads\\poll_week6_v2\\resources\\c19cd52c-37fd-4e8f-91dc-e63729c6744a.2871.gif"/>' 


file = open('output.html', 'w')
file.write(html)
file.close()

pdfkit.from_string(html, 'output.pdf', configuration=config, options={"enable-local-file-access": ""})

shutil.rmtree(image_directory)



#multiplechoice
#opentextquestion
#rankingquestion
#numericquestion 
#scatterplotquestion 
#clickmapquestion
