import urllib,bs4,requests, tablib,os
import openpyxl

numlist = ['004001','004002','004004']
base = os.getcwd()

if os.path.exists(base+'/Wconcept'):
    pass
else:
    os.makedirs(base+'/Wconcept')
crawl_list = tablib.Dataset(headers=['IDX','Goods name','Brand name','Price','Img URL'])

def wconcept_crawller(number,page,idx):
    url = 'https://www.wconcept.co.kr/Women/{num}?page={page}'.format(num=number,page= page)
    data = requests.get(url)
    # print(type(data.text))
    # print(data.text)
    soup = bs4.BeautifulSoup(data.text,'html.parser')
    list_box = soup.find('div',class_='thumbnail_list')
    # print(list_box)
    lis = list_box.find_all('li')

    for li in lis:
        if lis == []:
            return False
        try:
            img = "http:"+li.find('img').attrs['src']
            # print(idx)
            brand = li.find('div',class_='brand').text.replace("\n", "").replace("\t", "").replace("/", "").replace("\\", "").replace(" ","").replace("*","")
            goods = li.find('div',class_='product ellipsis multiline').text.replace("\n", "").replace("\t", "").replace("/", "").replace("\\", "").replace(" ","").replace("*","")
            price = li.find('span',class_='discount_price').text
            # print(brand,name,price)
            crawl_list.append((idx, goods, brand, price, img))
            urllib.request.urlretrieve(img,base+"/Wconcept/IMG{idx}_Wconcept_{brand}_{goods}.jpg".format(idx=idx, brand=brand,goods=goods))
            idx = idx + 1

            if idx % 50 == 0:

                # 파일로 만들기
                wb = openpyxl.Workbook()
                sheet = wb.active
                sheet.append(['IDX', 'Goods name', 'Brand name', 'Price', 'Img URL'])
                for row in crawl_list:
                    # print(row)
                    sheet.append(row)
                wb.save(os.path.join(base+'/Wconcept/메이드트렌_Wconcept.xlsx'))


                # with open(base + '/Wconcept/메이드트렌_Wconcept.xlsx', 'wb') as f:
                #     f.write(crawl_list.export('xlsx'))
                print(f"==========checkPoint: '메이드트렌_Wconcept.xlsx' has been updated==========")


        except KeyboardInterrupt as e:
            pass
    return idx



def run_wconcept_crawller():
    idx = 1
    for number in numlist:
        for page in range(1,20000):
            print(page, "page진행중/")
            idx = wconcept_crawller(number,page,idx)
            if not idx:
                break


    # with open(base,'메이드트렌_Wconcept.xlsx', 'wb') as f:
    #     f.write(crawl_list.export('xlsx'))