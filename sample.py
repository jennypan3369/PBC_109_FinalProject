import xlwings as xw


def main():
    """基本函數與概念"""
    # excel VBA 會去call python的funtion（不確定要不要最後把所有的互動funtion打包成一個 __main__ 一起呼叫？）
    wb = xw.Book.caller()  # 【重要】所有要跟excel互動的函數都要先加這一行才能讓excel呼叫到
    sht = wb.sheets[0]  # 我設sheet1作為互動的介面，大家只要記得是介面是在 "sht"

    rng = sht.range('d1:d4')  # sht.range('d1:d4')的意思是互動介面sheet1上的d1:d4儲存格這個範圍
    rng.clear()  # .clear() 是清除內容和格式，rng.clear() 就是sheet1的d1:d4儲存格清空
                 # 我覺得Kelly的函數會用到.clear()，因使用者要換篩選條件，重新run 得出新結果的時候，舊的結果要先清掉
    # 【重要】呼叫互動介面的工作表統一用「sht」，有需要去取用excel不同範圍的話rng可自行assign、改命名 --> sht不動、rng可動

    """讀入excel上的string或把值印在excel上"""
    input_price = sht.range('b2').value  # 取sheet1 b2的值，並把它叫做input_price
    if input_price == '一萬':  # 我在我的測試檔案上的sheet1 b2輸入'一萬'（目前還在研究要怎麼讀excel上的數字，暫時只能string）
        sht.range('d2').value = 10000  # 在sheet1 d3 印上 'yes'
    else:
        sht.range('d2').value = ''

    input_place = sht.range('b3').value
    if input_place == '台北':
        sht.range('d3').value = 'Taipei！'
    else:
        sht.range('d3').value = '您目前所選擇的區域佔不支援 拍謝'


    # wb = xw.Book.caller()
    # sheet = wb.sheets[0]
    # if sheet["A1"].value == "Hello xlwings!":
    #     sheet["A1"].value = "Bye xlwings!"
    # else:
    #     sheet["A1"].value = "Hello xlwings!"


if __name__ == "__main__":
    xw.Book("myproject2--standalone.xlsm").set_mock_caller()
    main()
