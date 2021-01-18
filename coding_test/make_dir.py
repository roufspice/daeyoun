import os
from pathlib import Path

def make_directory():
    root_path = os.getcwd()
    root_path = Path(root_path)
    dir_name = 'test_02/detail_01'
    mk_path = root_path.joinpath(dir_name)
    mk_path.mkdir(exist_ok=True, parents=True)
    # mk_path.mkdir(exist_ok=True)


def make_file(path):
    if Path.exists(path):
        os.path.isfile(file_path) if file_path else False



if __name__ == '__main__':

    root_path = Path(os.getcwd())
    make_file(root_path)
    # make_directory()