
import sys 
import json
import zipfile
import pdfmake
import pdfkit



zfile = zipfile.ZipFile(sys.argv[1])
poll_file = zfile.open('polls.json')
poll_data = json.load(poll_file)

html = ''
for question_number, question in enumerate(poll_data):
    print(question_number, question['@type'], question['text'])
    html += f"<h2>{question_number} {question['text']}</h2>"
    html += f"<p>{question['text']}</p>"

pdfmake.from_string(html, 'output.pdf')
