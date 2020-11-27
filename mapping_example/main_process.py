import os, tablib, sys

#initialization
import random
import time
from pathlib import Path

data_list = []
data_dict = {}

def change_dir_name_to_number():
    try:
        dir_name = str(input('변경할 디렉토리의 파일명을 입력하세요\n>'))
        meta_data_name = str(input('검색할 엑셀파일의 이름을 입력하세요(확장자 명은 생략)\n> '))
        # meta_data_name = 'meta_data'
        base_path = os.getcwd()
        dir_path = os.path.join(base_path + f'\\{dir_name}')
        # new_dir_path = os.path.join(dir_path + '_new')
        meta_data_path = os.path.join(base_path + f'\\{meta_data_name}.xlsx')
        meta_data = open(meta_data_path, 'rb')
        meta_data = tablib.Dataset().load(meta_data.read(), format='xlsx')

        for header in meta_data.headers:
            data_list.append(header)

        for datas in meta_data:
            for data in datas:
                if data == None:
                    pass
                else:
                    data_list.append(data)

        for i, index in enumerate(data_list,start=1):
            # 짝수번째 인덱스면 숫자
            if i%2 != 0:
                data_dict[index] = data_list[i]


        # print(data_list)
        print(len(data_dict))
        # print(data_dict)


        # Check Directory list
        for i, fn in enumerate(os.listdir(dir_path), start= 1):

            for k, v in data_dict.items():
                # print(fn)
                if k == fn:
                    print(os.path.join(dir_path , fn))
                    os.rename(os.path.join(dir_path, fn), os.path.join(dir_path, v))

                
                else:
                    pass
                
        print("done")



    except FileNotFoundError:
        print("'파일명'을 '정확'하게 입력을 해주세요\n"
              "프로그램을 종료합니다.")



def sort_file_names():
    try:
        dir_name = str(input('변경할 디렉토리의 파일명을 입력하세요\n>'))
        # meta_data_name = str(input('오름차순으로 정렬하시겠습니까?(y/n)\n> ')).upper()

        base = os.getcwd()
        # os.mkdir(os.path.join(base, dir_name))
        dir_path = os.path.join(base,dir_name)
        total = len(os.listdir(dir_path))

        for i, fn in enumerate(os.listdir(dir_path), start=1):
            try:
                fn = Path(fn)
                suffix = fn.suffix
                os.rename(os.path.join(dir_path, fn), os.path.join(dir_path, str(i)+suffix))

                print(f' 현재 진행률:  {i} / {total}' )
            except FileExistsError:
                print("파일이름이 기존에 존재합니다.")
                pass
        print("==================================\n\n\n\n")
        print("파일이름 변경 완료!!!")


    except FileNotFoundError:
        print("경로상의 파일을 찾지 못했습니다.")








def main_processor():
    run_module = str(input("실행할 프로그램을 선택해주세요\n"
                       "['파일이름 정렬: 1']\n"
                       "['베트남어 디렉토리 변경: 2']\n>"))

    try:
        if run_module == '1':
            print("프로그램을 시작합니다...")
            time.sleep(2)
            sort_file_names()

        elif run_module == '2':
            print("프로그램을 시작합니다...")
            time.sleep(2)
            change_dir_name_to_number()



    except KeyError:
        print("올바르게 입력해주세요~ ")



# main_processor()


