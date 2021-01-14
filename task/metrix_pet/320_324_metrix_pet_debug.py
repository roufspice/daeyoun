# TODO 320,324 json debugging - 누락건
# user_tasks = UserTask.objects.filter(
#     task__project__in=[320, 324],
#     status__in=['confirmed']
# )
#
# count_total = user_tasks.count()
# headers = ['project','file_path', 'user_task_id', 'keypoints_code', 'frame_number', 'time_stamp']
# dataset = tablib.Dataset(headers=headers)
# default_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
#
# for i, user_task in enumerate(user_tasks, start=1):
#     print(f'{i}/{count_total}')
#     raw_data = user_task.task.raw_data
#     frame_data = raw_data.data
#     file_path = raw_data.data['file_video'].replace("/mnt/projects/metrix_pet/고객업로드/", "")
#     frame_number= frame_data.get('frame')
#     time_stamp = frame_data.get('timestamp')
#
#     datas = user_task.data
#     code_list = []
#     is_null = False
#     for data in datas:
#         try:
#             if data['label']['category'] == 'point':
#                 code = data['classification']['code']
#                 code_list.append(int(code))
#         except KeyError:
#             pass
#
#     # key_point_code 누락된 경우
#     for num in default_list:
#         if not num in code_list:
#             is_null = True
#
#     if is_null:
#         # 누락된 값이 존재하면,
#         dataset.append([
#             user_task.task.project.id,
#             file_path,
#             user_task.id,
#             code_list,
#             frame_number,
#             time_stamp
#         ])
#
# print(dataset)
# directory = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/통계/')
# file_name = '320_324_키포인트오류 확인리스트.xlsx'
# with open(os.path.join(directory, file_name), 'wb') as f:
#     f.write(dataset.export('xlsx'))