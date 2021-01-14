import json
import requests
import tablib
from bs4 import BeautifulSoup
import os
import time
import datetime
from ipaclab.base_crawler import BaseScraper,Params,SetParams,Login




class ScriptScraper(BaseScraper):
    """
    번역문 크롤링 클래스
    """
    session = BaseScraper.session

    def __init__(self, is_transcripted='', is_confirmed='', is_invalid='', is_reject='', is_assigned=''):

        self.soup_main = BaseScraper(is_transcripted, is_confirmed, is_invalid, is_reject, is_assigned).login_response()
        self.main_params = BaseScraper(is_transcripted, is_confirmed, is_invalid, is_reject, is_assigned).main_params
        self.crawling_params = SetParams().crawling_params
        self.data_dict = {}
        self.total_docs = 0
        self.pages_count = 0

    def get_total_docs(self):
        """전체 페이지 번역문 수 메소드"""
        total_docs = \
        self.soup_main.find('div', class_='card-body').findChildren('div', class_='row')[1].findChildren('span')[
            0].text.replace('total docs : ', '')
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
        headers = ['순번', '원문번호1', '원문번호2', 'desc차이', 'claims차이', '작업자ID', '검수자 ID', '작업상태']
        dataset = tablib.Dataset(headers=headers)

        for page in range(self.pages_count):
            self.main_params['cur_page'] = str(page + 1)

            main_url = 'http://ipaclab.ipactory.com:29983/tr_manager/main/'
            res = BaseScraper.session.get(url=main_url, params=self.main_params, headers=Params.headers)
            main_p_soup = BeautifulSoup(res.text, 'html.parser')

            table = main_p_soup.find("table", class_='w3-table-all')
            tr = table.find("tbody").find_all("tr")

            tran_url = 'http://ipaclab.ipactory.com:29983/tr_manager/main/patent_view/'
            print(f'{page + 1}진행중/{self.pages_count}/{len(tr)}')

            self.data_dict, dataset = self.script_crawler(tr, self.data_dict, tran_url, page, dataset)
            dict_list = [self.data_dict]

            self.save_json(dict_list)
            self.save_bug_static_xlsx(dataset)





    def script_crawler(self, tr, data_dict, tran_url, page, dataset):
        """스크립트 크롤링 메소드"""
        for i, td in enumerate(tr, start=1):  # 해당페이지게시글크롤링진행
            print(f'현재 번역문: {page * 10 + i}/{self.total_docs}')
            #TODO 크롤링 목록 IDX 추가
            idx = td.find("td", class_="org-no").text

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
                'idx': idx,
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

            is_bug_exists = False
            data_dict_transNum = data_dict[transNum]
            # self.is_get_bugs(data_dict=data_dict)
            is_bug_exists = self.is_get_bugs(data_dict=data_dict_transNum)
            # print(is_bug_exists)
            if is_bug_exists:

                value_list = self.get_bug_static(data_dict=data_dict_transNum, transNum=transNum)
                dataset.append(value_list)

        return data_dict, dataset

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

    def is_get_bugs(self, data_dict=None):
        """
        버그가 존재하는 tranNum keys를 리스트로 리턴함
        총 갯수의 일치여부로 버그를 판단
        """

        desc_origin_counts = len(data_dict['desc']['origin'])
        desc_trans_counts = len(data_dict['desc']['trans'])
        claims_origin_counts = len(data_dict['claims']['origin'])
        claims_trans_counts = len(data_dict['claims']['trans'])
        is_bug_exists = True if desc_origin_counts != desc_trans_counts or claims_origin_counts != claims_trans_counts else False


        return is_bug_exists

    def get_bug_static(self, data_dict, transNum):
        """작업상태에 따른 버그번역문 정보 리턴 메서드"""


        # for key, value in self.data_dict.items():
        desc_origins = len(data_dict['desc']['origin'].values())
        desc_trans = len(data_dict['desc']['trans'].values())
        claims_origins = len(data_dict['claims']['origin'].values())
        claims_trans = len(data_dict['claims']['trans'].values())
        # desc차이
        desc_subs = abs(desc_origins - desc_trans) if desc_origins != desc_trans else 0
        # claim차이
        claims_subs = abs(claims_origins - claims_trans) if claims_origins != claims_trans else 0
        # 순번
        idx = data_dict['idx']
        # 원문번호1
        tran_num = transNum
        # 원문번호2
        original_num = data_dict['originalNum']
        # 작업자 ID
        voucher = data_dict['is_assgined']
        # 검수자 ID
        reviewer = data_dict['reviewer']
        # 작업상태
        is_transcripted = data_dict['is_transcripted']

        value_list = [idx, tran_num, original_num, desc_subs, claims_subs, voucher, reviewer, is_transcripted]

        return value_list


def main():
    """여기다가 코드 작성하세요~"""
    c1 = ScriptScraper(is_transcripted=2, is_assigned='voucher16')
    c1.do_crawler(start_page=0)


if __name__ == '__main__':
    main()
