import tablib, bs4, requests, urllib, json, os, sys, keyboard


from Swindow_crawler_copy import run_swindow_crawler
from Wconcept_crawler_copy import run_wconcept_crawller
from WIZWID_crawler_copy import run_wizwid_crawl
from YOOX_crawler_copy import run_Yook_crawller
from FARFETCH_crawler_copy import run_farfetch_crawler

# from Swindow_crawler import run_swindow_crawler
# from Wconcept_crawler import run_wconcept_crawller
# from WIZWID_crawler import run_wizwid_crawl
# from YOOX_crawler import run_Yook_crawller
# from FARFETCH_crawler import run_farfetch_crawler


opt_01 = '네이버쇼핑(Swindow)'
opt_02 = 'W컨셉(Wconcept)'
opt_03 = '위즈위드(Wizwid)'
opt_04 = '육스닷컴(Yoox)'
opt_05 = '파페치(Farfetch)'

info = "아래의 항목을 보고 크롤링할 사이트의 해당 '번호'를 입력해주세요\n" \
       "-------------------------------------------\n"
start_command = 0


def start_command_input():
    while True:
        try:

            print("올바른 작동을 위해 아래와 같은 명령어를 입력해주세요.\n")
            print(info)
            print(f'[1] : {opt_01}\n'
                  f'[2] : {opt_02}\n'
                  f'[3] : {opt_03}\n'
                  f'[4] : {opt_04}\n'
                  f'[5] : {opt_05}\n'
                 )
            start_command = int(input('>'))
            break


        except ValueError:
            print("입력한 값이 올바르지 않습니다.")


    return start_command


def start_command_confirmed():

    start_command = start_command_input()
    try:


        if start_command == 1:
            print(f"'{opt_01}' 을(를)크롤링 시작합니다.")
            run_swindow_crawler()

        elif start_command ==2:
            print(f"'{opt_02}' 을(를)크롤링 시작합니다.")
            run_wconcept_crawller()

        elif start_command ==3:
            print(f"'{opt_03}' 을(를)크롤링 시작합니다.")
            run_wizwid_crawl()

        elif start_command ==4:
            print(f"'{opt_04}' 을(를)크롤링 시작합니다.")
            run_Yook_crawller()

        elif start_command == 5:
            print(f"'{opt_05}' 을(를)크롤링 시작합니다.")
            run_farfetch_crawler()

        else:
            print("입력한 값이 올바르지 않습니다.")
            start_command_input()


    except ValueError as e:
        print("입력한 값이 올바르지 않습니다.")


start_command_confirmed()