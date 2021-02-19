# 50프로 이름바꾸기
def rename_dir_frames_in_100_percent_dir(animal):
    meta_data_path = os.path.join(os.getcwd(), '동작변경내역_데이터메이커_메트릭스작성.xlsx')
    f = open(meta_data_path, 'rb')
    dataset = tablib.import_set(f.read(), format='xlsx')
    original_frame_folder_name = dataset['original frame folder name']
    modified_frame_folder_name = dataset['modified frame folder name']
    json_origin_fn = dataset['original file name']
    json_md_fn = dataset['modified file name']

    root_path = f'/mnt/exports_old/metrix_pet/_100_percent_Upload/{animal}'
    dir_list = os.listdir(root_path)
    is_temp = False
    for dir in dir_list:
        # if is_temp:
        #     break

        dir_path = f'{root_path}/{dir}'
        file_list = os.listdir(dir_path)

        is_frame_changed = False

        for file_name in file_list:
            if file_name.startswith("_frames_fps_5_start_-1.00_end_-1.00_"):
                # print(file)
                if file_name in original_frame_folder_name:
                    frame_origin_path = f'{dir_path}/{file_name}'
                    new_file_name = modified_frame_folder_name[original_frame_folder_name.index(file_name)]
                    frame_renew_path = f'{dir_path}/{new_file_name}'
                    # print(frame_origin_path)
                    # print(frame_renew_path)

                    try:
                        os.rename(frame_origin_path, frame_renew_path)
                        print(f"frame rename: {frame_renew_path}")
                        is_frame_changed = True
                        # is_temp = True

                    except Exception as e:
                        print(str(e))

        if is_frame_changed:
            if dir in json_origin_fn:
                dir_origin_path = f'{root_path}/{dir}'
                renew_dir = json_md_fn[json_origin_fn.index(dir)]
                dir_new_path = f'{root_path}/{renew_dir}'
                # print(dir_origin_path)
                # print(dir_new_path)

                try:
                    os.rename(dir_origin_path, dir_new_path)
                    print(f"dir rename: {dir_new_path}")

                except Exception as e:
                    print(str(e))

# 다시프레임가져오기
def auto_labeling_frame_recopy():
    date_list = ['20210106', '20210107', '20210108', '20210109']

    for i, date in enumerate(date_list, start=0):

        video_root_path = f'/mnt/projects/metrix_pet/고객업로드/{date}'
        frame_dir_list = list(glob.glob(f'{video_root_path}/*_frames_fps_5_start_-1.00_end_-1.00_*', recursive=True))

        excel_path = os.path.join(os.getcwd(), '오토라벨링_갯수비교_리스트.xlsx')
        file = open(excel_path, 'rb')
        databook = tablib.import_book(file.read(), format='xlsx')
        sheets = databook.sheets()
        # 20210106_프레임
        dataset = sheets[7+i]
        none_frame_list = [re.search(r'\d{6}', data[1]).group() for data in dataset if data[2] == False]
        print(len(none_frame_list))
        copy_dir_path = f'/mnt/exports_old/metrix_pet/autolabeling/{date}'
        for frame_dir in frame_dir_list:

            frame_dir_n = Path(frame_dir).name
            frame_n = frame_dir_n.replace("_frames_fps_5_start_-1.00_end_-1.00_", "")
            frame_unique_number = re.search(r'\d{6}',frame_dir_n).group()
            if str(frame_unique_number) in none_frame_list:
                copy_dir_path_n = f'{copy_dir_path}/{frame_dir_n}'

                try:
                    shutil.copytree(str(frame_dir), str(copy_dir_path_n), copy_function= shutil.copy)
                    print(f'{date}: {copy_dir_path_n}')
                    print(os.path.exists(f'{copy_dir_path_n}'))

                except Exception as e:
                    print(str(e))
                    pass

# json이름변경_50%_파일복사함수
def rebuild_json_in_100_percent_dir(animal):
    """50% 디렉토리에 옯기기"""
    meta_data_path = os.path.join(os.getcwd(), '동작변경내역_데이터메이커_메트릭스작성.xlsx')
    f = open(meta_data_path, 'rb')
    dataset = tablib.import_set(f.read(), format='xlsx')
    json_origin_fn = dataset['original file name']
    json_md_fn = dataset['modified file name']
    json_md_action = dataset['metadata_action']

    dataset = {}
    root_path = f'/mnt/exports_old/metrix_pet/_100_percent_Upload/{animal}'
    root_path = Path(root_path)
    dir_list = os.listdir(root_path)
    #TODO json파일 하나만 있는 디렉토리 찾기
    for dir in dir_list:
        dir_path = f'{root_path}/{dir}'

        file_list = os.listdir(dir_path)
        if len(file_list) == 1 and file_list[0].endswith('.json'):
            #TODO 고유번호_추출
            unique_number = re.search(r'-\d{6}', file_list[0])
            unique_number = unique_number.group().replace("-", "")
            origin_path = f'{dir_path}/{file_list[0]}'
            # print(unique_number)
            # print(f'{dir_path}/{file_list[0]}')

            dataset[unique_number] = origin_path

    print("데이터셋 구축완료")
    # is_temp =False
    for dir in dir_list:
        # if is_temp:
        #     break
        dir_path = f'{root_path}/{dir}'
        file_list = os.listdir(dir_path)
        if len(file_list) == 1 and file_list[0].startswith("_frames_fps_5_start_-1.00_end_-1.00_"):
            # print(file_list[0])
            unique_num = re.search(r'-\d{6}', file_list[0])
            unique_num = unique_num.group().replace("-", "")
            move_path = f'{dir_path}'

            for k, v in dataset.items():
                if str(unique_num) == str(k):
                    origin_json_path = str(v)


                    try:
                        shutil.move(origin_json_path, move_path)
                        print(f'{origin_json_path}=>{move_path}')
                        # is_temp = True
                        break

                    except Exception as e:
                        print(str(e))

