import urllib
import requests
import selenium
import os
import sys
import time
import getpass
import msvcrt
import tablib
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


















search_list = ['블로그마켓', '공구', '도매', '인생템', '여자쇼핑몰', '남자쇼핑묠', '마켓오픈']



# 검색어 입력
search_keyword = search_list[0]
search = str(search_keyword)
search = urllib.parse.quote(search)
base_url = f'https://www.instagram.com/explore/tags/{search}/'
login_url = f'https://www.instagram.com/accounts/login/'

# information_definition
user_name = str(input('전화번호, 사용자 이름 또는 이메일\n>'))




# user_pw = getpass.getpass('password:')
user_pw = str(input('비밀번호 \n>'))
user_pw_confirm = str(input('비밀번호 재확인\n>'))
hash_tag = '해쉬태그'
has_link = f'//a[@href="/explore/tags/{hash_tag}/"]'




#input login_information
def main():

    if user_pw == user_pw_confirm:
        base = os.getcwd()
        driver = webdriver.Chrome(
            os.path.join(base + '\\chromedriver.exe'))  # Optional argument, if not specified will search path.
        driver.get(login_url)

        time.sleep(5)
        driver.find_element_by_name('username').send_keys(user_name)
        driver.find_element_by_name('password').send_keys(user_pw)
        time.sleep(3)
        # click login 버튼
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').submit()
        # //*[@id="react-root"]/section/main/div/div/div/div/button
        # //*[@id="react-root"]/section/main/div/div/div/section/div/button
        # alert_accept(driver) # 팝업창 발생
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').submit()
        # 옵션 추가

        time.sleep(10)
        driver.quit()

    else:
        print("비밀번호가 일치하지 않습니다.")
        print("다시 시작해주세요")



def alert_accept(driver):
    da = Alert(driver)

    return da.accept()




if __name__ == "__main__":
    main()

# SCROLL_PAUSE_TIME = 1.2  #인스타게시물 스크롤 속도 조절 ( 1.0 ~ 2.0까지 사양에 맞게 조절 )


# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!

