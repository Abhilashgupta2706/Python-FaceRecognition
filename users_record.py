import csv
import os
from datetime import datetime


def load():
    user_records = {}
    if os.path.exists("user_records.csv"):
        with open('user_records.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                user_records[row[0]] = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
    return user_records


def write(name, login_time):
    with open('user_records.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, login_time.strftime('%Y-%m-%d %H:%M:%S')])