#100_%_파일복사 함수_이동
def copy_auto_labeled_frames_to_100_percent_dir():

    export_excel = tablib.Dataset(headers=['path'])

    meta_excel_path = os.path.join(os.getcwd(), '동작변경내역_데이터메이커_메트릭스작성.xlsx')
    f = open(meta_excel_path, 'rb')
    meta_dataset = tablib.import_set(f.read(), format='xlsx')
    original_frames = meta_dataset['original frame folder name']
    modified_frames = meta_dataset['modified frame folder name']
    original_files = meta_dataset['original file name']
    modified_files = meta_dataset['modified file name']

    root_path = '/mnt/exports_old/metrix_pet/autolabeling'
    # root_path_dirs = ['20201215', '20201216', '20201217', '20201218', '20201219', '20201220', '20201221', '20210105']
    # root_path_dirs = ['20210106', '20210107', '20210108', '20210109']
    root_path_dirs = ['20210108', '20210109']
    copy_root_path = '/mnt/exports_old/metrix_pet/_100_percent_Upload'

    for i, date_dir in enumerate(root_path_dirs, start=1):

        date_dir = f'{root_path}/{date_dir}'
        print(date_dir)
        # print(os.path.exists(date_dir))
        files_list = os.listdir(date_dir)
        total_count = len(files_list)
        print(total_count)
        is_temp = False
        for i, file in enumerate(files_list, start=1):
            # if is_temp:
            #     break

            print(f'{i}/{total_count}')
            copy_path = None
            file = str(file)
            # print(file)
            if file.endswith(".json"):
                # jsons
                json_name = str(file).replace(".json", ".mp4")
                dir_name = json_name
                animal_name = json_name.split("-")[0].upper()
                original_path = f'{date_dir}/{file}'
                copy_path = f'{copy_root_path}/{animal_name}/{dir_name}'

                # TODO 중복검사

                try:
                    valid_files = os.listdir(copy_path)

                    if os.path.exists(copy_path) and len(valid_files) == 2:
                        print(f"The file already exists in export path! {copy_path}")
                        continue

                except Exception as e:
                    print(str(e))
                    pass

                original_path_file = original_path
                copy_path_file = f'{copy_path}/{file}'

                try:
                    if not os.path.exists(copy_path):
                        copy_path = Path(copy_path)
                        copy_path.mkdir(parents=True, exist_ok=True)

                        # shutil.copyfile(original_path_file, copy_path_file)
                        shutil.move(original_path_file, copy_path_file)
                        print(f"folder_and_json_create : {original_path_file} => {copy_path_file}")
                        is_temp = True

                    else:
                        # shutil.copyfile(original_path_file, copy_path_file)
                        shutil.move(original_path_file, copy_path_file)
                        print(f"folder exists and_json_create : {original_path_file} => {copy_path_file}")
                        is_temp = True


                except Exception as e:
                    print(str(e))

            elif file.startswith("_frames_fps_5_start_-1.00_end_-1.00_"):
                # frames
                frame_name = str(file).replace("_frames_fps_5_start_-1.00_end_-1.00_", "").replace("_mp4", ".mp4")
                dir_name = frame_name
                animal_name = frame_name.split("-")[0].upper()

                original_path = f'{date_dir}/{file}'
                copy_path = f'{copy_root_path}/{animal_name}/{dir_name}'

                #TODO 중복검사
                try:
                    valid_files = os.listdir(copy_path)
                    if os.path.exists(copy_path) and len(valid_files) == 2:
                        print(f"The file already exists in export path! {copy_path}")
                        continue

                except Exception as e:
                    pass

                try:
                    if not os.path.exists(copy_path):
                        copy_path = Path(copy_path)
                        copy_path.mkdir(parents=True, exist_ok=True)
                        # print("폴더생성")
                        # shutil.copytree(original_path, f'{copy_path}/{file}', copy_function=shutil.copy)
                        shutil.move(original_path, f'{copy_path}/{file}')
                        print(f"folder_and_frames_create :{original_path} => {copy_path}/{file}")

                        is_temp = True

                    else:
                        shutil.move(original_path, f'{copy_path}/{file}')
                        # shutil.copytree(original_path, f'{copy_path}/{file}', copy_function=shutil.copy)
                        print(f"folder_exists_and_frames_create : {original_path} => {copy_path}/{file}")

                        is_temp = True

                except Exception as e:
                    print(str(e))

            # if copy_path:
            #     print(f'{copy_path}:copied_completed')
            #     export_excel.append([str(copy_path)])

            with open(os.path.join(os.getcwd(), 'qh_오토라벨링복사_리스트_.xlsx'), 'wb') as f:
                f.write(export_excel.export('xlsx'))

