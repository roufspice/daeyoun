# def handle(self, *args, **options):
#     # 358
#     user_tasks = UserTask.objects.filter(
#         task__project__in=[358]
#     )
#
#     total_count = user_tasks.count()
#
#     # user_tasks_data = user_tasks.values('id', 'data')
#
#     # export_root = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/통계/ai_temp/')
#
#     for i, user_task in enumerate(user_tasks, start=1):
#         print(f'{i}/{total_count}')
#
#         export_root = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/통계/ai_temp/')
#         # export_root = 'C:\\Users\\daeyo\\Desktop\\ai_temp\\'
#         image_path = user_task.task.raw_data.file.path
#         image_path = os.path.join(settings.MEDIA_ROOT, image_path)
#         # print(image_path)
#
#         img_name = user_task.id
#
#         if user_task.data:
#             for label in user_task.data:
#                 bounding_box = label['label']['data']
#                 # print(bounding_box)
#                 top_left = (bounding_box['x'], bounding_box['y'])
#                 bottom_right = (
#                 (bounding_box['x'] + bounding_box['width']), (bounding_box['y'] + bounding_box['height']))
#                 # print(top_left, bottom_right)
#
#         if os.path.exists(image_path):
#             img_temp = cv2.imread(image_path, cv2.IMREAD_COLOR)
#             cv2.rectangle(img_temp, top_left, bottom_right, (0, 0, 255))
#             export_root = os.path.join(export_root, f"{img_name}.jpg")
#             # print(export_root)
#             cv2.imwrite(export_root, img_temp)
#
#         if i > 100:
#             break


# def handle(self, *args, **options):
#     user_tasks = UserTask.objects.filter(
#         task__project__in=[358]
#     )
#
#     total_count = user_tasks.count()
#     dataset = []
#
#     for i, user_task in enumerate(user_tasks, start=1):
#         data = {}
#         print(f"{i}/{user_tasks.count()}")
#         data['id'] = user_task.id
#         data['image_path'] = user_task.task.raw_data.file.path
#         data['data'] = user_task.data
#         dataset.append(data)
#
#         if i > 10:
#             break
#
#     start = time.time()
#     for i, data in enumerate(dataset, start=1):
#         print(f'image_download: {i}/{len(dataset)}')
#         export_root = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/ai_bounding_box_img/')
#         image_path = data['image_path']
#         img_name = data['id']
#         labels = data['data']
#         top_left = (0, 0)
#         bottom_right = (0, 0)
#         if labels:
#             for label in labels:
#                 bounding_box = label['label']['data']
#                 top_left = (bounding_box['x'], bounding_box['y'])
#                 bottom_right = (
#                 (bounding_box['x'] + bounding_box['width']), (bounding_box['y'] + bounding_box['height']))
#
#         else:
#             pass
#         img_temp = cv2.imread(image_path, cv2.IMREAD_COLOR)
#         cv2.rectangle(img_temp, top_left, bottom_right, (0, 0, 255), 3)
#         export_root = os.path.join(export_root, f"{img_name}.jpg")
#         cv2.imwrite(export_root, img_temp)
#
#     print(time.time() - start)
