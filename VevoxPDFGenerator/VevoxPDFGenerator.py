
import sys 
import json
import zipfile
import pdfkit
from PIL import Image
from io import StringIO
import numpy as np
import cv2


path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


print("This is the name of the script ", sys.argv[0])

#filepath = r"C:\Users\Aaron\source\repos\FinalYearProject\VevoxPDFGenerator\poll_week6_v2.zip"
zfile = zipfile.ZipFile(sys.argv[1])

poll_file = zfile.open('polls.json')
poll_data = json.load(poll_file)

img  = zfile.read("resources/1cf6875b-75f6-4a6d-b4db-868c17bfe10d.12567.png")
tmp1 = cv2.imdecode(np.frombuffer(img, np.uint8), 1) 
cv2.imshow("image", tmp1)
print(tmp1)
 
# Maintain output window utill
# user presses a key
cv2.waitKey(0)       
 
# Destroying present windows on screen
cv2.destroyAllWindows()
#img = Image.open(img)
#print(img.size, img.mode, len(img.getdata()))

#image_folder = zfile.open('resources/')
#imlist = zfile.infolist()

#print(imlist)
#for f in imlist:
#    ifile = zfile.open(f)
#    img = Image.open(ifile)
#    print(img)


html = ''
for question_number, question in enumerate(poll_data):
    print(question_number+1, question['@type'], question['text'], question['image'])
    html += f"<h2>{question['@type']}</h2>"
    html += f"<h3>{question_number+1} {question['text']} {question['image']}</h2>"
    if question['@type'] == "MultipleChoiceQuestion":
        for choices in question['choices']:
            print(choices['text'], choices['isCorrectAnswer'], choices['image'])
            html += f"<h3>{choices['text']} {choices['isCorrectAnswer']} {choices['image']}</h2>"

pdfkit.from_string(html, 'output.pdf', configuration=config)
