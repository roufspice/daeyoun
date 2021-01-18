"""외장하드 고객업로드 중복 파일 옮기기 20210115"""

def get_video_file_list():

    dataset = tablib.Dataset(headers=['file_video_name'])
    sub_directories = get_directories()
    video_list = []
    if sub_directories:
        for i, sub_directory in enumerate(sub_directories, start=1):
            print(f'{i}/{len(sub_directories)}')
            if 20201215<=int(Path(sub_directory).stem)<=20210108:
                video_path = [file for file in os.listdir(sub_directory) if file.endswith('.mp4' or '.MP4')]
                video_list.extend(video_path)


    for video_name in video_list:
        dataset.append([
            video_name
        ])


    directory = os.path.join(settings.EXPORT_ROOT, 'datamaker')
    file_name = 'metrix_pet_고객업로드_영상파일_중복리스트.xlsx'
    with open(os.path.join(directory, file_name), 'wb') as f:
        f.write(dataset.export('xlsx'))



def get_directories():
    # 고객업로드에서 20201215~20210108
    root_path = os.path.join(settings.PROJECT_ROOT, 'metrix_pet/고객업로드/')
    root_path = Path(root_path)

    if Path.exists(root_path):
        sub_directories = [f.path for f in os.scandir(root_path) if f.is_dir()]

        return sub_directories

    else:
        return None


def check_overlapped_videos():

    # excel_root_path
    excel_root_path = os.path.join(settings.EXPORT_ROOT, 'datamaker/metrix_pet_고객업로드_영상파일_중복리스트.xlsx')
    meta_data = open(excel_root_path, 'rb')
    meta_data = tablib.Dataset().load(meta_data.read(), format='xlsx')
    file_video_list = meta_data["file_video_name"]
    # dog-tailing-056631
    file_video_list = [file_name.replace(".mp4", "") for file_name in file_video_list]




    hdd_root_path = '/mnt/metrix_hdd/animals/'
    hdd_root_path = Path(hdd_root_path)

    # destination_path
    destination_path = '/mnt/metrix_hdd/animals/라벨링/'

    start = time.time()
    if hdd_root_path.exists():
        # 라벨링X 디렉토리 제외
        original_sub_directories_path = [f.path for f in os.scandir(hdd_root_path) if f.is_dir() and not f.path.endswith('라벨링X')]
        for original_path_1 in list(original_sub_directories_path):
            original_sub_directories_path = [f.path for f in os.scandir(original_path_1) if f.is_dir() and not f.path.endswith('라벨링X')]
            for original_path_2 in list(original_sub_directories_path):

                for file in os.listdir(original_path_2):
                    file_name = file.split(".")[0]

                    # 중복되는 파일 찾기
                    if file_name in file_video_list:
                        # 파일복사
                        print(os.path.join(original_path_2, file), os.path.join(destination_path, file))
                        shutil.move(os.path.join(original_path_2, file),
                                        os.path.join(destination_path, file))


                # 해당 파일 찾기



    print(time.time() - start)