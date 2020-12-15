import json
import requests
import tablib
from bs4 import BeautifulSoup
import os
import time
import datetime

class Params:
    """request 필요한 요청정보 클래스"""
    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Content-Type': 'application/json; charset=utf-8',
        'Referer': 'http://ipaclab.ipactory.com:29983/tr_manager/',
        'Accept-Language': 'ko-KR,ko;q=0.9',
    }
    main_params = {
        'is_transcripted': '',  # 작업전체보기
        'is_confirmed': '',  # 컨펌전체보기
        'is_invalid': '',  # 문서오류보기
        'is_reject': '',
        'row_num': '10',
        'cur_page': '1',
    }

    crawling_params = {
        'originalNum': '',
        'transNum': '',
        'idomeIdx': '',
        'return_page': '/tr_manager/main/',
        'row_num': '10',
        'cur_page': ''
    }

class SetParams:
    """파라미터 변경클래스"""
    def __init__(self):
        self.headers = Params().headers
        self.main_params = Params().main_params
        self.crawling_params = Params().crawling_params

    def set_main_params(self, is_transcripted='', is_confirmed='', is_invalid='', is_reject=''):
        """
        크롤링할 검색조건 세팅메소드
        is_transcripted:작업전체보기 (0, 미작업) (1, 작업중) (2, 작업완료)
        is_confirmed: 컨펌전체보기 (0, 미컨펌) (1, 컨펌완료)
        is_invalid: 문서오류전체보기 (0, 정상문서) (1, 오류문서)
        is_reject: 반려 문서보기 (0, 정상문서) (1, 반려문서) (2, 보완문서)
        """

        self.main_params['is_transcripted'] = str(is_transcripted)
        self.main_params['is_confirmed'] = str(is_confirmed)
        self.main_params['is_invalid'] = str(is_invalid)
        self.main_params['is_reject'] = str(is_reject)


        return self.main_params



class Login:
    """
    로그인 정보 관리 클래스
    """
    login_info = {
        'iu_id': 'voucher_admin',
        'password': 'rhksflwk@!@#$',
    }


class BaseScraper:
    """
   메인페이지에서 필요한 파라미터 정보 입력하는 클래스
   """
    session = requests.Session()

    def __init__(self, is_transcripted='', is_confirmed='', is_invalid='', is_reject=''):
        self.login_url = 'http://ipaclab.ipactory.com:29983/tr_manager/login/'
        self.main_url = 'http://ipaclab.ipactory.com:29983/tr_manager/main/'
        self.main_params = SetParams().set_main_params(is_transcripted, is_confirmed, is_invalid, is_reject)

    def login_response(self):
        """로그인 세션 요청메소드
        :return: 메인페이지 html
        """
        res = BaseScraper.session.post(url=self.login_url, data=Login.login_info)
        res = BaseScraper.session.get(url=self.main_url, headers=Params.headers, params=self.main_params)
        soup_main = BeautifulSoup(res.text, 'html.parser')

        return soup_main