#매뉴얼태깅_프레임복사확인 함수
def validate_manual_tagging():
    databook = tablib.Databook()

    root_path = '/mnt/exports_old/metrix_pet/공유_Data_Export'
    dir_date_list = os.listdir(root_path)
    dir_date_list = sorted(dir_date_list, reverse=False)

    for i, dir_path in enumerate(dir_date_list, start=1):
        print(dir_path)
        dataset = tablib.Dataset(headers=['frame', 'json', 'valid', 'name_valid'], title=dir_path)
        dir_root_path = f'{root_path}/{dir_path}'
        dirs_path = os.listdir(dir_root_path)
        for dir in dirs_path:
            files = f'{dir_root_path}/{dir}'
            files_list = os.listdir(files)
            json = None
            frame = None
            valid = False
            name_valid = False

            json_n = ''
            frame_n = ''

            for i in files_list:
                if str(i).endswith('.json'):
                    json = i
                    json_n = str(i).split("_")[-1].replace(".mp4.json", "")

                elif str(i).startswith('_frames_fps_5_start_-1.00_end_-1.00_'):
                    frame = i
                    frame_n = str(i).replace("_frames_fps_5_start_-1.00_end_-1.00_", "").replace("_mp4", "")

            if (json != None and frame != None):
                valid = True

            elif (json == None and frame == None):
                frame = files
                json = files

            if json_n == frame_n:
                name_valid = True

            dataset.append([
                frame,
                json,
                valid,
                name_valid,

            ])

        print(dataset)

        databook.add_sheet(dataset)

    export_directory = os.path.join(os.getcwd())
    with open(os.path.join(export_directory, f'메뉴얼태깅_갯수비교_리스트.xlsx'), 'wb') as f:
        f.write(databook.export(format='xlsx'))
    print("완료")

#autolabeling_프레임복사확인 함수
def validate_auto_labeling():
    dir_dates_list = ['20201215', '20201216', '20201217', '20201218', '20201219', '20201221', '20210105',
                      '20210106', '20210107', '20210108', '20210109', '20210110']
    databook = tablib.Databook()
    for dir_path in dir_dates_list:
        root_path = '/mnt/exports_old/metrix_pet/autolabeling'

        dir_root_path = f'{root_path}/{dir_path}'
        print(dir_root_path)

        jsons_list = []
        frames_list = []
    #
        dataset = tablib.Dataset(headers=['frames', 'json', 'valid'], title=dir_path)
    #
        file_list = os.listdir(dir_root_path)
        for file in file_list:
            if file.startswith("_frames_fps_5_start_-1.00_end_-1.00_"):
                frames_list.append(file)
            else:
                jsons_list.append(file)
    #
        # print(jsons_list)
        jsons_list = sorted(jsons_list, reverse=False)
    #
        # print(frames_list)
        frames_list = sorted(frames_list, reverse=False)
    #
        print(len(jsons_list))
        print(len(frames_list))
        count = 0
        for json in jsons_list:
            is_frame = False
            fn = str(json).split("-")[-1].replace(".json", "_mp4")
    #
            for frame in frames_list:
                if fn in frame:
                    is_frame = True
                    # print(frame)
                    count += 1
    #
                    dataset.append([
                        frames_list.pop(frames_list.index(frame)),
                        json,
                        True
                    ])
    #
            if not is_frame:
                dataset.append([
                    None,
                    json,
                    False
                ])

        for frame in frames_list:
            dataset.append([
                frame,
                None,
                False
            ])

        databook.add_sheet(dataset)

    directory = os.path.join(os.getcwd())
    with open(os.path.join(directory, f'오토라벨링_갯수비교_리스트.xlsx'), 'wb') as f:
        f.write(databook.export(format='xlsx'))
    print("완료")

