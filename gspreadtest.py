import gspread
import requests
from lookupGSPREAD import gspread_auth
import os
import time
import gspreader
credfile = os.environ.get('GSPREADER_GOOGLE_CREDS_PATH')

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        print('Connected to the Internet')
    except requests.ConnectionError:
        print('No Internet Connection')

def test_gspread():
    client = gspread_auth(credfile)

    # do this every 5 seconds 10 times
    for i in range(10):
        print('\n\ni = ', i)
        check_internet()
        sheet = client.open('Klas Title Demos Ratings Comments').sheet1
        print (sheet)
        # print (sheet.get_all_records())
        print(sheet.row_values(1))
        time.sleep(2)

def test_gspreader():

    client = gspread_auth(credfile)

    
    for i in range(10):
        print('\n\ni = ', i)
        check_internet()
        sheet = gspreader.get_sheet('Klas Title Demos Ratings Comments', 0, client)
        print (sheet)
        # print (sheet.get_all_records())
        print(sheet.row_values(1))
        time.sleep(2)

if __name__ == '__main__':
    test_gspread()
    # test_gspreader()