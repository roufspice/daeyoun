 #
 # def handle(self, *args, **options):
 #        date = datetime.date(2020, 11, 23)
 #        user_tasks = UserTask.objects.filter(
 #            task__project__in=[320,324],
 #            status__in=['confirmed'],
 #            last_labeled__lt=date,
 #
 #        )
 #
 #
 #        for i, user_task in enumerate(user_tasks, start=1):
 #            keypoints = {}
 #            labels = user_task.data
 #            is_keypoints = False
 #            for label in labels:
 #                if label['label']['category'] == 'point':
 #                    is_keypoints = True
 #
 #            if not is_keypoints:
 #                previous_user_task =get_user_task_previous_frame(user_task)
 #                previous_data = previous_user_task.data
 #                # print(user_task.task.project_id ,user_task.id)
 #                # print(previous_data)
 #                # print(previous_user_task.id)
 #
 #                break


#
# def get_user_task_previous_frame(user_task):
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
#