# 50_%_디렉토리 카운트
def count_amount_50_percent_dir():
    animal_list = ['CAT', 'DOG']
    databook = tablib.Databook()
    for animal in animal_list:
        print(f"{animal}...ongoing...")
        root_path = f'/mnt/exports_old/metrix_pet/_50_percent_Upload/{animal}'
        dataset = tablib.Dataset(title=animal, headers=[f'{animal}_json_count', f'{animal}_json_size', f'{animal}_frame_count', f'{animal}_frame_size'])

        dir_list = os.listdir(root_path)

        total_json_count = 0
        total_frame_count = 0
        total_json_size = 0
        total_frame_size = 0
        for dir in dir_list:
            file_list = os.listdir(f'{root_path}/{dir}')
            # file_size = os.path.getsize(f'{root_path}/{dir}')
            print(f'{root_path}/{dir}')

            if len(file_list) == 2:
                for file in file_list:
                    if str(file).endswith(".json"):

                        json_size = os.path.getsize(f'{root_path}/{dir}/{file}')
                        # print(f'json_size: {json_size}')
                        total_json_size += json_size
                        total_json_count += 1

                    elif str(file).startswith("_frames_fps_5_start_-1.00_end_-1.00"):
                        # frame_size = os.path.getsize(f'{root_path}/{dir}/{file}')
                        # print(f'frame_size: {frame_size}')
                        # total_frame_size += frame_size
                        frames_list = list(glob.glob(f'{root_path}/{dir}/{file}/*.jpg', recursive=True))
                        frames_count = len(frames_list)
                        total_frame_count += frames_count

                        tot_frame_size = 0
                        for frame in frames_list:
                            frame_size = os.path.getsize(frame)
                            tot_frame_size += frame_size

                        total_frame_size += tot_frame_size



        dataset.append([
            total_json_count,
            total_json_size,
            total_frame_count,
            total_frame_size,
        ])

        databook.add_sheet(dataset)


    export_directory = os.path.join(os.getcwd())
    with open(os.path.join(export_directory, f"50_업로드_통계.xlsx"), 'wb') as f:
        f.write(databook.export(format='xlsx'))

    print("download_completed")


def count_amount_without_50_percent_dir():
    root_path = '/mnt/exports_old/metrix_pet/autolabeling'
    date_list = ['20210106', '20210107', '20210108', '20210109', '20210110']

    total_CAT_json_count = 0
    total_CAT_json_size = 0
    total_CAT_frame_count = 0
    total_CAT_frame_size = 0

    total_DOG_json_count = 0
    total_DOG_json_size = 0
    total_DOG_frame_count = 0
    total_DOG_frame_size = 0

    headers = ['cat_json_count', 'cat_json_size', 'cat_frame_count', 'cat_frame_size', 'dog_json_count', 'dog_json_size', 'dog_frame_count', 'dof_frame_size']
    dataset = tablib.Dataset(headers=headers)
    for date in date_list:
        print(f'{date}..ongoing..')

        root_date_path = f'{root_path}/{date}'
        print(root_date_path)

        # CAT_json_갯수
        CAT_jsons_list = list(glob.glob(f'{root_date_path}/*cat*.json', recursive=True))
        CAT_jsons_count = len(CAT_jsons_list)

    #     #CAT_frame_갯수 및 크기
        CAT_frames_dir_list = glob.glob(f'{root_date_path}/*_frames_fps_5_start_-1.00_end_-1.00*cat*', recursive=True)
        CAT_frames_dir_list = list(CAT_frames_dir_list)
        #CAT_frames
        for cat_frames_dir in CAT_frames_dir_list:
            print(cat_frames_dir)
            frames_list = list(glob.glob(f'{cat_frames_dir}/*.jpg'))
            frames_count = len(frames_list)
            tot_frames_size = 0
            for frame in frames_list:
                frame_size = os.path.getsize(frame)
                tot_frames_size += frame_size

            # print(frames_count)
            total_CAT_frame_count += frames_count
            # print(tot_frames_size)
            total_CAT_frame_size += tot_frames_size

        #CAT_json 크기
        for cat_json in CAT_jsons_list:
            print(cat_json)
            json_size = os.path.getsize(cat_json)
            # print(json_size)
            total_CAT_json_size += json_size


        #DOG_json_갯수
        DOG_jsons_list = list(glob.glob(f'{root_date_path}/*dog*.json', recursive=True))
        DOG_jsons_count = len(DOG_jsons_list)

        #DOG_frame_갯수 및 크기
        DOG_frames_dir_list = glob.glob(f'{root_date_path}/*_frames_fps_5_start_-1.00_end_-1.00*dog*', recursive=True)
        DOG_frames_dir_list = list(DOG_frames_dir_list)

        #DOG_frames
        for dog_frames_dir in DOG_frames_dir_list:
            print(dog_frames_dir)
            frames_list = list(glob.glob(f'{dog_frames_dir}/*.jpg'))
            frames_count = len(frames_list)
            tot_frames_size = 0

            for frame in frames_list:
                frame_size = os.path.getsize(frame)
                tot_frames_size += frame_size

            # print(frames_count)
            total_DOG_frame_count += frames_count
            # print(tot_frames_size)
            total_DOG_frame_size += tot_frames_size


        #DOG_json_크기
        for dog_json in DOG_jsons_list:
            print(dog_json)
            json_size = os.path.getsize(dog_json)
            # print(json_size)
            total_DOG_json_size += json_size


        total_CAT_json_count += CAT_jsons_count
        total_DOG_json_count += DOG_jsons_count


    dataset.append([
        total_CAT_json_count,
        total_CAT_json_size,
        total_CAT_frame_count,
        total_CAT_frame_size,
        total_DOG_json_count,
        total_DOG_json_size,
        total_DOG_frame_count,
        total_DOG_frame_size,
    ])

    export_path = os.path.join(os.getcwd(), '10106_이후_업로드_통계.xlsx')
    with open(export_path, 'wb') as f:
        f.write(dataset.export(format='xlsx'))


