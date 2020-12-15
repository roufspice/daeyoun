import os
from pathlib import Path
import tablib
import sys

# 어떤 파일이 있든 정리가 가능하면 된다.


class FileOrder:
    hash_num = 1382123
    """파일이름을 정렬해주는 클래스"""
    def __init__(self, dir):
        """해당 디렉토리의 경로를 설정"""
        self.dir = Path(dir)
        self.data_list = []
        self.data_dict = {}


class SortFileName(FileOrder):
    def __init__(self, dir):
        super().__init__(dir)

    def sort_file_names(self):
        """해당 디렉토리내의 모든 파일 이름을 0부터 순서대로 정렬해주는 메소드"""
        try:
            if self.dir.exists():
                base_path = self.dir
                sub_directory_counts = len(os.listdir(base_path))

                # 하단 디렉토리 탐색
                for f, sub_dir in enumerate(os.listdir(base_path), start =1):
                    sub_path = base_path/sub_dir

                    #디렉토리 내 파일 탐색
                    for i, fn in enumerate(os.listdir(sub_path), start=1):
                        fn = Path(fn)
                        suffix = fn.suffix
                        hash_num = FileOrder.hash_num * i / 3.5

                        is_exist = os.path.exists(os.path.join(sub_path, str(i) +suffix))
                        if is_exist:
                            os.rename(os.path.join(sub_path, fn), os.path.join(sub_path, str(hash_num) + suffix))

                        else:
                            os.rename(os.path.join(sub_path, fn),os.path.join(sub_path, str(hash_num) + suffix))


                    for i, fn in enumerate(os.listdir(sub_path) ,start=1):
                        fn = Path(fn)
                        suffix = fn.suffix

                        is_exist = os.path.exists(os.path.join(sub_path, str(i) + suffix))
                        if is_exist:
                            print(f' 동일한 이름의 파일이 존재합니다. {i + 1} / {len(os.listdir(sub_path))}')

                            os.rename(os.path.join(sub_path, fn), os.path.join(sub_path, str(i) + suffix))
                        else:
                            os.rename(os.path.join(sub_path, fn), os.path.join(sub_path, str(i) + suffix))
                            print(f'이름 변경완료 {i + 1} / {len(os.listdir(sub_path))}')



            else:
                print("경로가 올바르지 않습니다.")

        except FileNotFoundError as e:
            print(e)



dir = os.path.join(os.getcwd(), 'result_test')

c1 = SortFileName(dir)
c1.sort_file_names()