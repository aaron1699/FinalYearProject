
from importlib.metadata import requires
import sys 
import json
import zipfile
import pdfkit
from PIL import Image
from io import StringIO
import numpy as np
import cv2
import base64
from django.template import Context, Template
import jinja2
import os
from os import listdir
from os.path import isfile, join
import re

path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)




print("This is the name of the script ", sys.argv[0])

#filepath = r"C:\Users\Aaron\source\repos\FinalYearProject\VevoxPDFGenerator\poll_week6_v2.zip"
zfile = zipfile.ZipFile(sys.argv[1])

for file in zfile.namelist():
    zfile.extract(file)


poll_file = zfile.open('polls.json')
poll_data = json.load(poll_file)

onlyfiles = [f for f in listdir('resources/') if isfile(join('resources', f))]
directory = 'resources/'
#files = os.listdir(directory)
print(onlyfiles)
output = [re.sub(r'\s*\.\d+\.', '.', x) for x in onlyfiles]
print(output)

i = 0
while i != len(output):
    os.rename(directory + onlyfiles[i], directory + output[i])
    i = i + 1

print(onlyfiles)



html = ''
for question_number, question in enumerate(poll_data):
    print(question_number+1, question['@type'], question['text'], question['image'])
    string1 = "C:/Users/Aaron/source/repos/FinalYearProject/VevoxPDFGenerator/resources/"
    string2 = ".gif"
    questionx = question['image']
    final = "%s%s%s" % (string1, question['image'], string2)
    html += f"<h2>{question['@type']}</h2>"
    #html += f'<img src= "C:/Users/Aaron/source/repos/FinalYearProject/VevoxPDFGenerator/resources/c19cd52c-37fd-4e8f-91dc-e63729c6744a.gif"/>' 
    print(final)
    html += f'<img src={final}/>'
    html += f"<h2>{question_number+1} {question['text']} {question['image']}</h2>"  
    if question['@type'] == "MultipleChoiceQuestion":
        for choices in question['choices']:
            print(choices['text'], choices['isCorrectAnswer'], choices['image'])
            html += f"<h3>{choices['text']} {choices['isCorrectAnswer']} {choices['image']}</h3>"
html += f'<img src="C:\\Users\\Aaron\\Downloads\\poll_week6_v2\\resources\\c19cd52c-37fd-4e8f-91dc-e63729c6744a.2871.gif"/>' 


print(final)

pdfkit.from_string(html, 'output.pdf', configuration=config, options={"enable-local-file-access": ""})


