## 製作目的
由於自主學習主題是「**探討太陽能板分佈及記錄全校每日用電量並分析每年用電量數據**」，有一部分需要抓取大量數據才能分析數據，所以決定做一個 Python 網路爬蟲來自動抓取數據，來增加效率。  

## 製作過程
### 1. 分析需求與確定目標:  
我們需要抓的數據有即時需量（kW）、本日累計用電（度）、本月累計用電（度）、年度累計用電（度）、年度CO2排放量（噸），並儲存至 Excel 或 Google Sheet 中，才能進行後續的數據分析。  
### 2. 開始撰寫程式碼:  
#### 1. 使用 Requests 獲取網頁
首先需要發送一個 HTTP 請求，來抓取包含數據的網頁。例如，如果要抓取即時電力數據，可以使用 Python 的<code>requests</code>模組對<code>realdata/kw.aspx</code>頁面發送請求。
```py
import requests

url = "http://140.138.251.201/powermanage/realdata/kw.aspx"
response = requests.get(url)

# 檢查網頁是否成功獲取
if response.status_code == 200:
    html_content = response.content
else:
    print("獲取網頁失敗。")
```
#### 2. 使用 BeautifulSoup 解析 HTML
當我們拿到網頁的 HTML 內容後，可以使用<code>BeautifulSoup</code>來解析它，並擷取出需要的部分。這裡就是要找出用來顯示數字的<code>img</code> 標籤。
```py
from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(html_content, 'html.parser')

# 找到包含數字圖片路徑的 img 標籤
number_images = soup.find_all('img', src=re.compile(r'\.\./images/num/\d\.png'))
```
#### 3. 用定義的方式將圖片檔名對應數字
將每個圖片檔名（如<code>2.png</code>, <code>1.png</code>）對應到它所代表的數字。
```py
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
```
擷取每張圖片的檔名，並將其轉換為對應的數字
```py
number_str = ""
for img in number_images:
    img_src = img['src'].split('/')[-1]  # 擷取檔名 (如 '2.png')
    number_str += digit_map.get(img_src, '?')  # 根據檔名映射到對應的數字

print(f"提取的數字: {number_str}")
```
#### 5. 完整程式碼
```py
import requests
from bs4 import BeautifulSoup
import re

# 將圖片檔名對應到相應的數字
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

# 從給定頁面獲取並解析數字的函數
def fetch_number_from_page(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"無法獲取頁面: {url}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 找出所有顯示數字的 img 標籤
    number_images = soup.find_all('img', src=re.compile(r'\.\./images/num/\d\.png'))
    
    number_str = ""
    for img in number_images:
        img_src = img['src'].split('/')[-1]  # 獲取圖片檔名 (如 '2.png')
        number_str += digit_map.get(img_src, '?')  # 映射到對應的數字
    
    return number_str

# 即時電力數據的範例 URL
url = "http://140.138.251.201/powermanage/realdata/kw.aspx"
number = fetch_number_from_page(url)

if number:
    print(f"提取的即時電力數據: {number}")
```
## 參考資料
* [【 Python 爬蟲 】2 小時初學者課程 ：一次學會 PTT 爬蟲、Hahow 爬蟲、Yahoo 電影爬蟲！](https://youtu.be/1PHp1prsxIM?si=YkFFE6DzUZQ8oPwH)  
* [【python】selenium 網頁自動化、網路爬蟲 ｜ 爬蟲 ｜ python 爬蟲 ｜ 自動化 ｜pycharm ｜](https://youtu.be/ximjGyZ93YQ?si=_wYaRLTHsVZJkxzn)  
  
