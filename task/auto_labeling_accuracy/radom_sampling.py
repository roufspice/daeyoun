def random_sampling_():
    """random_sampling
    11/24 ~ 12/16 사이의 40,000개 데이터 추출"""

    count = 0
    users = [7863, 6383, 8036, 7818, 10600, 9696, 9191, 9172, 2116]
    before_ = datetime.datetime(2020, 11, 24, 0, 0, 0, tzinfo=datetime.timezone.utc)
    after_ = datetime.datetime(2020, 12, 16, 0, 0, 0, tzinfo=datetime.timezone.utc)

    user_tasks = UserTask.objects.filter(
        task__project__in=[324,320],
        status__in=['confirmed'],
        last_labeled__gte=before_,
        # last_labeled__lte=after_,


    ).exclude(
        user_id__in=users
    ).order_by('task__raw_data__checksum')
    databook = []
    paths_video = user_tasks.values_list('task__raw_data__data__file_video', flat=True)
    paths_video = list(set(list(paths_video)))

    count_total = len(paths_video)

    for i, path_video in enumerate(paths_video, start=1):
        if count == 40000:
            break
        annotations = []
        path_video_relative = path_video.replace('/mnt/projects/metrix_pet/고객업로드/', '')

        user_tasks_video = user_tasks.filter(
            task__raw_data__data__file_video=path_video,
        ).order_by('task__raw_data__data__frame').distinct('task__raw_data__data__frame')

        for user_task in user_tasks_video:

            if count == 40000:
                break
            raw_data = user_task.task.raw_data
            frame_url = raw_data.file.path


            annotation = {
                'id': user_task.id,
                'frame_url':str(frame_url),
                'frame_number':raw_data.data.get('frame'),
                'timestamp':raw_data.data.get('timestamp'),
            }

            annotations.append(annotation)
            count +=1
            print(count)


        dataset = {
            'video_path': path_video,
            'file_video': path_video_relative,
            'annotations': annotations
        }
        databook.append(dataset)
    print(databook)

    file_name_json = 'metrix_pet_annotation_random'
    dir_name = ''
    detail_dir = ''

    save_json_modified(databook, f'{file_name_json}.json', dir_name, detail_dir)
    print('save완료')



def save_json_modified(data, path, path_dir, video_dir):
    """저장루트 변경하는 코드"""
    pass
    export_root_path = os.path.join(os.getcwd())
    export_root_path = Path(export_root_path)

    export_json_path = get_export_path(export_root_path, path_dir, video_dir)
    export_json_path = export_json_path / path


    with open(str(export_json_path), 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



def get_export_path(path, path_dir, video_dir):
    path = Path(path)
    path = path / path_dir / video_dir

    path.mkdir(parents=True, exist_ok=True)
    return path

