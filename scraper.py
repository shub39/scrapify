import requests
from bs4 import BeautifulSoup
import csv
import time

def fetch_data_from_website(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    anchors = soup.find_all('a')
    data = {}
    for anchor in anchors:
        link = anchor['href']
        content = anchor.text.strip()
        data[link] = content
    return data

def read_data_from_csv(file_path):
    data = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            link, content = row
            data[link] = content
    return data

def write_data_to_csv(file_path, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Link', 'Content']) 
        for link, content in data.items():
            writer.writerow([link, content])
