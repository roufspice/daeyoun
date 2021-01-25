def metrix_pet_export_json_image_set():
    """json+이미지셋
    11/30 이후, 9명 사용자"""
    date = datetime.date(2020, 11, 30)
    user_tasks = UserTask.objects.filter(
        task__project__in=[324, 320],
        user__in = [7863, 6383, 8036, 7818, 10600, 9696, 9191, 9172, 2116],
        #12월 이후 작업물
        last_labeled__gte= date
    )
    count_total = user_tasks.count()

    # json익스포트
    paths_video = user_tasks.values_list('task__raw_data__data__file_video', flat=True)
    paths_video = list(set(list(paths_video)))
    count_total = len(paths_video)

    for i, path_video in enumerate(paths_video, start=1):
        print(f'{i}/{count_total}')

        path_video_relative = path_video.replace('/mnt/projects/metrix_pet/고객업로드/', '')
        annotations = []
        metadata = None

        user_tasks_video = user_tasks.filter(
            task__raw_data__data__file_video=path_video,
        ).order_by(
            'task__raw_data__data__frame'
        ).distinct('task__raw_data__data__frame')

        for user_task in user_tasks_video:

            labels = user_task.data or []
            raw_data = user_task.task.raw_data

            frame_data = raw_data.data
            image_path = raw_data.file.path

            image_width, image_height = get_image_size(image_path)

            keypoints= {}
            bounding_box = None

            for code in range(1, 16):
                keypoints[str(code)] = None

            for label in labels:
                try:
                    if label['label']['category'] == 'point':
                        keypoint = {
                            'x': label['label']['data']['x'],
                            'y': label['label']['data']['y']
                        }

                        if is_point_within(image_width, image_height, keypoint):
                            keypoints[label['classification']['code']] = keypoint

                    elif label['label']['category'] == 'rect':
                        bounding_box = label['label']['data']

                except KeyError:
                    pass

            annotation = {
                'frame_number': frame_data.get('frame'),
                'frame_url': f'https://dashboard.datamaker.io{raw_data.file.url}',
                'timestamp': frame_data.get('timestamp'),
                'keypoints': keypoints,
                'bounding_box': bounding_box
            }

            set_bounding_box_within_boundary(annotation, image_width, image_height)

            set_keypoints_within_bounding_box(annotation)

            annotations.append(annotation)
            #TODO frame 저장
            save_get_frame(user_task, path_video_relative)

        path_json = os.path.join(path_video.replace('.mp4', '.json'))

        try:
            with open(path_json) as file_json:
                metadata = json.load(file_json)
        except IOError:
            pass

        dataset = {
            'file_video': path_video_relative,
            'metadata': metadata,
            'annotations': annotations
        }

        file_name_json = path_video_relative.replace('/', '_')
        save_json(dataset, f'{file_name_json}.json', file_name_json)


def save_json(data, path, file_name):
    dir_name = Path(file_name).stem
    dir_name = dir_name.split("_")[-1]
    export_root_path = os.path.join(settings.EXPORT_ROOT, f'metrix_pet/NIA_SAMPLE/{dir_name}')
    export_root_path = Path(export_root_path)
    export_root_path.mkdir(parents=True, exist_ok=True)

    export_json_path = export_root_path / path
    with open(str(export_json_path), 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def save_get_frame(user_task, path_video_relative):

    file_name = path_video_relative.replace('/', '_')
    dir_name = Path(file_name).stem
    dir_name = dir_name.split("_")[-1]
    img_write_path = os.path.join(settings.EXPORT_ROOT, f'metrix_pet/NIA_SAMPLE/{dir_name}/{file_name}')
    img_write_path = Path(img_write_path)
    img_write_path.mkdir(parents=True, exist_ok=True)

    file_path = user_task.task.raw_data.file.path
    frame = user_task.task.raw_data.data['frame']
    timestamp = user_task.task.raw_data.data['timestamp']
    img = cv2.imread(file_path, cv2.IMREAD_COLOR)

    img_name = f'frame_{frame}_timestamp_{timestamp}.jpg'
    cv2.imwrite(os.path.join(img_write_path, img_name), img)
