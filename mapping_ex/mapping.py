import os
import tablib
import time
from pathlib import Path

class Mapping:

    def __init__(self, dir_name):

        self.dir_name = dir_name


    def dir_name_to_number(self):
        try:

            dir_name = self.dir_name
            meta_data_name = str(input('검색할 엑셀파일의 이름을 입력하세요(확장자 명은 생략)\n> '))
            base_path = os.getcwd()
            dir_path = os.path.join(base_path + f'\\{dir_name}')
            meta_data_path = os.path.join(base_path + f'\\{meta_data_name}.xlsx')

            meta_data = open(meta_data_path, 'rb')
            meta_data = tablib.Dataset().load(meta_data.read(), format='xlsx')

            data_list = []
            data_dict = {}

            for header in meta_data.headers:
                data_list.append(header)

            for datas in meta_data:
                for data in datas:
                    if data == None:
                        pass
                    else:
                        data_list.append(data)

            for i, index in enumerate(data_list, start=1):
                # 짝수번째 인덱스면 숫자
                if i % 2 != 0:
                    data_dict[index] = data_list[i]

            print(len(data_dict))

            # Check Directory list
            for i, fn in enumerate(os.listdir(dir_path), start=1):
                for k, v in data_dict.items():
                    if k == fn:
                        print(os.path.join(dir_path, fn))
                        os.rename(os.path.join(dir_path, fn), os.path.join(dir_path, v))


                    else:
                        pass
            print("done")


        except FileNotFoundError:
            print("'파일명'을 '정확'하게 입력을 해주세요\n"
                  "프로그램을 종료합니다.")

    def sort_files(self):
        try:
            dir_name = str(input('변경할 디렉토리의 파일명을 입력하세요\n>'))
            base = os.getcwd()
            dir_path = os.path.join(base, dir_name)
            total = len(os.listdir(dir_path))
            print(total)
            time.sleep(0.1)

            for j, fn_upper in enumerate(os.listdir(dir_path), start=1):
                dir_path_detail = os.path.join(dir_path, fn_upper)
                print("\n\n==================")
                print(fn_upper + '진행중...\t찾은파일개수: ', len(os.listdir(dir_path_detail)))

                for i, fn in enumerate(os.listdir(dir_path_detail)):
                    fn = Path(fn)
                    suffix = fn.suffix
                    hash_num = i*156166845 /3.51
                    is_exist = os.path.exists(os.path.join(dir_path_detail, str(i) + suffix))
                    if is_exist:
                        os.rename(os.path.join(dir_path_detail, fn), os.path.join(dir_path_detail, str(hash_num) + suffix))
                    else:
                        os.rename(os.path.join(dir_path_detail, fn), os.path.join(dir_path_detail, str(hash_num) + suffix))

                for i, fn in enumerate(os.listdir(dir_path_detail)):
                    fn = Path(fn)
                    suffix = fn.suffix
                    is_exist = os.path.exists(os.path.join(dir_path_detail, str(i) + suffix))
                    if is_exist:
                        print(f' 동일한 이름의 파일이 존재합니다. {i+1} / {len(os.listdir(dir_path_detail))}')
                        os.rename(os.path.join(dir_path_detail, fn), os.path.join(dir_path_detail, str(i) + suffix))
                    else:
                        os.rename(os.path.join(dir_path_detail, fn), os.path.join(dir_path_detail, str(i) + suffix))
                        print(f'이름 변경완료 {i + 1} / {len(os.listdir(dir_path_detail))}')
        except FileNotFoundError:
            print("디렉토리 안에 변경할 디렉토리 또는 파일이 없습니다.")



    def main_processor(self):
        run_module = str(input("실행할 프로그램을 선택해주세요\n"
                               "['파일이름 정렬: 1']\n"
                               "['베트남어 디렉토리 변경: 2']\n>"))

        try:
            if run_module == '1':
                print("프로그램을 시작합니다...")
                time.sleep(2)
                self.sort_files()

            elif run_module == '2':
                print("프로그램을 시작합니다...")
                time.sleep(2)
                self.dir_name_to_number()



        except KeyError:
            print("올바르게 입력해주세요~ ")



