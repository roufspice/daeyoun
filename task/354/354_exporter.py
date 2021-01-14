"""
354번 프로젝트의 4개 태스크를 동일한 7명이 작업한 결과물을 엑셀로 뽑고 싶어서요.
"""

# users = UserTask.objects.filter(
#     task__project__in=[354],
#     status__in=['inspecting'],
#     task__in=[6938829, 6938765, 6938764, 6286228],
# ).values_list('user', flat=True)
#
# users_list = list(set(list(users)))
#
# for user in users_list:
#     user_tasks = UserTask.objects.filter(
#         task__project__in=[354],
#         status__in=['inspecting'],
#         task__in=[6938829, 6938765, 6938764, 6286228],
#         user=user,
#     )
#     # data_book
#     databook = tablib.Databook()
#     for user_task in user_tasks:
#         headers = ['id', 'variation', 'option']
#         dataset = tablib.Dataset(title=str(user_task.task.id), headers=headers)
#
#         timelines = user_task.data['timelines']
#         # id
#         for _, val in timelines.items():
#             # id
#             id = val['id']
#             try:
#                 # variation
#                 variation = val['variation']
#             except KeyError:
#                 variation = None
#             try:
#                 # option
#                 attributes = val['attributes']['kind']
#             except KeyError:
#                 attributes = None
#
#             dataset.append([
#                 id,
#                 variation,
#                 attributes,
#
#             ])
#         #
#         # print(dataset)
#
#         databook.add_sheet(dataset)
#
#     directory = os.path.join(settings.EXPORT_ROOT, 'datamaker')
#     with open(os.path.join(directory, f'354_{user}_.xlsx'), 'wb') as f:
#         f.write(databook.export(format='xlsx'))
#
#     #
#     print('success')