def del_empty_100_percent_dir(animal):
    root_path = '/mnt/exports_old/metrix_pet/_100_percent_Upload/'
    root_path = f'/mnt/exports_old/metrix_pet/_100_percent_Upload/{animal}'
    root_path = Path(root_path)
    dir_list = os.listdir(root_path)

    for dir in dir_list:
        dir_path = f'{root_path}/{dir}'

        file_list = os.listdir(dir_path)
        if len(file_list) == 0:

            os.rmdir(dir_path)
            print(dir_path)


#auto_프레임복사 함수
def move_frame_autolabel():
    """0106~0110 프레임 복사"""
    # date_dir = ['20210106', '20210107', '20210108', '20210109', '20210110']
    date_dir = ['20210108', '20210109', '20210110']
    # json_root_path = f'/mnt/exports/metrix_pet/autolabeling/'
    json_root_path = f'/mnt/exports_old/metrix_pet/autolabeling'
    dataset = tablib.Dataset(headers=['original_frame', 'copied_frame', 'is_success', 'error_message'])

    for date in date_dir:
        # frame_meta_root_path = f'/mnt/projects/metrix_pet/고객업로드/{date}'
        frame_meta_root_path = os.path.join(settings.PROJECT_ROOT, f'metrix_pet/고객업로드/{date}')

        json_export_path = f'{json_root_path}/{date}'
        # frame_meta_root_path = Path(frame_meta_root_path)
        # json_export_path = Path(json_export_path)
        if os.path.exists(frame_meta_root_path) and os.path.exists(json_export_path):
            #         #20210106
            print(json_export_path)

            frame_list = os.listdir(frame_meta_root_path)
            frame_list = [dir for dir in frame_list if str(dir).startswith("_frames_fps_5_start_-1.00_end_-1.00_")]

            total_count = len(frame_list)

            json_list = Path(json_export_path).rglob("*.json")
            count = 0
            for json in json_list:
                print(f'{date}: {count}/{total_count}')
                json_fn = json.name
                new_fn = json.name.replace(".json", "_mp4")
                new_fn = f'_frames_fps_5_start_-1.00_end_-1.00_{new_fn}'
                if new_fn in frame_list:
                #print(new_fn)
                # 경로를 가져와서 그대로 복사
                    origin_path = f'{frame_meta_root_path}/{new_fn}'
                    copy_path = f'{json_export_path}'

                    try:
                        if os.path.exists(f'{copy_path}/{new_fn}'):
                            print(f'file_existed: {copy_path}/{new_fn}')
                            pass
                        else:
                            # print(f"{json_count}/{total_count}")
                            print(f"moving...")
                            shutil.move(origin_path, copy_path)
                            print(f'moved completed: {origin_path} => {copy_path}')
                            dataset.append([
                                origin_path,
                                copy_path,
                                "True",
                                "None"

                            ])

                        count += 1
                    #
                    except Exception as e:
                        print(str(e))
                        print(f'!!!Fail!!!: {origin_path} => {copy_path}')
                        dataset.append([
                            origin_path,
                            copy_path,
                            "False",
                            str(e)
                        ])

                        count += 1

    # with open(os.path.join(os.getcwd(), 'auto_labeling_프레임복사리스트_0106_0110.xlsx'), 'wb') as f:
    #     f.write(dataset.export('xlsx'))


def manual_copy_frames_movement_tjsquf():
    """projects/축종_행동유형_선별영상_프레임 옮기기
        /projects/metrix_pet/축종_행동유형_선별영상/20210112_선별/
        """
    headers = ['original_frame', 'copied_frame', 'is_success', 'error_message']
    log_dataset = tablib.Dataset(headers=headers)

    meta_data_path = os.path.join(os.getcwd(), '동작변경내역_데이터메이커_메트릭스작성.xlsx')
    f = open(meta_data_path, 'rb')
    dataset = tablib.import_set(f.read(), format='xlsx')
    meta_origin_fn = dataset['original frame folder name']
    meta_md_fn = dataset['modified frame folder name']

    frames_root_path = '/mnt/projects/metrix_pet/축종_행동유형_선별영상/20210112_선별'
    frames_export_path = '/mnt/exports/metrix_pet/공유_Data_Export/20210112'

    dir_list = os.listdir(frames_root_path)
    for dir in dir_list:
        if dir.startswith("_frames_fps_5_start_-1.00_end_-1.00_"):

            export_dir_name = dir.replace("_frames_fps_5_start_-1.00_end_-1.00_", "").replace("_mp4", ".mp4")
            origin_dir_path = f'{frames_root_path}/{dir}'

            copy_dir_path = f'{frames_export_path}/{export_dir_name}/{dir}'

            try:
                shutil.copytree(origin_dir_path, copy_dir_path, copy_function=shutil.copy)
                print(f"프레임복사완료: {copy_dir_path}")
                log_dataset.append([
                    origin_dir_path,
                    copy_dir_path,
                    "True",
                    None
                ])

            except Exception as e:
                log_dataset.append([
                    origin_dir_path,
                    copy_dir_path,
                    "False",
                    str(e)

                ])

    with open(os.path.join(os.getcwd(), '매뉴얼태깅_축종_프레임복사리스트_20210112_선별_.xlsx'), 'wb') as f:
        f.write(log_dataset.export('xlsx'))


def auto_rename_json_100_percent_dir(animal):
    """auto_labeling / json 파일들 이름 바꾸기"""

    meta_data_path = os.path.join(os.getcwd(), '동작변경내역_데이터메이커_메트릭스작성.xlsx')
    f = open(meta_data_path, 'rb')
    dataset = tablib.import_set(f.read(), format='xlsx')
    json_origin_fn = dataset['original file name']
    json_md_fn = dataset['modified file name']
    json_md_action = dataset['metadata_action']

    root_path = f'/mnt/exports_old/metrix_pet/_100_percent_Upload/{animal}'
    dir_list = sorted(os.listdir(root_path))

    is_changed_temp = False

    for dir in dir_list:
        # if is_changed_temp:
        #     break

        is_changed = False
        dir_path = f'{root_path}/{dir}'
        # json, frames,
        file_list = os.listdir(dir_path)

        for file in file_list:
            # json_변경하기
            if str(file).endswith('.json'):
                if str(file).startswith("2020"):
                    fn = str(file).split("_")[-1].replace(".json", "")

                else:
                    fn = str(file).replace(".json", ".mp4")

                # print(fn)
                if str(fn) in json_origin_fn:
                    print(f'{dir_path}/{file}')
                    # print(file)
                    json_path = f'{dir_path}/{file}'
                    new_fn = json_md_fn[json_origin_fn.index(fn)]
                    new_action = json_md_action[json_origin_fn.index(fn)]

                    new_file = str(file).replace(str(fn), str(new_fn))
                    new_json_path = f'{dir_path}/{new_file}'
                    # print(f'new_json_path: {new_json_path}')
                    #
                    # print(str(json_path))
                    with open(str(json_path), 'r', encoding='UTF8') as file_json:
                        json_f = json.load(file_json)
                    # print(json_f['file_video'])
                    #
                    json_new = modified_json(json_f, new_fn, new_action)
                    #
                    is_json_created = save_json(new_json_path, json_new)

                    if is_json_created:
                        print(f'new_json_created: {new_json_path}')
                        # 기존 json 삭제
                        os.remove(str(json_path))
                        print(f'json_deleted: {json_path}')

                    # is_changed = True
                    is_changed_temp = True

        print("json_name_completed")
        for file in file_list:
            # json_변경하기
            if str(file).endswith('.json'):
                if str(file).startswith("2020"):
                    fn = str(file).split("_")[-1].replace(".json", "")

                else:
                    fn = str(file).replace(".json", ".mp4")

                # print(fn)
                if str(fn) in json_md_fn:
                    print(f'{dir_path}/{file}')
                    # print(file)
                    json_path = f'{dir_path}/{file}'
                    new_fn = fn
                    new_action = json_md_action[json_md_fn.index(fn)]

                    new_file = str(file).replace(str(fn), str(new_fn))
                    new_json_path = f'{dir_path}/{new_file}'
                    # print(f'new_json_path: {new_json_path}')

                    # print(str(json_path))
                    with open(str(json_path), 'r', encoding='UTF8') as file_json:
                        json_f = json.load(file_json)
                    # print(json_f['file_video'])
                    #
                    json_new = modified_json(json_f, new_fn, new_action)
                    #
                    is_json_created = save_json(new_json_path, json_new)

                    if is_json_created:
                        is_changed_temp =True
                        pass


        # if is_changed:
        #     new_dir = json_md_fn[json_origin_fn.index(str(dir).split("/")[-1])]
        #     origin_dir_path = dir_path
        #     new_dir_path = f'{root_path}/{new_dir}'
        #
        #     try:
        #         if os.path.exists(new_dir_path):
        #             print(f'dir_existed:{new_dir_path}')
        #             shutil.rmtree(new_dir_path)
        #             print(f'dir_deleted!')
        #
        #             # dir 이름 변경
        #             shutil.move(origin_dir_path, new_dir_path)
        #             print(f'dir_rename_completed: {new_dir_path}')
        #             is_changed_temp = True
        #
        #         else:
        #             # dir 이름 변경
        #             shutil.move(origin_dir_path, new_dir_path)
        #             print(f'dir_rename_completed: {new_dir_path}')
        #             is_changed_temp = True
        #
        #
        #     except Exception as e:
        #         print(str(e))


def load_json(input_path):
    with open(str(input_path), encoding='UTF8') as f:
        return json.load(f)


def modified_json(json, new_fn, new_action):
    json['file_video'] = str(new_fn)
    json['metadata']['action'] = str(new_action)

    return json


def save_json(new_path, data):
    is_created = False
    with open(str(new_path), 'w', encoding='UTF-8') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)
        is_created = True

    return is_created


def manual_copy_frames():
    """매뉴얼 태깅 frames 고객업로드 복사하기 """
    headers = ['original_frame_fn', 'copied_frame_fn', 'is_success', 'error_message']
    log_dataset = tablib.Dataset(headers=headers)

    meta_data_path = os.path.join(os.getcwd(), '동작변경내역_데이터메이커_메트릭스작성.xlsx')

    f = open(meta_data_path, 'rb')
    dataset = tablib.import_set(f.read(), format='xlsx')
    meta_origin_fn = dataset['original frame folder name']
    meta_md_fn = dataset['modified frame folder name']

    frames_root_path = '/mnt/projects/metrix_pet/고객업로드'
    frames_export_path = '/mnt/exports/metrix_pet/공유_Data_Export'

    date_dir_list = os.listdir(frames_root_path)

    total_count = len(date_dir_list)

    for i, date_dir in enumerate(date_dir_list, start=1):
        print(f'dates: {date_dir}')

        dirs_path = os.path.join(frames_root_path, date_dir)
        dirs_path_list = os.listdir(dirs_path)

        for j, dir_path in enumerate(dirs_path_list, start=1):
            print(f'{date_dir}_mp4_count: {j}/{len(dirs_path_list)}')
            if dir_path.startswith("_frames_fps_5_start_-1.00_end_-1.00_"):
                # print(os.path.join(dirs_path, dir_path))

                origin_dir_path = os.path.join(dirs_path, dir_path)

                origin_frame_fn = dir_path
                if origin_frame_fn in meta_origin_fn:
                    origin_frame_fn = meta_md_fn[meta_origin_fn.index(origin_frame_fn)]

                fn_dir = origin_frame_fn.replace("_frames_fps_5_start_-1.00_end_-1.00_", "")
                fn_dir = fn_dir.replace("_", ".")
                copy_dir_path = f'{frames_export_path}/{date_dir}/{fn_dir}/{origin_frame_fn}'

                print(origin_frame_fn)

                try:
                    shutil.copytree(origin_dir_path, copy_dir_path, copy_function=shutil.copy)
                    print(f'success: {origin_dir_path} => {copy_dir_path}')
                    log_dataset.append([
                        origin_dir_path,
                        copy_dir_path,
                        "True",
                        None,
                    ])


                except FileExistsError as e_message:
                    print(f'failed: {origin_dir_path} => {copy_dir_path}')
                    log_dataset.append([
                        origin_dir_path,
                        copy_dir_path,
                        "False",
                        e_message,
                    ])
                    pass

            else:
                pass

    with open(os.path.join(os.getcwd(), '매뉴얼태깅_프레임복사리스트.xlsx'), 'wb') as f:
        f.write(log_dataset.export('xlsx'))


def rename_dir_name():
    """공유_DATA_폴더이름 변경"""
    root_path = '/mnt/exports/metrix_pet/공유_Data_Export/'
    date_dir_list = os.listdir(root_path)
    meta_data_path = os.path.join(os.getcwd(), '동작변경내역_데이터메이커_메트릭스작성.xlsx')

    success_count = 0
    fail_count = 0
    if os.path.exists(meta_data_path):
        f = open(meta_data_path, 'rb')
        dataset = tablib.import_set(f.read(), format='xlsx')

        origin_fn = dataset['original file name']
        new_fn = dataset['modified file name']

        for date_dir in date_dir_list:
            d_dir_path = os.path.join(root_path, date_dir)
            dir_path_list = os.listdir(d_dir_path)
            for dir_path in dir_path_list:
                if dir_path in origin_fn:
                    # print(dir_path)
                    new_path = new_fn[(origin_fn.index(dir_path))]
                    try:
                        origin_dir = os.path.join(d_dir_path, dir_path)
                        # print(origin_dir)
                        new_dir = os.path.join(d_dir_path, new_path)
                        # print(new_dir)
                        # (origin_dir, new_dir)
                        shutil.move(origin_dir, new_dir)
                        success_count += 1
                        print(f'success: {dir_path}, {new_path}')
                    except FileNotFoundError:
                        fail_count += 1
                        print(f'failed: {dir_path}, {new_path}')

    print(f'fail:{fail_count} / success:{success_count}')


def video_to_frame_temp(date):
    root_paths = os.path.join(settings.PROJECT_ROOT, 'metrix_pet/고객업로드/')
    root_paths = [os.path.join(settings.PROJECT_ROOT, f'metrix_pet/고객업로드/{dir}/') for dir in
                  os.listdir(Path(root_paths)) if dir >= date]
    print(root_paths)

    for i, root_path in enumerate(root_paths, start=1):
        print(f'{i}/{len(root_paths)}')

        path = Path(root_path).rglob('*.mp4')

        for video_path in path:
            print(video_path)
            preprocess(
                input_file_path=video_path,
                fps=5,
            )


