def keypoints_answer_export_dataset():
    """345_키포인트 답변 데이터 json"""
    user_tasks = UserTask.objects.filter(
        task__project_id__in=[345],
        status__in=['completed'],


    )
    total_count = user_tasks.count()
    dir_name = '_frames_fps_5_start_-1.00_end_-1.00_'
    annotations = []
    for i, user_task in enumerate(user_tasks, start=1):
        print(f'{i}/{total_count}')

        try:
            raw_data = user_task.task.raw_data
            raw_data_data = raw_data.data
            fps = raw_data_data['fps']
            frame_number = raw_data_data['frame']
            timestamp = raw_data_data['timestamp']
            file_video = raw_data_data['file_video']
            file_video = Path(file_video)
            suffix = file_video.suffix.replace(".", "_")
            root_name = f'{dir_name}{file_video.stem}{suffix}'

            frame_url = file_video.parent / root_name / f'frame_{frame_number}_timestamp_{timestamp}.jpg'

            user_task_data = user_task.data

            polygon = {}
            bounding_box = None

            if not user_task_data:
                continue

            for code in range(1, 16):
                polygon[str(code)] = None

            for data in user_task_data:
                try:
                    if data['label']['category'] == 'polygon':
                        polygon_data = data['label']['data']
                        polygon[data['classification']['code']] = polygon_data

                    elif data['label']['category'] == 'rect':
                        bounding_box = data['label']['data']


                except KeyError:
                    pass

            annotation = {
                'frame_url': f'{frame_url}',
                'frame_number': frame_number,
                'timestamp': timestamp,
                'polygon': polygon,
                'bounding_box': bounding_box
            }
            # print(annotation)

            annotations.append(annotation)

        except Exception as e:
            error_message = str(e)
            print(e)


        file_name_json = '345_answer_polygon_data_'
        save_json(annotations, f'{file_name_json}.json', file_name_json)



def save_json(data, path, file_name):
    # dir_name = Path(file_name).stem
    # dir_name = dir_name.split("_")[-1]
    export_root_path = os.path.join(settings.EXPORT_ROOT, f'datamaker/{file_name}')
    export_root_path = Path(export_root_path)
    export_root_path.mkdir(parents=True, exist_ok=True)

    export_json_path = export_root_path / path
    with open(str(export_json_path), 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)