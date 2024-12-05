import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 設定 Google Sheets API 的認證
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'檔案位置\檔名.json', scope)  # 憑證檔案名稱
client = gspread.authorize(creds)

# 開啟 Google Sheets 文件
spreadsheet_id = 'spreadsheet ID' 
sheet = client.open_by_key(spreadsheet_id).sheet1  # 取得第一個工作表

# 設定爬蟲目標
url = 'https://www.yzu.edu.tw/index.php/tw'  # 網站網址
url_page = url[:url.find('/', url.find('//') + 2)]  # 取得網站的基礎網址
response = requests.get(url)  # 發送 HTTP 請求抓取頁面
soup = BeautifulSoup(response.text, 'html.parser')  # 使用 BeautifulSoup 解析頁面

# 取得消息內容
content_divs = soup.find_all('div', class_='msg-content')  # 假設消息在 msg-content class 裡

# 假設 Google Sheets 第一行是表頭，這邊可以加上表頭寫入
sheet.append_row(['Title', 'Link', 'Date'])

# 將抓取到的資料寫入 Google Sheets
for content_div in content_divs:
    title_tag = content_div.find('h3').find('a')  # 假設標題在 h3 標籤內的 a 標籤
    title = title_tag.text.strip() if title_tag else 'N/A'  # 取得標題

    link = url_page + title_tag['href'] if title_tag and 'href' in title_tag.attrs else 'N/A'  # 取得連結

    date_tag = content_div.find('div', class_='date')  # 假設日期在 date class 裡
    date = date_tag.text.strip() if date_tag else 'N/A'  # 取得日期

    # 寫入 Google Sheets (假設從第 2 列開始寫入)
    sheet.append_row([title, link, date])

    print(f'Title: {title}')
    print(f'Link: {link}')
    print(f'Date: {date}')
    print("-" * 40)

