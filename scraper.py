import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
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
                if int(name_or_roll) >= 10:
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

def get_students_details(roll_numbers_str, parameter, file_name):
    roll_numbers = roll_numbers_str.split(',')
    result = {}
    for roll_number in roll_numbers:
        student_details = get_student_details(roll_number.strip(), file_name)
        if student_details and parameter in student_details:
            result[roll_number.strip()] = student_details[parameter]
        else:
            result[roll_number.strip()] = None
    return result

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
            
def get_nearest_birthday(file_name, skip=0):
    try:
        data = pyexcel.get_sheet(file_name=file_name)
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
        birthdays = []
        
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
            birthdays.append((days_until_bday, bday, row[name_column_index]))
        
        birthdays.sort()
        
        if skip >= len(birthdays):
            return None, None
        
        nearest_days, nearest_birthday, nearest_name = birthdays[skip]
        
        if nearest_birthday:
            nearest_birthday_str = nearest_birthday.strftime('%d-%m')
            return nearest_name, nearest_birthday_str
        else:
            return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
