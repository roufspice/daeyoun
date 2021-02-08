import requests

base_url = 'https://www.sothebys.com/en/search-results.html'
rsp = requests.get(base_url)
print(rsp.status_code)