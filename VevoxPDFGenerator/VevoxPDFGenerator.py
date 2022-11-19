
import sys 
import json
import zipfile
import pdfkit

path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


print("This is the name of the script ", sys.argv[0])

filepath = r"C:\Users\Aaron\source\repos\FinalYearProject\VevoxPDFGenerator\poll_week6_v2.zip"
zfile = zipfile.ZipFile(filepath)
poll_file = zfile.open('polls.json')
poll_data = json.load(poll_file)

html = ''
for question_number, question in enumerate(poll_data):
    print(question_number, question['@type'], question['text'])
    html += f"<h2>{question_number} {question['text']}</h2>"
    html += f"<p>{question['text']}</p>"

pdfkit.from_string(html, 'output.pdf', configuration=config)
