import requests, bs4, tablib, urllib, os

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

        except KeyboardInterrupt as e:
            pass


    return idx


if os.path.exists(origin_path + "/Swindow"):
    print('exist')
else:
    os.makedirs(origin_path + "/Swindow")


def run_swindow_crawler(idx=0, save_name="swindow"):




    # end = False
    # count_page = 0
    # while not end:
    for page in range(1, 20000):
        print(page, "page진행중")

        try:
            idx = swindow(page, idx)
            if not idx:
                break
            if idx % 50 == 0:
                with open(os.path.join(origin_path, f'{save_name}_new_xlsx.xlsx'), 'wb') as f_output:
                    f_output.write(crawl_list.export('xlsx'))

                f_output.close()
                print(f"checkPoint: {save_name}_new_xlsx.xlsx has been updated")

        except:
            pass



    with open(os.path.join(origin_path, f'{save_name}_new_xlsx.xlsx'), 'wb') as f_output:
        f_output.write(crawl_list.export('xlsx'))

    f_output.close()

