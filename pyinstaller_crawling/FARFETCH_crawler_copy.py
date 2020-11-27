import urllib,bs4,json,requests,tablib,os
import openpyxl


crawl_list = tablib.Dataset(headers=['IDX','Goods name','Brand name','Price','Img URL'])
base = os.getcwd()
if os.path.exists(base+'/FARFETCH'):
    pass
else:
    os.makedirs(base+'/FARFETCH')
def farfetch_crawler(page,idx):
    url = "https://www.farfetch.com/kr/shopping/women/bags-purses-1/items.aspx?page={page}&view=180&category=136035|136315|136297|137188|137189|136311|137170|136033".format(page=page)
    data = requests.get(url)
    print(data)
    soup = bs4.BeautifulSoup(data.text,'html.parser')
    # print(soup)
    list_box = soup.find('div', class_='_0ab668')
    # print(list_box)
    lis = list_box.find_all('a',class_='_5ce6f6')
    # print(lis)
    count = 0
    for li in lis:
        try:
            img = li.find('meta').attrs['content']
            brand = li.find('h3',class_='_346238').text.replace("\n", "").replace("\t", "").replace("/", "").replace("\\", "").replace(" ","").replace("*","")
            goods = li.find('p',class_='_d85b45').text.replace("\n", "").replace("\t", "").replace("/", "").replace("\\", "").replace(" ","").replace("*","")
            price_in = li.find('div',class_='_6356bb')
            price = price_in.find('span').text
            urllib.request.urlretrieve(img, base+"/FARFETCH/IMG{idx}_FARFETCH_{brand}_{goods}.jpg".format(idx=idx, brand=brand, goods=goods))
            crawl_list.append((idx, goods, brand, price, img))
            print(idx)
            idx += 1

            if idx % 50 == 0:

                # 파일로 만들기
                wb = openpyxl.Workbook()
                sheet = wb.active
                sheet.append(['IDX','Goods name','Brand name','Price','Img URL'])
                for row in crawl_list:
                    # print(row)
                    sheet.append(row)
                wb.save(os.path.join(base + '/FARFETCH/메이드트렌_FARFETCH.xlsx'))
                print(f"==========checkPoint: '메이드트렌_FARFETCH.xlsx' has been updated==========")
                # with open(base + '/FARFETCH/메이드트렌_FARFETCH.xlsx'.format(idx), 'wb') as f:
                #     f.write(crawl_list.export('xlsx'))
                # print(f"checkPoint: '메이드트렌_FARFETCH.xlsx' has been updated")

        except KeyboardInterrupt as e:
            pass

    return idx

idx = 1



def run_farfetch_crawler(idx =1):

    for page in range(1,98):
        print(page, "page진행중/",'97page중')
        idx = farfetch_crawler(page,idx)

    # with open(base + '/FARFETCH/메이드트렌_FARFETCH.xlsx'.format(idx), 'wb') as f:
    #     f.write(crawl_list.export('xlsx'))
    # print(f"checkPoint: '메이드트렌_FARFETCH.xlsx' has been updated")
