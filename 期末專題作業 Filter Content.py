#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 期末專題作業


# 導入模組
import requests 
import bs4

# 輸入網址
lst = ['https://www.ptt.cc/bbs/Rent_apart/M.1608134422.A.DB4.html']

# 對所有list中的文章連結
for url in lst:
    
    # 設定Header與Cookie
    my_headers = {'cookie': 'over18=1;'}
    
    # 發送get 請求 到 ptt 八卦版
    response = requests.get(url, headers = my_headers)

    #  把網頁程式碼(HTML) 丟入 bs4模組分析
    soup = bs4.BeautifulSoup(response.text,"html.parser")


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

    print(contents)
    
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
        if contents[i].find('http') != -1:
            contents.remove(contents[i])
            contents.insert(i, '')
        if contents[i].find('聯絡方式') != -1:
            contents.remove(contents[i])
            contents.insert(i, '')
        if contents[i].find('聯絡人') != -1:
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

    
    content = '\n'.join(lst_final) # 排版比較好觀察
    
    print(lst_final)
    print()
    print(content)
    print()

