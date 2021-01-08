import requests

# 사용자 OAuth 인증
base_url = "https://testapi.openbanking.or.kr/oauth/2.0/authorize"

params = {
    'response_type': 'code',
    'client_id': 'C27rr1JMq42uoQUUX2akV5sG5EDl9lba6MZ1k2a4',
    'redirect_uri': 'http://dashboard.datamaker.io:8500/payment/bank_accounts/update/',
    'state': 98765432109876543210987654321098,
    'scope': 'login',
    'auth_type': 0,
}

res = requests.get(base_url, params=params)
print(res.text)

