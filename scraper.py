import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
import time
import pyexcel


def get_student_details(name_or_roll, file_name):
    try:
        data = pyexcel.get_sheet(file_name = file_name)
        name_column_index = None
        roll_column_index = None
        for index, cell_value in enumerate(data.row[0]):
            if cell_value.lower() == 'name':
                name_column_index = index
            elif cell_value.lower() == 'uni roll':
                roll_column_index = index
        if name_column_index is None or roll_column_index is None:
            return None  
        for row_index, row in enumerate(data):
            if row_index == 0:
                continue
            if name_or_roll.isdigit():
                if int(name_or_roll) > 10:
                    roll = "120305230" + name_or_roll
                else:
                    roll = "1203052300" + name_or_roll
                if str(roll) == str(row[roll_column_index]):
                    student_details = {}
                    for col_index, col_name in enumerate(data.row[0]):
                        student_details[col_name] = row[col_index]
                    return student_details
            else:
                if row[name_column_index].lower() == name_or_roll.lower():
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
        if reader == {}:
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
            
def get_nearest_birthday(file_name):
    try:
        data = pyexcel.get_sheet(file_name = file_name)
        bday_column_index = None
        name_column_index = None
        for index, cell_value in enumerate(data.row[0]):
            if cell_value.lower() == 'bday':
                bday_column_index = index
            elif cell_value.lower() == 'name':
                name_column_index = index
        if bday_column_index is None or name_column_index is None:
            return None, None  
        today = datetime.now().date()
        nearest_birthday = None
        nearest_days = float('inf')
        nearest_name = None
        for row_index, row in enumerate(data):
            if row_index == 0:
                continue
            bday_str = str(row[bday_column_index])
            try:
                bday = datetime.strptime(bday_str, '%Y-%m-%d').date()  
            except ValueError:
                try:
                    bday = datetime.strptime(bday_str, '%Y/%m/%d').date()
                except ValueError:
                    continue 
            bday = bday.replace(year=today.year)
            if bday < today:
                bday = bday.replace(year=today.year + 1)
            days_until_bday = (bday - today).days
            if days_until_bday < nearest_days:
                nearest_days = days_until_bday
                nearest_birthday = bday
                nearest_name = row[name_column_index]
        if nearest_birthday:
            nearest_birthday_str = nearest_birthday.strftime('%d-%m')  
            return nearest_name, nearest_birthday_str
        else:
            return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
