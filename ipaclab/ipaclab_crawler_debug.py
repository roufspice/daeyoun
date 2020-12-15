import json
import requests
from bs4 import BeautifulSoup
import os
import time


export_root = os.path.join(os.getcwd())

dict_list = [] #최종적으로 나올 json 출력물
data_dict = { #json출력물

}

login_info = {
    'iu_id': 'voucher_admin',
    'password': 'rhksflwk@!@#$'
}

headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'Content-Type': 'application/json; charset=utf-8',
    'Referer': 'http://ipaclab.ipactory.com:29983/tr_manager/',
    'Accept-Language': 'ko-KR,ko;q=0.9',
}

params = {
    'originalNum': '',
    'transNum': '',
    'idomeIdx': '',
    'return_page': '/tr_manager/main/',
    'row_num': '10',
    'cur_page': ''

}

# session
s = requests.Session()
url = 'http://ipaclab.ipactory.com:29983/tr_manager/login/'
res = s.post(url=url, data=login_info)

main_url = 'http://ipaclab.ipactory.com:29983/tr_manager/main/'

main_params = {
    'is_transcripted': '2'
}

res = s.get(url=main_url, headers=headers, params=main_params)

main_p_soup = BeautifulSoup(res.text, 'html.parser')

# 전체글 갯수 check
total_docs = main_p_soup.find('div', class_='card-body').findChildren('div', class_='row')[1].findChildren('span')[
    0].text.replace('total docs : ', '')
total_docs = int(total_docs)

if total_docs % 10 == 0:
    page_count = int(total_docs / 10)
else:
    page_count = (total_docs // 10) + 1


print(f'total_docs:{total_docs}')
print(f'page_count: {page_count}')

"""전체페이지 조회"""
start = time.time()

for page in range(page_count):

    page_params = {
        'row_num': '10',
        'cur_page': str(page + 1),
        'is_transcripted': '2'
    }

    main_url = 'http://ipaclab.ipactory.com:29983/tr_manager/main/'
    res = s.get(url=main_url, params=page_params, headers=headers)
    main_p_soup = BeautifulSoup(res.text, 'html.parser')

    table = main_p_soup.find("table", class_='w3-table-all')
    tr = table.find("tbody").find_all("tr")

    tran_url = 'http://ipaclab.ipactory.com:29983/tr_manager/main/patent_view/'  # 번역보기

    print(f'{page + 1}진행중/{page_count}/{len(tr)}')

    for i, td in enumerate(tr, start=1):  # 해당페이지게시글크롤링진행
        print(f'{page*10 + i}/{total_docs}')
        label_id = td.find_all("label")[0].text
        trans_btn = td.find("a", class_="btn bg-indigo-400 medium-font search-btn")
        try:
            is_transcripted_btn = td.find("a", class_="btn bg-grey-400 medium-font isTranscripted-btn")
            is_transcripted = is_transcripted_btn.attrs['is_transcripted']
        except AttributeError:
            is_transcripted_btn = td.find("a", class_="btn bg-indigo-400 medium-font isTranscripted-btn")
            is_transcripted = is_transcripted_btn.attrs['is_transcripted']
        # btn bg-indigo-400 medium-font isTranscripted-btn

        originalNum = trans_btn.attrs['data-orgno']
        transNum = trans_btn.attrs['data-transno']
        idomeIdx = trans_btn.attrs['data-idomeidx']

        params['originalNum'] = originalNum
        params['transNum'] = transNum
        params['idomeIdx'] = idomeIdx
        params['cur_page'] = str(page + 1)

        res = s.get(url=tran_url, params=params, headers=headers)
        trans_soup = BeautifulSoup(res.text, 'html.parser')

        data_dict[transNum] = {
            'originalNum': originalNum,
            'is_transcripted': is_transcripted,
            'is_assgined':label_id,
            'desc': {},
            'claims': {}
        }

        desc_dict = {
            'origin': {},
            'trans': {},

        }
        claim_dict = {
            'origin': {},
            'trans': {},
        }

        #row_description and trans
        contents =trans_soup.find_all('div', class_='col-xl-6 w3-border-right info-div')
        row_descriptions_origins = contents[2]
        row_descriptions_trans = contents[3]
        row_claims_origins = contents[4]
        row_claims_trans = contents[5]

        # 1) row_descriptions_origin
        row_descriptions_origins = row_descriptions_origins.find_all('div', class_='row description-div')
        for row_description_origin in row_descriptions_origins:
            desc_idx = row_description_origin.find("div", class_="col-xl-1").text
            origin_desc = row_description_origin.find("textarea", class_="form-control description origin-desc textarea_height").text

            desc_dict['origin'][desc_idx] = origin_desc

        row_descriptions_trans = row_descriptions_trans.find_all('div', class_='row description-div')
        for row_description_tran in row_descriptions_trans:
            tran_idx = row_description_tran.find("div", class_="col-xl-1").text
            tran_desc = row_description_tran.find("textarea", class_="form-control description trans-desc textarea_trans_height").text

            desc_dict['trans'][tran_idx] = tran_desc

        row_claims_origins = row_claims_origins.find_all('div',class_="row claim-div")
        for row_claims_origin in row_claims_origins:
            origin_val = row_claims_origin.find("input", class_="form-control num").attrs['value']
            origin_claims = row_claims_origin.find("textarea", class_="form-control claim origin-claim textarea_height").text

            claim_dict['origin'][origin_val] = origin_claims

        row_claims_trans = row_claims_trans.find_all('div',class_="row claim-div")
        for row_claims_tran in row_claims_trans:
            trans_val = row_claims_tran.find("input", class_="form-control num").attrs['value']
            tran_claims = row_claims_tran.find("textarea", class_="form-control claim trans-claim textarea_height").text

            claim_dict['trans'][trans_val] = tran_claims

        """생성완료"""
        # desc_dict
        # claim_dict

        data_dict[transNum]['desc'] = desc_dict
        data_dict[transNum]['claims'] = claim_dict

        for k, v, in data_dict.items():
            key = k
            v = v['originalNum']

        log_data = f'{key} {v} {time.asctime()} \n'



        print(log_data)

        log_directory = os.path.join(export_root, f'ipaclab_trans_{page_count}_01_log.txt')
        with open(log_directory, 'a+t') as f:
            f.write(log_data)

        # print(data_dict)


# print(f"time:{round(time.time()-start,2)}")

    # print(data_dict)
    # print(data_dict.keys())
    dict_list=[data_dict]
    # print(dict_list)

    # 10페이지씩 savepoint
    print("json.updated and saved")


    directory = os.path.join(export_root, f'ipaclab_trans_{page_count}_01.json')

    with open(directory, 'w', encoding='UTF-8') as fp:
        json.dump(dict_list, fp, indent=4, sort_keys=False, ensure_ascii=False)




#
# export_root = os.path.join(os.getcwd())
# directory = os.path.join(export_root, f'ipaclab_trans_{page_count}_01.json')
# with open(directory, 'w', encoding='UTF-8') as fp:
#     json.dump(dict_list, fp, indent=4, sort_keys=False, ensure_ascii=False)



