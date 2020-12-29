# 사용자태스크에 할당할 user를 지정함
# 어떤 태스크를 불러올거냐 (할당되지 않은것들) 할당되지 않은 것들에 대해서 __isnull
# 여러개의 object를 생성할 때 bulk_create()메소드를 사용
# 하나의 쿼리로 여러 개의 object를 생성 - bulk_create()
# create() 메소드는 하나의 쿼리를 거치는 과정이라 비효율적임
# update(): QuerySet의 objects를 한번에 수정할 수 있음.
# generally only 1 query, no matter how many objects there are

# user = User.objects.get(email='ai@datamaker.io')
# tasks = Task.objects.filter(user_tasks__isnull=True, project_id=358)
#
# print(tasks.count())
#
# user_tasks = []
#
# for task in tasks:
#     # print(task.id)
#     user_tasks.append(UserTask(
#         user=user,
#         task=task,
#         status='stand_by',
#         percentage_distribution=0,
#         is_paid=True,
#     ))
#
# UserTask.objects.bulk_create(user_tasks)
#
# # 사전바운딩박스 ai 작업처리
# for i, user_task in enumerate(user_tasks, start=1):
#     print(f'{i}/{len(user_tasks)}')
#     post_participate(user_task)
#
# # user_task = UserTask.objects.get(id=6564450)
# # post_participate(user_task)