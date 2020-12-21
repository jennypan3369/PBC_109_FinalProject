
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


# 找標題&網址：回傳一個 dictionary (輸入頁面的網址list，輸出 標題&網址 dict)   
def CatchTitleAndLink(url_lst):
    correspond_dict = dict()
    
    for url in url_lst:
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

        # 3. 抓日期
        date = soup.find_all("div", class_="date")
        date_lst = []
        for d in date:
            d_temp = d.text.strip()
            d_temp2 = datetime.datetime.strptime(d_temp,"%m/%d" )
            date_lst.append(d_temp2)
        
        # 判別日期是否大於等於使用者輸入的日期，變成一個編號位置的 list
        loc_lst = []

        for j in range(len(date_lst)):
            if date_lst[j] >= date_user:
                loc_lst.append(j)     
        
        # append 到 dict
        for i in loc_lst:
            correspond_dict[title_lst[i]] = 'https://www.ptt.cc' + article_href[i]
    
    return correspond_dict
 
    
    
# 查找到的頁數
# 1.依據使用者輸入的日期
import datetime

date_temp = sheet.batch_get(['B2']) # 記得要改成使用者輸入的欄位！！！！！！

date_user = datetime.datetime.strptime(date_temp[0][0][0],"%m/%d" )
diff = datetime.timedelta(days = 1) # 這邊要抓使用者輸入的前一天（要確保頁面上該日期都有，之後再篩）
date_input = (date_user - diff).strftime("%m/%d")
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
def gsheet(output):  
    # append 是把他讀進去
    for i in output:
        sheet.append_row(i, table_range = "C7:C10")
         # 可以自己設定 table_range (str)


# 刪除不符合要求(key_lst)的標題
def Cut(title_lst):  
    # 找到 key在title_lst的index
    tmp_record_index = []
    for title in title_lst:  
        index = title_lst.index(title)
        for key in key_lst:
            if key in title:
                tmp_record_index.append(index)
                continue
        if title.find("房") == -1:
            tmp_record_index.append(index)

    # 刪除不符要求的標題 index，append 進新的 new_title_lst
    new_title_lst = []
    all_index = set(list(range(len(title_lst))))  # 建立{0,1,.,len(title_lst)}
    record_index = set(tmp_record_index)
    new_all_index = all_index - record_index
    for r in new_all_index:
        new_title_lst.append(title_lst[r])
    
    return new_title_lst


# 篩選符合使用者條件的標題（需輸入 Leona 部分的性別、城市、房數）
def Filter(title_lst, gender, city, room):  # gender=str(), city=str(), room=str()
    Num2Chi = {"1":"一", "2":"二", "3":"三", "4":"四", "5":"五", "6":"六", "7":"七","8":"八"}
    
    Num_room = room + "房"
    Chi_room = Num2Chi[room] + "房"
 
    new_title_lst = []
    for title in title_lst:
        if gender in title:
            if city in title:
                if Num_room in title or Chi_room in title or room == "都可以":
                    new_title_lst.append(title)
        elif title[title.find("[")+1] == "無":
            if city in title:
                if Num_room in title or Chi_room in title or room == "都可以":
                    new_title_lst.append(title)
    
    return new_title_lst


