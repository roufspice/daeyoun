import tablib, bs4, urllib, requests, numbers, os
import openpyxl

code_list = ["001050662","001050661","001050660","001050659","001239125","000700011"]
crawl_list = tablib.Dataset(headers=['Goods name','Brand name','Price','Img URL'])
base = os.getcwd()
if os.path.exists(base+'/WIZWID'):
    pass
else:
    os.makedirs(base+'/WIZWID')

def wizwid_crawl(code,page,idx):
    url = 'https://www.wizwid.com/CSW/handler/wizwid/kr/Catalog-Start?CategoryID={code}&Flag=&OrderType=New&MaxRowNum=1000&PageNO={page}&CouponYn=&SaleYn=&SordOut=&Delivery1=&Delivery2=&RPrice=#browseOptions'.format(code=code,page = page)
    data = requests.get(url)
    # print(data)
    # print(data.text)
    # print(url)
    soup = bs4.BeautifulSoup(data.text,'html.parser')
    base_directory = "Z:\메이드트렌\크롤링데이터/"
    list_box = soup.find('ul',class_='thumbCatalog clearfix')
    lis = list_box.find_all('li')

    for li in lis:
        if lis == []:
            return False
        try:
            img = li.find('img').attrs['src']
            brand = li.find('dd', class_="brand").text.replace("\n","").replace("\t","").replace("/","").replace("\\","")
            goods = li.find('dd', class_="goods").text.replace("\n","").replace("\t","").replace("/","").replace("\\","")
            price = li.find('dd', class_="price sales").text.replace("\n","").replace("\t","")
            urllib.request.urlretrieve(img, base+"/WIZWID/IMG{idx}_WIZWID_{brand}_{goods}.jpg".format(idx=idx,brand=brand,goods=goods))
            crawl_list.append((goods, brand, price, img))
            # print(idx)
            idx += 1
            if idx % 50 == 0:
                # 파일로 만들기
                wb = openpyxl.Workbook()
                sheet = wb.active
                sheet.append(['Goods name','Brand name','Price','Img URL'])
                for row in crawl_list:
                    # print(row)
                    sheet.append(row)
                wb.save(os.path.join(base + '/WIZWID/메이드트렌_WIZWID.xlsx'))
                print(f"==========checkPoint: '메이드트렌_WIZWID.xlsx' has been updated==========")
                # with open(base + '/WIZWID/메이드트렌_WIZWID.xlsx', 'wb') as f:
                #     f.write(crawl_list.export('xlsx'))

        except KeyboardInterrupt as e:
            pass
    return idx


def run_wizwid_crawl():
    idx =1
    for code in code_list:
        # print(code)
        for page in range(1,10):
            print(page, "page진행중/")
            idx = wizwid_crawl(code, page, idx)
            if not idx:
                break

    # with open(os.path.join(base + '/WIZWID/메이드트렌_WIZWID.xlsx','wb')) as f :
    #     f.write(crawl_list.export('xlsx'))

