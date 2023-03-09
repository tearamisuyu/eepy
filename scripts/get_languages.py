import csv
import requests
from bs4 import BeautifulSoup

r = requests.get('https://tesseract-ocr.github.io/tessdoc/Data-Files#data-files-for-version-400-november-29-2016')
html_content = BeautifulSoup(r.text, 'html.parser')

with open('languages.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['code', 'lang'])
    
    for table in html_content.find_all('table'):
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 3:
                print([cols[0].text.strip(), cols[1].text.strip()])
                writer.writerow([cols[0].text.strip(), cols[1].text.strip()])
                