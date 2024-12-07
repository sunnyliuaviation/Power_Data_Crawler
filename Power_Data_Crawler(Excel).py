import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import openpyxl
import re

# 圖像檔名對應的數字
digit_map = {
    "0.png": "0",
    "1.png": "1",
    "2.png": "2",
    "3.png": "3",
    "4.png": "4",
    "5.png": "5",
    "6.png": "6",
    "7.png": "7",
    "8.png": "8",
    "9.png": "9"
}

# 獲取網頁
def fetch_number_from_page(url):  
    response = requests.get(url)
    
    # 如果頁面請求失敗，返回 None
    if response.status_code != 200:
        print(f"無法獲取頁面: {url}")
        return None
    
    # 使用 BeautifulSoup 解析頁面內容
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 查找所有顯示數字的圖片標籤
    number_images = soup.find_all('img', src=re.compile(r'\.\./images/num/\d\.png'))
    
    # 提取圖片的 src 屬性並與 digit_map 匹配，重建數字
    number_str = ""
    for img in number_images:
        img_src = img['src'].split('/')[-1]  # 獲取圖片檔名（例如 '2.png'）
        number_str += digit_map.get(img_src, '?')  # 使用映射對應數字，若無對應則使用 '?' 
    
    return number_str

urls = {
    "即時需量〈kW〉": "http://140.138.251.201/powermanage/realdata/kw.aspx",   # 即時電力需求（kW）
    "本日累計用電〈度〉": "http://140.138.251.201/powermanage/realdata/p1.aspx",   # 今日用電累計
    "本月累計用電〈度〉": "http://140.138.251.201/powermanage/realdata/p2.aspx",   # 本月用電累計
    "年度累計用電〈度〉": "http://140.138.251.201/powermanage/realdata/p3.aspx",   # 本年用電累計
    "年度CO2排放量〈噸〉": "http://140.138.251.201/powermanage/realdata/co2.aspx", # 本年CO2排放量
}

# 將數據儲存到 Excel 文件中
def save_to_excel(data):
    file_name = "power_data.xlsx"

    try:
        wb = openpyxl.load_workbook(file_name)
        sheet = wb.active
    except FileNotFoundError:
        # 如果文件不存在，建立一個新的工作簿
        wb = openpyxl.Workbook()
        sheet = wb.active
        # 在第一行建立標題
        sheet.append(["時間戳記", "即時需量〈kW〉", "本日累計用電〈度〉", "本月累計用電〈度〉", "年度累計用電〈度〉", "年度CO2排放量〈噸〉"])

    # 將數據添加到工作表中
    sheet.append([data['時間戳記'], data['即時需量〈kW〉'], data['本日累計用電〈度〉'], data['本月累計用電〈度〉'], data['年度累計用電〈度〉'], data['年度CO2排放量〈噸〉']])

    # 儲存活頁簿
    wb.save(file_name)
    print(f"數據已保存至 {file_name}")

# 主循環，每 10 分鐘執行一次
while True:
    data = {}
    for title, url in urls.items():
        number = fetch_number_from_page(url)
        data[title] = number

    # 添加時間戳記
    data['時間戳記'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 輸出獲取的數據
    print("\n今日數據:")
    for title, number in data.items():
        print(f"{title}: {number}")

    # 將數據儲存到 Excel
    save_to_excel(data)

    # 等待 10 分鐘（600 秒）後再次執行
    time.sleep(600)
