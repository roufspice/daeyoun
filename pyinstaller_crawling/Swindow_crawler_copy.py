import requests, bs4, tablib, urllib, os, sys
import openpyxl
import keyboard
import time



crawl_list = tablib.Dataset(headers=['IDX', 'Goods name', 'Brand name', 'Price', 'Img URL'])
idx = 0
origin_path = os.getcwd()

address = 'https://m.swindow.naver.com/designer/list/more/composite'


def swindow(page, idx=0):
    # idx = 0
    header = {
        "referer": "https://m.swindow.naver.com/designer/list/category?menu=10009045",

        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36',

    }
    form = {
        "item.paging.current": page,
        "item.paging.rowsPerPage": 50,
        "item.paging.moreCount": "true",
        "item.tr": "swl",
        "cache": "true",
        "all": "true",
        "openPetLink": "false",
        "pageCode": "LIST",
        "menu": 10009045,
        "ios": "false",
        "sort": "DATE_DSC",
        "naverPayOnly": "false",
        "sType": "append",
        "current": page,
        "clickCodeArea": "pct",
        "tr": "swl"
    }
    data = requests.post(url=address, headers=header, data=form).text
    soup = bs4.BeautifulSoup(data, 'html.parser')
    lis = soup.find_all('li')
    for li in lis:
        src = li.find('img').attrs['src']
        p_name = li.find('strong').text
        price = li.find('span', class_='price').text
        b_name = li.find('a', class_='storewrap').text

        try:
            urllib.request.urlretrieve(src, origin_path + "/Swindow/{}.jpg".format(idx))
            crawl_list.append((idx, p_name, b_name, price, src))
            idx = idx + 1
            print(idx)


        except:
            pass


    return idx



if os.path.exists(origin_path + "/Swindow"):
    print('exist')
else:
    os.makedirs(origin_path + "/Swindow")


def run_swindow_crawler(idx=0, save_name="swindow"):
    for page in range(1, 20000):
        try:
            print(page, "page진행중")
            idx = swindow(page, idx)
            if not idx:
                break


            # print(crawl_list)
            if idx % 50 == 0:

                #<class 'tablib.core.Dataset'>
                #파일로 만들기
                wb = openpyxl.Workbook()
                sheet = wb.active
                sheet.append(['IDX', 'Goods name', 'Brand name', 'Price', 'Img URL'])
                for row in crawl_list:
                    # print(row)
                    sheet.append(row)
                wb.save(os.path.join(origin_path,f'{save_name}_new_xlsx.xlsx'))
                # with open(os.path.join(origin_path, f'{save_name}_new_xlsx.xlsx'), 'wb') as f_output:
                #     f_output.write(crawl_list.export('xlsx'))


                print(f"==========checkPoint: {save_name}_new_xlsx.xlsx has been updated==========")

        except KeyboardInterrupt:
            break


    #완료시
    for row in crawl_list:
        sheet.append(row)
    wb.save(os.path.join(origin_path,f'{save_name}_new_xlsx.xlsx'))
    print(f"==========checkpoint {save_name}_new_xlsx.xlsx has been completed==========")


    # with open(os.path.join(origin_path, f'{save_name}_new_xlsx.xlsx'), 'wb') as f_output:
    #     f_output.write(crawl_list.export('xlsx'))




