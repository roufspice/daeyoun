import tablib, bs4, requests, urllib, json, os

crawl_list = tablib.Dataset(headers=['IDX', 'Goods name', 'Brand name', 'Price', 'Img URL'])
base = os.getcwd()
if os.path.exists(base + '/YOOX'):
    pass
else:
    os.makedirs(base + '/YOOX')


def Yoox_crawller(page, idx):
    url = 'https://www.yoox.com/KR/shoponline?dept=bagsaccwomen&gender=D&page={page}&attributes=%7B%27ctgr%27%3A%5B%27brsmn%27%2C%27brsspll%27%2C%27brstrcll%27%5D%7D&season=X&clientabt=SmsMultiChannel_ON%2CSrRecommendations_ON%2CRecentlyViewed_ON%2CRecentlyViewedItemPage_ON%2CmyooxNew_ON%2CImageFormatB_ON%2COnePageCheckout_ON'.format(
        page=page)
    data = requests.get(url)
    print(data)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    # print(soup)
    list_box = soup.find('div', class_='col-18-24')
    lis = list_box.find_all('div', class_='col-8-24')

    for li in lis:
        if lis == []:
            return False
        # print(li)
        try:
            img = li.find('img').attrs['data-original']
            img2 = li.find('img').attrs['rel']
            brand = li.find('div', class_='brand font-bold text-uppercase').text.replace("\n", "").replace("\t",
                                                                                                           "").replace(
                "/", "").replace("\\", "").replace(" ", "").replace("*", "").replace("\r", "")
            goods = li.find('div', class_='microcategory font-sans').text.replace("\n", "").replace("\t", "").replace(
                "/", "").replace("\\", "").replace(" ", "").replace("*", "").replace("\r", "")
            price_info = li.find('span', class_='fullprice font-bold').text.split(" ")
            price = price_info[price_info.index("(KRW") + 1].rstrip(')')
            crawl_list.append((idx, goods, brand, price, img))
            urllib.request.urlretrieve(img,
                                       base + "/YOOX/IMG{idx}_YOOX_{brand}_{goods}.jpg".format(idx=idx, brand=brand,
                                                                                               goods=goods))
            idx = idx + 1

            if idx % 50 == 0:
                with open(base + '/YOOX/YOOX.xlsx'.format(idx), 'wb') as f:
                    f.write(crawl_list.export('xlsx'))
                print(f"checkPoint: 'YOOX.xlsx' has been updated")

            # print(idx)
            crawl_list.append((idx, goods, brand, price, img2))
            urllib.request.urlretrieve(img2,
                                       base + "/img/YOOX/IMG{idx}_YOOX_{brand}_{goods}.jpg".format(idx=idx, brand=brand,
                                                                                               goods=goods))
            idx = idx + 1
            print(idx)

        except KeyboardInterrupt as e:
            pass
    return idx


# C:\Users\82106\PycharmProjects\madetren\YOOX

def run_Yook_crawller(idx=1):
    for page in range(1, 200):
        print(page, "page진행중")
        idx = Yoox_crawller(page, idx)
        if not idx:
            break


    with open(base + '/YOOX/YOOX.xlsx'.format(idx), 'wb') as f:
        f.write(crawl_list.export('xlsx'))


