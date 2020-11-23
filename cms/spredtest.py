# スプレッドシートのテスト

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('tech-card-2894e3e99fd6.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('teccard test').sheet1

wks.update_acell('A1', 'Hello World!')
print(wks.acell('A1'))