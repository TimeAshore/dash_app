import csv
import requests


def core_domain():
    csv_file=open('core.csv')
    csv_reader_lines = csv.reader(csv_file)
    date = []
    for one_line in csv_reader_lines:
        date.append(one_line)
    i = 0
    while i < len(date):
        print(date[i][2], date[i][3], date[i][4], date[i][5], date[i][6], date[i][8], date[i][9])
        url = 'http://127.0.0.1:5000/domain/archived'
        data = {
            'icp_updated': date[i][2],
            'name': date[i][3],
            'icp_number': date[i][4],
            'sponsor': date[i][5],
            'sponsor_type': date[i][6],
            'city_code': date[i][8],
            'region_code': date[i][9],

        }
        i += 1
        resp = requests.post(url, json=data)
        print(resp.json())


def company_domain():
    csv_file=open('company.csv')
    csv_reader_lines = csv.reader(csv_file)
    date = []
    for one_line in csv_reader_lines:
        date.append(one_line)
    i = 0
    while i < len(date):
        print(date[i][2], date[i][3], date[i][4], date[i][5], date[i][6], date[i][8], date[i][9])
        url = 'http://127.0.0.1:5000/domain/archived'
        data = {
            'icp_updated': date[i][2],
            'name': date[i][3],
            'icp_number': date[i][4],
            'sponsor': date[i][5],
            'sponsor_type': date[i][6],
            'city_code': date[i][8],
            'region_code': date[i][9],

        }
        i += 1
        resp = requests.post(url, json=data)
        print(resp.json())


if __name__ == '__main__':
    core_domain()
    # company_domain()



