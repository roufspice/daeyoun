#         #TODO keypoints 복사하기 324,320
#         date = datetime.date(2020, 11, 24)
#         user_tasks = UserTask.objects.filter(
#             task__project__in=[320, 324],
#             status__in=['confirmed'],
#             last_labeled__lt=date,
#         )
#
#
#         count_total = user_tasks.count()
#
#         headers = ['project_id', 'user_task_id', 'previous_user_task.id']
#         dataset = tablib.Dataset(headers=headers)
#
#         for i, user_task in enumerate(user_tasks, start=1):
#
#             print(f'{i}/{count_total}')
#             labels = user_task.data
#             is_keypoints = False
#             for label in labels:
#                 if label['label']['category'] == 'point':
#                     is_keypoints = True
#
#             # 키포인트 없는경우
#             if not is_keypoints:
#                 keypoints = []
#                 previous_user_task = get_user_task_previous_frame(user_task)
#                 previous_data = previous_user_task.data
#                 # print(user_task.task.project_id, user_task.id, previous_user_task.id)
#
#                 # boundingbox 제외하고 넣기
#                 for label in previous_data:
#                     # print(previous_data)
#
#                     try:
#                         if label['label']['category'] == 'point':
#                             keypoints.append(label)
#
#                     except KeyError:
#                         pass
#
#                 # print(keypoints)
#
#                 for keypoint in keypoints:
#                     user_task.data.append(keypoint)
#
#                 user_task.save()
#
#                 dataset.append([
#                     user_task.task.project_id,
#                     user_task.id,
#                     previous_user_task.id,
#                 ]
#                 )
#                 # print(dataset)
#
#         directory = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/통계')
#         file_name = 'metrix_pet_keypoints_is_saved_list.xlsx'
#         file_path = os.path.join(directory, file_name)
#
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#
#         with open(file_path, 'wb') as f_output:
#             f_output.write(dataset.xlsx)
#
#
# def get_user_task_previous_frame(user_task):
#
#     user_task_previous = None
#
#     data = user_task.task.raw_data.data
#
#     frame = data.get('frame')
#     file_video = data.get('file_video')
#
#     if frame is not None and file_video:
#         user_task_previous = UserTask.objects.filter(
#             data__isnull=False,
#             task__project=user_task.task.project,
#             task__raw_data__data__file_video=file_video,
#             task__raw_data__data__frame__lt=frame
#         ).order_by('-task__raw_data__data__frame').first()
#
#     return user_task_previous