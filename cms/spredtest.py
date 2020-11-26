# スプレッドシートのテスト

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('tech-card-2894e3e99fd6.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('teccard test').sheet1

wks.update_acell('A2', 'Hello World!今日は')# ここに入力する内容を書き込んでいるから、DBのデータをlistに入れてここに挿入すればいい
print(wks.acell('A1'))#スプレッドシートから値を取得してprint


# テストの手順
# １APIの承諾
# ２アカウントキーの生成
# ３スプレッドシートの作成
# ４シートにキーを共有
# ５プログラムのようい
# ６プログラムにシートの場所とjsonフォルダの情報入力
# コードの実行で書き込まれる

# スプレッドに必要な情報
# ・使用者が作ったスプレッド情報のアクセス情報
# ・API