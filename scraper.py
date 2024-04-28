import requests
from bs4 import BeautifulSoup
import csv
import time
import pyexcel


def get_student_details(name):
    try:
        data = pyexcel.get_sheet(file_name='DS_DATA.ods')
        name_column_index = None
        for index, cell_value in enumerate(data.row[0]):
            if cell_value.lower() == 'name':
                name_column_index = index
                break
        if name_column_index is None:
            return None  
        for row_index, row in enumerate(data):
            if row_index == 0:  
                continue
            if row[name_column_index].lower() == name.lower():
                student_details = {}
                for col_index, col_name in enumerate(data.row[0]):
                    student_details[col_name] = row[col_index]
                return student_details        
                return None 
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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