class ScriptScraper(BaseScraper):
    """
    번역문 크롤링 클래스
    """
    session = BaseScraper.session


    def __init__(self, is_transcripted='', is_confirmed='', is_invalid='', is_reject=''):

        self.soup_main = BaseScraper(is_transcripted, is_confirmed, is_invalid, is_reject).login_response()
        self.main_params = BaseScraper(is_transcripted, is_confirmed, is_invalid, is_reject).main_params
        self.crawling_params = SetParams().crawling_params
        self.data_dict = {}
        self.total_docs = 0
        self.pages_count = 0


    def get_total_docs(self):
        """전체 페이지 번역문 수 메소드"""
        total_docs = self.soup_main.find('div', class_='card-body').findChildren('div', class_='row')[1].findChildren('span')[0].text.replace('total docs : ', '')
        self.total_docs = int(total_docs)
        return self.total_docs

    def get_pages_count(self):
        """크롤링할 페이지 계산 메소드"""
        total_docs = self.get_total_docs()
        if total_docs % 10 == 0:
            self.pages_count = int(total_docs / 10)
        else:
            self.pages_count = (total_docs // 10) + 1

        return self.pages_count

    def do_crawler(self, start_page=0):
        """페이지 크롤링 메소드"""
        print(f'{self.main_params}')
        self.get_pages_count()
        for page in range(self.pages_count):
            self.main_params['cur_page'] = str(page+1)

            main_url = 'http://ipaclab.ipactory.com:29983/tr_manager/main/'
            res = BaseScraper.session.get(url=main_url, params=self.main_params, headers=Params.headers)
            main_p_soup = BeautifulSoup(res.text, 'html.parser')

            table = main_p_soup.find("table", class_='w3-table-all')
            tr = table.find("tbody").find_all("tr")

            tran_url = 'http://ipaclab.ipactory.com:29983/tr_manager/main/patent_view/'
            print(f'{page + 1}진행중/{self.pages_count}/{len(tr)}')

            self.data_dict = self.script_crawler(tr, self.data_dict, tran_url, page)
            dict_list = [self.data_dict]

            self.save_json(dict_list)


    def script_crawler(self, tr, data_dict, tran_url, page):
        """스크립트 크롤링 메소드"""
        for i, td in enumerate(tr, start=1):  # 해당페이지게시글크롤링진행
            print(f'{page * 10 + i}/{self.total_docs}')
            label_id = td.find_all("label")[0].text
            reviewer = td.find_all("label")[1].text
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

            self.crawling_params['originalNum'] = originalNum
            self.crawling_params['transNum'] = transNum
            self.crawling_params['idomeIdx'] = idomeIdx
            self.crawling_params['cur_page'] = str(page + 1)

            res = BaseScraper.session.get(url=tran_url, params=self.crawling_params, headers=Params.headers)
            trans_soup = BeautifulSoup(res.text, 'html.parser')

            self.data_dict[transNum] = {
                'originalNum': originalNum,
                'is_transcripted': is_transcripted,
                'is_assgined': label_id,
                'reviewer': reviewer,
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

            # row_description and trans
            contents = trans_soup.find_all('div', class_='col-xl-6 w3-border-right info-div')
            desc_dict, claim_dict = self.get_row(contents, desc_dict, claim_dict)

            data_dict[transNum]['desc'] = desc_dict
            data_dict[transNum]['claims'] = claim_dict

            self.save_log(data_dict)


            is_bug_exists = self.is_get_bugs(data_dict=data_dict)
            # print(is_bug_exists)


            if is_bug_exists:
                dataset = self.get_bug_static(data_dict = data_dict)

                self.save_bug_static_xlsx(dataset=dataset)
                print("saved")



        return data_dict

    def get_row(self, contents, desc_dict, claim_dict):
        # desc_origins
        row_descriptions_origins = contents[2]
        row_descriptions_trans = contents[3]
        row_claims_origins = contents[4]
        row_claims_trans = contents[5]

        row_descriptions_origins = row_descriptions_origins.find_all('div', class_='row description-div')
        for row_description_origin in row_descriptions_origins:
            desc_idx = row_description_origin.find("div", class_="col-xl-1").text
            origin_desc = row_description_origin.find("textarea",
                                                      class_="form-control description origin-desc textarea_height").text

            desc_dict['origin'][desc_idx] = origin_desc

        row_descriptions_trans = row_descriptions_trans.find_all('div', class_='row description-div')
        for row_description_tran in row_descriptions_trans:
            tran_idx = row_description_tran.find("div", class_="col-xl-1").text
            tran_desc = row_description_tran.find("textarea",
                                                  class_="form-control description trans-desc textarea_trans_height").text

            desc_dict['trans'][tran_idx] = tran_desc

        row_claims_origins = row_claims_origins.find_all('div', class_="row claim-div")
        for row_claims_origin in row_claims_origins:
            origin_val = row_claims_origin.find("input", class_="form-control num").attrs['value']
            origin_claims = row_claims_origin.find("textarea",
                                                   class_="form-control claim origin-claim textarea_height").text

            claim_dict['origin'][origin_val] = origin_claims

        row_claims_trans = row_claims_trans.find_all('div', class_="row claim-div")
        for row_claims_tran in row_claims_trans:
            trans_val = row_claims_tran.find("input", class_="form-control num").attrs['value']
            tran_claims = row_claims_tran.find("textarea", class_="form-control claim trans-claim textarea_height").text

            claim_dict['trans'][trans_val] = tran_claims

        return desc_dict, claim_dict

    def save_log(self, data_dict):
        """log파일 저장 메소드"""
        today = datetime.date.today().isoformat()

        for k, v in data_dict.items():
            key = k
            v = v['originalNum']

        log_data = f'{key} {v} {time.asctime()} \n'


        log_directory = os.path.join(os.getcwd(), f'json/ipaclab_trans_{self.pages_count}_{today}_log.txt')
        with open(log_directory, 'a+t') as f:
            f.write(log_data)

    def save_json(self, dict_list):
        """json파일 저장 메소드"""
        today = datetime.date.today().isoformat()
        directory = os.path.join(os.getcwd(), f'json/ipaclab_trans_{self.pages_count}_{today}.json')
        with open(directory, 'w', encoding='UTF-8') as fp:
            json.dump(dict_list, fp, indent=4, sort_keys=False, ensure_ascii=False)

        print("json.updated and saved")

        """원문, 번역문 추출 메소드"""


    def save_bug_static_xlsx(self, dataset):
        today = datetime.date.today().isoformat()
        export_path = os.path.join(os.getcwd(), f'statistic/ipaclab_bugs_check_{today}.xlsx')
        dataset = dataset

        with open(export_path, 'wb') as f_output:
            f_output.write(dataset.export('xlsx'))



# class BugCheck:
#     """번역문과 원문의 갯수 차이가 있는 번역문을 확인하는 클래스"""
#     def __init__(self):
#         """버그번역문을 리스트에 담는 설정 """
#         self. is_bug_exists = []

    def is_get_bugs(self, data_dict=None):
        """
        버그가 존재하는 tranNum keys를 리스트로 리턴함
        총 갯수의 일치여부로 버그를 판단
        """
        for key, value in data_dict.items():
            is_bug_exists = False
            tran_num = key

            desc_origin_counts = len(data_dict[tran_num]['desc']['origin'])
            desc_trans_counts = len(data_dict[tran_num]['desc']['trans'])
            claims_origin_counts = len(data_dict[tran_num]['claims']['origin'])
            claims_trans_counts = len(data_dict[tran_num]['claims']['trans'])

            is_bug_exists = True if desc_origin_counts != desc_trans_counts or claims_origin_counts != claims_trans_counts else False

            # if is_bug_exists:
            #     # is_bug_exists.append(tran_num)

        return is_bug_exists


    def get_bug_static(self, data_dict):
        """작업상태에 따른 버그번역문 정보 리턴 메서드"""
        headers = ['순번', '원문번호1', '원문번호2', 'desc차이', 'claims차이', '작업자ID', '검수자 ID']
        dataset = tablib.Dataset(headers=headers)
        idx = 0

        for key, value in self.data_dict.items():
            desc_origins = len(value['desc']['origin'].values())
            desc_trans = len(value['desc']['trans'].values())
            claims_origins = len(value['claims']['origin'].values())
            claims_trans = len(value['claims']['trans'].values())
            # desc차이
            desc_subs = abs(desc_origins - desc_trans) if desc_origins != desc_trans else 0
            # claim차이
            claims_subs = abs(claims_origins - claims_trans) if claims_origins != claims_trans else 0
            # 순번
            idx += 1
            # 원문번호1
            tran_num = key
            # 원문번호2
            original_num = value['originalNum']
            # 작업자 ID
            voucher = value['is_assgined']
            # 검수자 ID
            reviewer = value['reviewer']

            dataset.append([
                idx,
                tran_num,
                original_num,
                desc_subs,
                claims_subs,
                voucher,
                reviewer
            ])

        return dataset



def main():
    """여기다가 코드 작성하세요~"""
    c1 = ScriptScraper(is_confirmed=1)
    c1.do_crawler(start_page=0)


if __name__ == '__main__':
    main()



