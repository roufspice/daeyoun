"""나스에 다운로드된 해당 이미지 익스포트 되기전에 승인으로 처리하는 로직"""

# nas에 재작업필요한 폴더에서 이미지파일 찾기
# not_bounding_img_root = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/ai_bounding_box_img/2_재작업필요/')
# checked_bounding_img_root = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/ai_bounding_box_img/1_확인됨/')
#
# if os.path.exists(not_bounding_img_root):
#     file_list = os.listdir(not_bounding_img_root)
#     not_ai_file_list = [int(file.replace(".jpg", "")) for file in file_list if file.endswith('.jpg')]
#
# print(len(not_ai_file_list))
#
# if os.path.exists(checked_bounding_img_root):
#     file_list = os.listdir(checked_bounding_img_root)
#     checked_ai_file_list = [int(file.replace(".jpg","")) for file in file_list if file.endswith('.jpg')]
#
# print(len(checked_ai_file_list))


# user = User.objects.get(email='ai@datamaker.io')
# bounding_box 없는경우 제거,
# user_tasks = UserTask.objects.filter(
#     task__project__in=[358],
#     data__isnull=False,
#     id__in=checked_ai_file_list,
# ).exclude(id__in=not_ai_file_list)
# #
# count_total = user_tasks.count()
# #
# print(count_total)
# for i, user_task in enumerate(user_tasks, start=1):
#     print(f'{i}/{count_total}')
#     if not user_task.status == 'confirmed':
#
#         user_task.status = 'confirmed'
#         user_task.save()
#