def shared_data_metrix_pet_selection():
    """선별영상 re_export"""

    list_excel = os.path.join(os.getcwd(), '동작변경내역_데이터메이커_메트릭스작성.xlsx')
    f = open(list_excel, 'rb')
    meta_data = tablib.import_set(f, format='xlsx')
    original_frames = meta_data['original frame folder name']
    modified_frames = meta_data['modified frame folder name']

    meta_data_excel = os.path.join(os.getcwd(), '메뉴얼태깅_갯수비교_리스트.xlsx')
    f = open(meta_data_excel, 'rb')
    meta_databook = tablib.import_book(f, format='xlsx')
    sheets = meta_databook.sheets()

    meta_dataset = sheets[-1]
    meta_dataset_frames = [data[0] for data in meta_dataset if not data[2]]

    videos = []
    for frame in meta_dataset_frames:
        frame = str(frame)
        if frame in original_frames:
            videos.append(frame)

        # original_fn으로 처리
        elif frame in modified_frames:
            # print(f'mdfn: {frame}')
            frame = original_frames[modified_frames.index(frame)]
            # print(f'mdfn: {frame}')
            videos.append(frame)

        else:
            videos.append(frame)

    videos = [frame.replace("_frames_fps_5_start_-1.00_end_-1.00_", "").replace("_mp4", ".mp4") for frame in videos]

    user_tasks = UserTask.objects.filter(
        task__project__in=[320, 324, 358],
        status__in=['confirmed']
    )

    paths_video = user_tasks.values_list('task__raw_data__data__file_video', flat=True)
    paths_video = list(set(list(paths_video)))

    paths_video = [path_video for path_video in paths_video if str(path_video.split("/")[-1]) in videos]

    for path_video in paths_video:
        print(path_video)

    # count_total = len(paths_video)
    # for i, path_video in enumerate(paths_video, start=1):
    #     if i > 1:
    #         continue
    #     print(f'{i}/{count_total}')
    #
    #     annotations = []
    #     metadata = None
    #
    #     user_tasks_video = user_tasks.filter(
    #         task__raw_data__data__file_video=path_video,
    #     ).order_by(
    #         'task__raw_data__data__frame'
    #     ).distinct('task__raw_data__data__frame')
    # #
    #         for user_task in user_tasks_video:
    #             labels = user_task.data or []
    #             raw_data = user_task.task.raw_data
    #
    #             frame_data = raw_data.data
    #             image_path = raw_data.file.path
    #
    #             image_width, image_height = get_image_size(image_path)
    #
    #             keypoints = {}
    #             bounding_box = None
    #
    #             for code in range(1, 16):
    #                 keypoints[str(code)] = None
    #
    #             for label in labels:
    #                 try:
    #                     if label['label']['category'] == 'point':
    #                         keypoint = {
    #                             'x': label['label']['data']['x'],
    #                             'y': label['label']['data']['y']
    #                         }
    #
    #                         if is_point_within(image_width, image_height, keypoint):
    #                             keypoints[label['classification']['code']] = keypoint
    #
    #                     elif label['label']['category'] == 'rect':
    #                         bounding_box = label['label']['data']
    #
    #                 except KeyError:
    #                     pass
    #
    #             annotation = {
    #                 'frame_number': frame_data.get('frame'),
    #                 'frame_url': f'https://dashboard.datamaker.io{raw_data.file.url}',
    #                 'timestamp': frame_data.get('timestamp'),
    #                 'keypoints': keypoints,
    #                 'bounding_box': bounding_box
    #             }
    #
    #             set_bounding_box_within_boundary(annotation, image_width, image_height)
    #
    #             set_keypoints_within_bounding_box(annotation)
    #
    #             annotations.append(annotation)
    #
    #         path_json = os.path.join(path_video.replace('.mp4', '.json'))
    #
    #         try:
    #             with open(path_json) as file_json:
    #                 metadata = json.load(file_json)
    #         except IOError:
    #             pass
    #
    #         dataset = {
    #             'file_video': path_video_relative,
    #             'metadata': metadata,
    #             'annotations': annotations
    #         }
    #
    #         file_name_json = path_video_relative.replace('/', '_')
    #         # save_json_modified(dataset, f'{file_name_json}.json', path_video_dir_name, video_dir_name)
    #
    #
    #
    #     else:
    #         continue


def get_annotation(frame):
    stem = frame.stem
    timestamp = stem.split("_")[-1]
    frame_number = stem.split("_")[1]

    return frame_number, timestamp


def get_auto_bounding_box(frame_path):
    kwargs = {
        'function_path': 'metrix_auto_label.infer',
        'parameter': {
            'args': [],
            'kwargs': {
                'path': str(frame_path),
                'config': 'default_keypoint.yaml',

            }
        }
    }

    return remote_service(**kwargs)