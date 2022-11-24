
import sys 
import json
import zipfile
import pdfkit
#from PIL import Image

path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


print("This is the name of the script ", sys.argv[0])

#filepath = r"C:\Users\Aaron\source\repos\FinalYearProject\VevoxPDFGenerator\poll_week6_v2.zip"
zfile = zipfile.ZipFile(sys.argv[1])

poll_file = zfile.open('polls.json')
poll_data = json.load(poll_file)

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
    html += f"<h3>{question_number} {question['text']}</h2>"
    for choices in question['choices']:
         print(choices['text'], choices['isCorrectAnswer'], choices['image'])
        

    #html += f"<p>{question['text']}</p>"

pdfkit.from_string(html, 'output.pdf', configuration=config)
