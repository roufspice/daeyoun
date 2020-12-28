"""시간복잡도 하나"""

def handle(self, *args, **options):
    previous_user_tasks = UserTask.objects.filter(
        task__project__in=[317, 314, 313],
        status__in=['discarded']
    ).values('task__raw_data__id', 'data')

    tasks = Task.objects.filter(
        project__in=[359]
    )

    dataset = {}
    for i, user_task in enumerate(previous_user_tasks, start=1):
        raw_data_id = user_task['task__raw_data__id']
        dataset[raw_data_id] = user_task['data']

    total_count = tasks.count()
    saved = 0
    for task in tasks:

        if task.data:
            continue

        try:
            data = dataset[task.raw_data.id]
        except KeyError:
            data = None

        if data:
            saved += 1
            task.data = {'user_task_data': data}
            task.save()

        print(saved, total_count)

    previous_user_tasks = UserTask.objects.filter(
        task__project__in=[317, 314, 313],
        status__in=['discarded']
    )

    tasks = Task.objects.filter(
        project__in=[359]
    )

    total_count = previous_user_tasks.count()
    save_num = 0
    time_start = time.time()
    for i, previous_user_task in enumerate(previous_user_tasks, start=1):

        if i >= 190:
            break
        previous_raw_data = previous_user_task.task.raw_data.data

        try:
            task = tasks.get(raw_data__data=previous_raw_data)
            # if not task.data:
            task.data = {}
            task.data['user_task_data'] = previous_user_task.data
            # task.save()
            print(f'{i}/{previous_user_tasks.count()}:saved')


        except (Task.DoesNotExist, Task.MultipleObjectsReturned):
            continue

    time_end = time.time()

    print(time_end - time_start)

    print(save_num)
