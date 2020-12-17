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
        'is_assigned': '',  # 작업자할당
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

    def set_main_params(self, is_transcripted='', is_confirmed='', is_invalid='', is_reject='', is_assigned=''):
        """
        크롤링할 검색조건 세팅메소드
        is_assigned: 작업자체크(voucher00)
        is_transcripted:작업전체보기 (0, 미작업) (1, 작업중) (2, 작업완료)
        is_confirmed: 컨펌전체보기 (0, 미컨펌) (1, 컨펌완료)
        is_invalid: 문서오류전체보기 (0, 정상문서) (1, 오류문서)
        is_reject: 반려 문서보기 (0, 정상문서) (1, 반려문서) (2, 보완문서)
        """

        self.main_params['is_transcripted'] = str(is_transcripted)
        self.main_params['is_confirmed'] = str(is_confirmed)
        self.main_params['is_invalid'] = str(is_invalid)
        self.main_params['is_reject'] = str(is_reject)
        self.main_params['is_assigned'] = str(is_assigned)

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

    def __init__(self, is_transcripted='', is_confirmed='', is_invalid='', is_reject='', is_assigned=''):
        self.login_url = 'http://ipaclab.ipactory.com:29983/tr_manager/login/'
        self.main_url = 'http://ipaclab.ipactory.com:29983/tr_manager/main/'
        self.main_params = SetParams().set_main_params(is_transcripted, is_confirmed, is_invalid, is_reject,
                                                       is_assigned)

    def login_response(self):
        """로그인 세션 요청메소드
        :return: 메인페이지 html
        """
        res = BaseScraper.session.post(url=self.login_url, data=Login.login_info)
        res = BaseScraper.session.get(url=self.main_url, headers=Params.headers, params=self.main_params)
        soup_main = BeautifulSoup(res.text, 'html.parser')

        return soup_main