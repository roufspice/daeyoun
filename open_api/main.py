import requests, json

# 사용자 OAuth 인증
from bs4 import BeautifulSoup
from nanoid import generate
from datetime import datetime


def openApi_test():
    # 2_legged_request
    token_url = "https://testapi.openbanking.or.kr/oauth/2.0/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "client_id": "C27rr1JMq42uoQUUX2akV5sG5EDl9lba6MZ1k2a4",
        "client_secret": "q1pxdiiVT7w66nj3IcXRx1xd40CRHqG7bbdwuLzr",
        "grant_type": "client_credentials",
        "scope": "oob",

    }

    res_token = requests.post(url=token_url, headers=headers, data=data).json()

    access_token = res_token['access_token']
    print(access_token)
    # 3_계좌실명조회_API
    account_valid_url = "https://testapi.openbanking.or.kr/v2.0/inquiry/real_name"

    account_headers = {
        "Authorization": f"Bearer {str(access_token)}",
        "Content-Type": "application/json; charset=UTF-8",

    }
    # TODO bank_tran_id 값 자동설정!
    client_use_code = "T990038640U"
    datamaker_tran_num = f"DM{generate('0123456789', 6)}{generate('ABCDEFG', 1)}"
    bank_tran_id = client_use_code + datamaker_tran_num
    tran_dtime = datetime.now()
    current_dtime = tran_dtime.strftime('%Y%m%d%H%M%S')

    print(bank_tran_id)

    data = {
        "bank_tran_id": bank_tran_id,
        "bank_code_std": "003",
        "account_num": "9876543210987654",
        "account_holder_info": "000101",
        "tran_dtime": current_dtime,
    }

    account_res = requests.post(url=account_valid_url, headers=account_headers, data=json.dumps(data)).json()

    print(account_res)

    return res_token


if __name__ == '__main__':
    openApi_test()
