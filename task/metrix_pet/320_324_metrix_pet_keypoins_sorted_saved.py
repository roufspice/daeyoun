#
# file_excel_path = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/통계/metrix_pet_keypoints_is_saved_list.xlsx')
# file_excel = open(file_excel_path, 'rb')
# dataset_excel = tablib.import_set(file_excel, format='xlsx')
#
# # print(dataset_excel)
#
# dataset = []
#
# for row in dataset_excel.dict:
#     # print(row['user_task_id'])
#     dataset.append(row['user_task_id'])
#
#
#
# print(len(dataset))
#
# user_tasks = UserTask.objects.filter(
#     task__project__in=[320 ,324],
#     id__in=dataset
# )
# headers = ['user_task_id']
# dataset_saved = tablib.Dataset(headers=headers)
#
# for i, user_task in enumerate(user_tasks, start=1):
#
#     print(f'{i}/{user_tasks.count()}')
#     # print(user_task.id)
#     datas = user_task.data
#     # 가장 위쪽 첫번째 label이 바운딩박스 선택
#     if datas[0]['label']['category'] == 'rect':
#         dataset.append(user_task.id)
#         # print(datas)
#         # print("==============")
#         for data in datas:
#             if data['label']['category'] == 'rect':
#                 rect = data
#                 datas.remove(data)
#                 datas.append(rect)
#
#         # print(datas)
#         # print("==============")
#
#         for data in datas:
#             if not datas[0]['classification']['code'] == '1' :
#
#                 code = data['classification']['code']
#
#                 if not data['label']['category'] == 'rect' :
#                     data['classification']['code'] = str(int(code) -1)
#
#         # print(datas)
#         # print("==============")
#
#         print(user_task.id)
#         user_task.save()
#
#         dataset_saved.append([
#             user_task.id
#         ])
#
# # print(dataset_saved)
#
# directory = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/통계')
# file_name = 'metrix_pet_keypoins_sorted_saved_list.xlsx'
# file_path = os.path.join(directory, file_name)
#
# with open(file_path, 'wb') as f_output:
#     f_output.write(dataset_saved.xlsx)
