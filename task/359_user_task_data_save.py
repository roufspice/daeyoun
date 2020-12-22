"""20201221_314,313,317"""


def handle(self, *args, **options):
    test_data = {'file': '35_7.png', 'batch': 1, 'group': '-2020-10-15-Mapmaker1-RF_0-238-image0'}
    get_bug = []

    previous_user_tasks = UserTask.objects.filter(
        task__project__in=[317, 314, 313],
        status__in=['discarded']
    )
    tasks = Task.objects.filter(
        project__in=[359]
    )
    print(tasks.count())
    # user_tasks = UserTask.objects.filter(
    #     task__project__in=[359]
    # )

    total_count = previous_user_tasks.count()
    save_num = 0

    for i, previous_user_task in enumerate(previous_user_tasks, start=1):

        print(f'{i}/{tasks.count()}')
        previous_raw_data = previous_user_task.task.raw_data.data

        try:
            task = tasks.get(raw_data__data=previous_raw_data)
            if task.id == 6095925:
                print(task.id)

                task.data = previous_user_task.data
                task.save()

                break





        except (Task.DoesNotExist, Task.MultipleObjectsReturned):
            continue
