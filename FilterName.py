import bs4
import requests

r = requests.get("https://www.ptt.cc/bbs/Rent_apart/index.html")
soup = bs4.BeautifulSoup(r.text, "html.parser")
titles = soup.find_all("div", class_="title")

# 接續 Jenny, CatchTitleAndLink, 1.找標題
title_lst = []  # 例：['\n[徵/竹北/] 室內平面停車位\n', '\n[徵/桃園/多區] 4房2廳2衛 電梯大樓 \n']
for t in titles:
    title_lst.append(t.text)

key_lst = ["徵", "店面", "辦公室", "辦公大樓", "發文教學", "公告"]

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
    Num2Chi = {"1":"一", "2":"二", "3":"三", "4":"四", "5":"五", "6":"六", "7":"七"}
    
    Num_room = room + "房"
    Chi_room = Num2Chi[room] + "房"
    new_title_lst = []
    for title in title_lst:
        if gender in title:
            if city in title:
                if Num_room or Chi_room in title:
                    new_title_lst.append(title)
        elif title[title.find("[")+1] == "無":
            if city in title:
                if Num_room or Chi_room in title:
                    new_title_lst.append(title)
    
    return new_title_lst

cut_title_lst = Cut(title_lst)
filter_title_lst = Filter(cut_title_lst, gender, city, room)  # gender=str, city=str, room=str


