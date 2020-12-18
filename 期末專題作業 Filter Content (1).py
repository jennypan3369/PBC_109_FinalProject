#!/usr/bin/env python
# coding: utf-8

# In[55]:


# 期末專題作業


# 導入模組
import requests 
import bs4

# 輸入網址
lst = ['''網址list輸入''']

def contentfilter:
    # 對所有list中的文章連結
    for url in lst:

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

#         print('原檔:',contents, sep='\n')

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
    #         if contents[i].find('聯絡方式') != -1:
    #             contents.remove(contents[i])
    #             contents.insert(i, '')
    #         if contents[i].find('聯絡人') != -1:
    #             contents.remove(contents[i])
    #             contents.insert(i, '')

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

#         print()
#         print('整理後的list:',lst_final,sep='\n')
#         print()
#         print(content)
#         print()


        ans = []
        for i in range(len(lst_final)):
            
            # district
            if lst_final[i].find('租屋地址') != -1:
                if lst_final[i][8:].find('區') != -1:
                    district = lst_final[i][8:lst_final[i].find('區')+1]
                if lst_final[i][8:].find('市') != -1:
                    district = lst_final[i][8:lst_final[i].find('市')+1]
                if lst_final[i][8:].find('鄉') != -1:
                    district = lst_final[i][8:lst_final[i].find('鄉')+1]
                if lst_final[i][8:].find('鎮') != -1:
                    district = lst_final[i][8:lst_final[i].find('鎮')+1]

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
        if district == '''地區輸入''' or district =='都可以':
            if floor == '''樓層輸入''' or floor == '都可以':
                equipment_list = ['''設備輸入1''','''設備輸入2''','''設備輸入3''']
                if '' in equipment_list:
                    equipment_list.remove('')
                cnt = 0
                for equip in equipment_list:
                    if equip in equipment:
                        cnt += 1
                    if equip == '都可以':
                        cnt += 1
                if cnt == len(equipment_list):
                    if '''租金區間輸入'''.split('~')[1] != '':
                        if int('''租金區間輸入'''.split('~')[0]) <= rent <= int('''租金區間輸入'''.split('~')[1]):
                            ans.append([title, url, person, contact])
                    if '''租金區間輸入'''.split('~')[1] == '':
                        if int('''租金區間輸入'''.split('~')[0]) <= rent:
                            ans.append([title, url, person, contact])
                    if '''租金區間輸入''' == '都可以':
                        ans.append([title, url, person, contact])

#         print(district)                    
#         print(floor)
#         print(rent)
#         print(equipment)
        
        # 二維的list
        return ans


# In[ ]:




