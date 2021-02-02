def re_build_json():
    """json파일 재 빌드하기"""
    meta_data_path = os.path.join(os.getcwd(), 'movement_meta_data.xlsx')
    if os.path.exists(meta_data_path):
        f =open(meta_data_path, 'rb')
        meta_data = tablib.import_set(f.read(), format='xlsx')
        origin_fn = meta_data['original file name']
        modified_fn = meta_data['modified file name']
        actions = meta_data['metadata_action']


    json_path = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/공유_Data_Export/')
    json_paths_list = Path(json_path).rglob("*.json")
    count = 0
    is_file = False
    for json_path in json_paths_list:
        if is_file:
            break
        for fn, m_fn, act in zip(origin_fn, modified_fn, actions):
            if str(fn) in str(json_path):
                with open(json_path, encoding='utf-8') as f:
                        f_json = json.load(f)
                # file_video
                file_video = f_json['file_video']
                file_video = file_video.replace(fn, m_fn)
                f_json['file_video'] = file_video
                # print(f_json)
                #action
                f_json['metadata']['action'] = act

                #FILENAME
                root_path = json_path.parents[1]
                dir_path = root_path / fn
                print(dir_path)
                #root_path
                new_dir_path = root_path / m_fn
                # print(new_dir_path)
                file_name = json_path.name.replace(fn, m_fn)
                # print(file_name)
                new_json_path = new_dir_path / file_name
                is_create = is_resave_json(f_json, new_dir_path, file_name)

                # if is_create:
                #     """기존 폴더 삭제"""
                #     print("삭제")
                #     shutil.rmtree(dir_path)


                is_file = True
                break

def is_resave_json(data, path, fn):
    is_create = False
    if not path.exists():
        path.mkdir(exist_ok=True, parents=True)
        json_path = path / fn
        with open(str(json_path), 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(str(json_path))
        is_create = True

    return is_create

