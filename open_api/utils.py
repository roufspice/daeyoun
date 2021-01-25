import requests
import json
from nanoid import generate
from datetime import datetime
from django.conf import settings

TOKEN_URL = "https://testapi.openbanking.or.kr/oauth/2.0/token"
API_URL = "https://testapi.openbanking.or.kr/v2.0/inquiry/real_name"

# TODO 오픈api 기능테스트 testapi

def openbanking_accounts_validator(bank_code, bank_account, date_birth):

    tran_dtime = datetime.now()
    token_url = TOKEN_URL
    client_id = settings.OPEN_BANKING_API_KEY
    client_secret = settings.OPEN_BANKING_API_SECRET
    access_token = get_access_token(token_url, client_id, client_secret)

    data = {
        "bank_tran_id": get_bank_tran_id(),
        "bank_code_std": bank_code,
        "account_num": bank_account,
        "account_holder_info": date_birth,
        "tran_dtime": tran_dtime.strftime('%Y%m%d%H%M%S'),
    }

    account_rsp = requests.post(url=API_URL, headers=get_api_headers(access_token), data=json.dumps(data)).json()
    rsp_code = account_rsp['rsp_code']
    is_valid = False
    if rsp_code == "A0000":
        is_valid = True
    return is_valid




def get_access_token(token_url, client_id, client_secret):
    res_token = requests.post(url=token_url,
                              headers = get_token_headers(),
                              data= get_token_params(client_id, client_secret)).json()

    return res_token['access_token']

def get_token_headers():
    return {
        "Content-Type": "application/x-www-form-urlencoded",
    }

def get_api_headers(access_token):
    return {
        "Authorization": f"Bearer {str(access_token)}",
        "Content-Type": "application/json; charset=UTF-8",
    }

def get_token_params(client_id, client_secret):
    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "oob",
    }

def get_bank_tran_id():
    """은행 고유번호 생성 메소드"""
    client_use_code = settings.CLIENT_USE_CODE
    datamaker_tran_num = f"DM{generate('0123456789', 6)}{generate('ABCDEFG', 1)}"
    return client_use_code + datamaker_tran_num


def get_bank_name():
    pass


#forms > BankAccountForm
def clean(self):
    # TODO: OpenBanking Test
    cleaned_data = super().clean()

    print(cleaned_data)
    bank_code = cleaned_data['name']
    bank_account = cleaned_data['number']
    date_birth = self.user.date_birth.strftime("%y%m%d")

    is_accounts_vaild = openbanking_accounts_validator(bank_code, bank_account, date_birth)

    if not is_accounts_vaild:
        self.add_error('number', f'입력하신 계좌정보를 조회할 수 없습니다.\n'
                                 f'\n다시 입력해주세요.')
    return cleaned_data