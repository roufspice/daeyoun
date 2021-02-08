

"""외장하드 파일 지우고, 옮기고, 이름 바꾸고 """

def del_true_metrix_hdd():
    not_delete_dataset = tablib.Dataset(headers=['frames'])

    meta_data_path = os.path.join(os.getcwd(), 'metrid_hdd_CAT_DOG.xlsx')

    hdd_root_path_cat_frames = '/mnt/metrix_hdd/PASS/CAT/_frames'
    hdd_root_path_dog_frames = '/mnt/metrix_hdd/PASS/DOG/_frames'

    if os.path.exists(meta_data_path):
        f = open(meta_data_path, 'rb')

        databook = tablib.import_book(f, format='xlsx')
        sheets = databook.sheets()

        cat_frames_dataset = sheets[0]
        dog_frames_dataset = sheets[1]

        del_cat_frames = [frame[1] for frame in cat_frames_dataset if frame[0] == True]
        del_dog_frames = [frame[1] for frame in dog_frames_dataset if frame[0] == True]

        cat_dirs = os.listdir(hdd_root_path_cat_frames)
        dog_dirs = os.listdir(hdd_root_path_dog_frames)

        for cat in del_cat_frames:
            cat_dir_path = os.path.join(hdd_root_path_cat_frames, cat)
            if os.path.exists(cat_dir_path):
                shutil.rmtree(cat_dir_path)
                print(cat)


            else:
                not_delete_dataset.append([
                    cat
                ])



        for dog in del_dog_frames:
            dog_dir_path = os.path.join(hdd_root_path_dog_frames, dog)
            if os.path.exists(dog_dir_path):
                shutil.rmtree(dog_dir_path)
                print(dog)
            else:
                not_delete_dataset.append([
                    dog
                ])



def get_list_metrix_ccd():
    ccd_root_path = f'/mnt/metrix_hdd/PASS'
    data_book = tablib.Databook()
    # Dog
    headers_cat_frames = ['CAT_frames']
    headers_dog_frames = ['DOG_frames']
    headers_cat_json = ['DOG_frames']
    headers_dog_json = ['DOG_frames']

    dataset_cat_frames = tablib.Dataset(title='CAT_frames', headers=headers_cat_frames)
    dataset_dog_frames = tablib.Dataset(title='DOG_frames', headers=headers_dog_frames)
    dataset_cat_json = tablib.Dataset(title='CAT_json', headers=headers_cat_json)
    dataset_dog_json = tablib.Dataset(title='DOG_json', headers=headers_dog_json)


    cat_frames_path = os.path.join(ccd_root_path, 'CAT/_frames/')
    dog_frames_path = os.path.join(ccd_root_path, 'DOG/_frames/')
    cat_json_path = os.path.join(ccd_root_path, 'CAT/_json/')
    dog_json_path = os.path.join(ccd_root_path, 'DOG/_json/')
    cat_json_path = Path(cat_json_path)
    dog_json_path = Path(dog_json_path)

    if os.path.exists(cat_frames_path) and os.path.exists(dog_frames_path):
        dir_cat_list = os.listdir(cat_frames_path)
        dir_dog_list = os.listdir(dog_frames_path)
        for cat, dog in zip(dir_cat_list, dir_dog_list):
            dataset_cat_frames.append([
                cat
            ])
            dataset_dog_frames.append([
                dog
            ])

    data_book.add_sheet(dataset_cat_frames)
    data_book.add_sheet(dataset_dog_frames)

    if cat_json_path.exists() and dog_json_path.exists():
        dir_cat_list = cat_json_path.rglob("*.json")
        dir_dog_list = dog_json_path.rglob("*.json")
        for cat, dog in zip(dir_cat_list, dir_dog_list):
            dataset_cat_json.append([
                cat
            ])
            dataset_dog_json.append([
                dog
            ])

    data_book.add_sheet(dataset_cat_json)
    data_book.add_sheet(dataset_dog_json)

    directory = os.path.join(os.getcwd())
    with open(os.path.join(directory, f'metrid_hdd_CAT_DOG.xlsx'), 'wb') as f:
        f.write(data_book.export(format='xlsx'))



def set_rename_cdd(name):
    """외장하드 이름 바꾸기 """
    # meta_data
    dataset = {}
    changed_dir = tablib.Dataset(headers=['original frame folder name'])
    meta_data_path = os.path.join(os.getcwd(), '동작변경내역_데이터메이커_메트릭스작성.xlsx')
    meta_data_path = Path(meta_data_path)
    if meta_data_path.exists():
        f = open(meta_data_path, 'rb')
        meta_data = tablib.import_set(f.read(), format='xlsx')
        original_frame_fn = meta_data['original frame folder name']
        modified_frame_fn = meta_data['modified frame folder name']

        for origin_fn, modified_fn in zip(original_frame_fn, modified_frame_fn):
            dataset[origin_fn] = modified_fn

    """외장하드 이름 바꾸기 """
    ccd_root_cat_path = f'/mnt/metrix_hdd/PASS/{name}/_frames'
    if os.path.exists(ccd_root_cat_path):
        dir_list = os.listdir(ccd_root_cat_path)
        for dir_ in dir_list:

            try:

                origin_dir = os.path.join(ccd_root_cat_path, dir_)
                new_dir = os.path.join(ccd_root_cat_path, dataset[dir_])
                print(new_dir)
                if os.path.exists(new_dir):
                    pass
                else:
                    shutil.move(origin_dir, new_dir)
            except KeyError:
                changed_dir.append([
                    dir_
                ])

                continue

    with open(os.path.join(os.getcwd(), f'외장하드_폴더이름 변경 리스트_{name}(1).xlsx'), 'wb') as f:
        f.write(changed_dir.export('xlsx'))





