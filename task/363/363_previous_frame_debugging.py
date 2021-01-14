def debug_363_previous_frame():
    user_tasks = UserTask.objects.filter(
        task__project__in=[363],
        status__in=['in_progress', 'stand_by'],

    )
    dataset = tablib.Dataset(headers=['user_task_id', 'user_task_frame', 'user_task_previous', 'previous_raw_data'])
    count_total = user_tasks.count()
    # previous_frame
    for i, user_task in enumerate(user_tasks, start=1):
        print(f'{i}/{count_total}')
        if i > 500:
            continue
        data = user_task.task.raw_data.data

        frame = data.get('frame')
        group = data.get('file_video')
        if frame is not None and group:
            user_task_previous = UserTask.objects.filter(
                data__isnull=False,
                task__project=user_task.task.project,
                task__raw_data__data__frame__lt=frame,
                task__raw_data__data__file_video=group,
            ).order_by('-task__raw_data__data__frame').first()

        # print(f'{user_task.id} {user_task_previous.id} {user_task_previous.task.raw_data.data}')
        try:

            dataset.append([
                user_task.id,
                user_task.task.raw_data.data['frame'],
                user_task_previous.id,
                user_task_previous.task.raw_data.data
            ])
        except AttributeError:
            pass

    directory = os.path.join(settings.EXPORT_ROOT, 'datamaker')
    file_name = '363_check_list_2.xlsx'
    with open(os.path.join(directory, file_name), 'wb') as f:
        f.write(dataset.export('xlsx'))