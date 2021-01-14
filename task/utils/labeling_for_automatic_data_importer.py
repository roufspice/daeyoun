# def handle(self, *args, **options):
#     origin_data = {'file': '35_7.png', 'batch': 1, 'group': '-2020-10-15-Mapmaker1-RF_0-238-image0'}
#
#     get_bug = []
#     previous_user_tasks = UserTask.objects.filter(
#         task__project__in=[317, 314, 313],
#         status__in=['discarded']
#     )
#     user_tasks = UserTask.objects.filter(
#         task__project__in=[359]
#     )
#
#     total_count = previous_user_tasks.count()
#
#     for i, previous_user_task in enumerate(previous_user_tasks, start=1):
#         print(f'{i}/{total_count}')
#         if i > 5:
#             break
#
#         previous_raw_data = previous_user_task.task.raw_data.data
#
#         for user_task in user_tasks:
#
#             raw_data = user_task.task.raw_data.data
#
#             if previous_raw_data == raw_data:
#                 try:
#                     # user_task.data = previous_user_task.data
#                     print(user_task.id)
#                     print(previous_user_task.id)
#                     # print(previous_user_task.data)
#                     # user_task.save()
#
#
#                 except AttributeError as e:
#                     get_bug.append(user_task.id)
#                     print(e)