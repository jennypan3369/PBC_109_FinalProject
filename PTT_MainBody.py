#PTT 租屋版


# 用 beautifulsoup 來處理 html 格式
import bs4
import requests

website = "https://www.ptt.cc/bbs/Rent_apart/index.html"


# googlesheet 串接

scopes = ["https://spreadsheets.google.com/feeds"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "credential.json", scopes)
client = gspread.authorize(credentials)
sheet = client.open_by_key(
    "1muFburMLNn2A3-3aEsh6ecT0bkrkn8e7xHpU1A3zp6U").sheet1


# 找標題&網址：回傳一個 dictionary (輸入頁面，輸出 標題&網址 dict)   
def CatchTitleAndLink(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    titles = soup.find_all("div", class_="title")


    # 1.找標題 (title_lst 是個 list)
    title_lst = []
    for t in titles:
        title_lst.append(t.text)


    # 2.抓網址 (article_href 是個 list)
    article_href = []
    for item in titles:
        item_href = item.select_one("a").get("href")
        article_href.append(item_href)

    correspond_dict = dict()
    for i in range(len(title_lst)):
        correspond_dict[title_lst[i]] = 'https://www.ptt.cc' + article_href[i]
    
    return correspond_dict
 
    
    
# 查找到的頁數
# 1.依據使用者輸入的日期
import datetime

date_temp = sheet.batch_get(['B2']) # 記得要改成使用者輸入的欄位！！！！！！

date_temp2 = datetime.datetime.strptime(date_temp[0][0][0],"%m/%d" )
diff = datetime.timedelta(days = 1)
date_input = (date_temp2 - diff).strftime("%m/%d")
print(date_input)

# 2.查找
def CheckDate(date_lst):
    date_check = 0
    for i in date_lst:
        if i.text == date_input:
            date_check += 1
    if date_check == 0:
        return False
    else:
        return True
    
    
# 頁面跳轉    
# 輸入你想要查找得 PTT 的版面後，他會生成所有分頁的連結  (輸入：網站主頁連結，輸出：所有頁面連結的 list)   
def Page(website):
    r = requests.get(website)
    next_page = bs4.BeautifulSoup(r.text, "html.parser")  # 最後面 html.parser  >> 告訴 bs4 是 html 格式
    all_link = []
    all_link.append(website)
    
    while True:
        btn = next_page.select('div.btn-group > a')
        up_page_href = btn[3]['href']
        all_link.append('https://www.ptt.cc' + up_page_href)

        next_page_url = 'https://www.ptt.cc' + up_page_href
        next_page_req = requests.get(next_page_url)
        next_page = bs4.BeautifulSoup(next_page_req.text, "html.parser")
        
        # 依照使用者指定日期，輸入他想要查到的時間為何
        date = next_page.find_all("div", class_="date")
        check = CheckDate(date)
        if check == True:
            break
    
    return all_link


# 輸出到 googlesheet
def gsheet(titles):  
    # append 是把他讀進去
    sheet.append_row(titles, table_range = "C7:C10")
     # 可以自己設定 table_range (str)

        
        
# 這會輸出 board 上的大頁面網址        
pages_url_lst = Page(website) 

# 現在先輸出小頁面網址當測試，之後要改！
link_for_test = []
for url in pages_url_lst:
    TitleLink = CatchTitleAndLink(url)
    
    for i in TitleLink.values():
        link_for_test.append(i)
    gsheet(link_for_test)
    

print(link_for_test)
 