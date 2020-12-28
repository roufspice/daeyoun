# # metadata_path = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/데이터메이커 구축량 현황.xlsx')
#         # file_excel = open(metadata_path, 'rb')
#         # dataset_metadata = tablib.import_set(file_excel, format='xlsx')
#
#         user_tasks = UserTask.objects.filter(
#             task__project__in=[324, 320],
#             status__in=['confirmed'],
#
#         )
#
#         paths_video = user_tasks.values_list('task__raw_data__data__file_video', flat=True)
#         paths_video = list(set(list(paths_video)))
#         print(len(paths_video))
#         dataset = {}
#
#         headers = ['축종', '행동(영문)', '구축량(json)', '구축량(이미지)']
#
#         databook = tablib.Dataset(headers=headers)
#
#         for i, path_video in enumerate(paths_video, start=1):
#             print(f'{i}/{len(paths_video)}')
#             # json 파일 갯수는 paths_video갯수랑 동일함
#             path_video_relative = path_video.replace('/mnt/projects/metrix_pet/고객업로드/', '')
#
#             video_name = Path(path_video_relative).stem
#             species = video_name.split("-")[0]
#             movement = f'{species}{video_name.split("-")[1]}'
#
#
#             if not movement in dataset:
#                 dataset[movement] = {
#                     'json_count': 1,
#                     'frame_count': 0,
#                     'species': species,
#                 }
#             else:
#                 dataset[movement]['json_count'] += 1
#
#
#
#             user_tasks_video = user_tasks.filter(
#                 task__raw_data__data__file_video=path_video,
#             ).order_by(
#                 'task__raw_data__data__frame'
#             ).distinct('task__raw_data__data__frame')
#
#             # print(user_tasks_video.count())
#             dataset[movement]['frame_count'] += user_tasks_video.count()
#
#
#         for key, value in dataset.items():
#             databook.append([
#                 value['species'],
#                 key,
#                 value['json_count'],
#                 value['frame_count']
#             ])
#
#
#         export_path = os.path.join(settings.EXPORT_ROOT, 'metrix_pet')
#         if os.path.exists(export_path):
#
#             with open(os.path.join(export_path, 'json_build_amounts_01.xlsx'), 'wb') as f:
#                 f.write(databook.export('xlsx'))