# 內文篩選
def contentfilter(url_lst, district_input, rent_input, floor_input, equipment_list):
    # 對所有list中的文章連結
    ans = []
    for url in url_lst:

        # 設定Header與Cookie
        my_headers = {'cookie': 'over18=1;'}

        # 發送get 請求 到 ptt 八卦版
        response = requests.get(url, headers = my_headers)

        # 把網頁程式碼(HTML) 丟入 bs4模組分析
        soup = bs4.BeautifulSoup(response.text,"html.parser")

        # 標題
        header = soup.find_all('span','article-meta-value')
        title = header[2].text


        ## 查找所有html 元素 抓出內容
        main_container = soup.find(id='main-container')

        # 把所有文字都抓出來
        all_text = main_container.text

        # 把整個內容切割透過 "-- " 切割成2個陣列
        pre_text = all_text.split('--')[0]

        # 把每段文字 根據 '\n' 切開
        texts = pre_text.split('\n')

        # 如果你爬多篇你會發現 
        contents = texts[2:]


        # 去除一些不看的資訊，並格式化部分文字
        i = 0
        while i < len(contents):

            if contents[i][:contents[i].find('：')].find(' ') != -1:
                contents[i] = contents[i].replace(' ','')
            if contents[i].find('\u3000') != -1:
                contents[i] = contents[i].replace('\u3000','')
            if contents[i][:contents[i].find(':')].find(' ') != -1:
                contents[i] = contents[i].replace(' ','')
            if contents[i].find('\u3000') != -1:
                contents[i] = contents[i].replace('\u3000','')

            if contents[i].find('：') != -1 and contents[i+1].find('：') != -1:
                contents.insert(i+1,'')

            if contents[i].find('照片連結') != -1:
                contents.remove(contents[i])
                contents.insert(i, '')
            if contents[i].find('聯絡方式') == -1 and contents[i].find('http') != -1:
                contents.remove(contents[i])
                contents.insert(i, '')

            i += 1


        # 將我們要的資訊另存一個list
        lst_final = []
        for i in range(len(contents)):
            if i != len(contents):
                if contents[i] != '' and contents[i+1] != '':
                    contents[i+1] = contents[i] + contents [i+1]
                if contents[i] != '' and contents[i+1] == '':
                    lst_final.append(contents[i])
        for element in lst_final:
            if element.find('聯絡人') != -1:
                person = element[4:]
            if element.find('聯絡方式') != -1:
                contact = element[5:]


        content = '\n'.join(lst_final) # 排版比較好觀察
        print(url)
        for i in range(len(lst_final)):

            # district2
            if lst_final[i].find('租屋地址') != -1:
                if lst_final[i][8:].find('區') != -1:
                    district2 = lst_final[i][8:lst_final[i].find('區')+1]
            else:
                district2 = "沒寫"
                    
            # floor
            if lst_final[i].find('租屋樓層') != -1:
                floor = lst_final[i][5:lst_final[i].find('/')]

            # rent
            if lst_final[i].find('每月租金') != -1:
                num_list = ['1','2','3','4','5','6','7','8','9','0']
                for j in range(5,len(lst_final[i])):
                    if lst_final[i][j] not in num_list:
                        lst_final[i] = lst_final[i].replace(lst_final[i][j], ' ')
                rent = int(lst_final[i][5:].replace(' ',''))
            
            # equipment
            if lst_final[i].find('提供設備') != -1:
                equipment = lst_final[i][5:]
                
        # 這裡為使用者輸入的地方

        if district_input == "都可以" or district2 == district_input:
            if floor == floor_input or floor_input == '都可以':
                if '' in equipment_list:
                    equipment_list.remove('')
                cnt = 0
                for equip in equipment_list:
                    if equip in equipment:
                        cnt += 1
                    if equip == '都可以':
                        cnt += 1
                if cnt == len(equipment_list):
                    if rent_input.split('~')[1] != '':
                        if int(rent_input.split('~')[0]) <= rent <= int(rent_input.split('~')[1]):
                            ans.append([title, url, person, contact])
                    if rent_input.split('~')[1] == '':
                        if int(rent_input.split('~')[0]) <= rent:
                            ans.append([title, url, person, contact])
                    if rent_input == '都可以':
                        ans.append([title, url, person, contact])
        

        
    # 二維的list
    return ans


# 前情提要
key_lst = ["徵", "店面", "辦公室", "辦公大樓", "發文教學", "公告"]

        
# step1：搜集 board 上的大頁面網址（這會輸出 board 上的大頁面網址 list)        
pages_url_lst = Page(website) 

# step2: 將上面的所有標題＆link抓下來
title_lst = []
TitleLink = CatchTitleAndLink(pages_url_lst)

for i in TitleLink.keys():
    title_lst.append(i)

# step3：標題篩選
# 這邊要改！！
gender = "女" #C3
city = "台北" #C4
room = "2" #C7
cut_title_lst = Cut(title_lst)
filter_title_lst = Filter(cut_title_lst, gender, city, room)
print(filter_title_lst)


# step4: 篩選標題後，輸出一個符合標題的網址 list
link_filtered_lst = []
for i in filter_title_lst:
    for j in TitleLink.keys():
        if i == j:
            link_filtered_lst.append(TitleLink[j])
print(link_filtered_lst)            
# step5: 將內文做 filter
# 這邊要改！！
district_input = "都可以" #C4 
rent_input = "10001~30000"
floor_input= "都可以"
equipment_list = ["都可以","都可以","冷氣"]

output = contentfilter(link_filtered_lst,district_input,rent_input,floor_input,equipment_list)


#印出在 googlesheet 上
gsheet(output)


print(output)
 
