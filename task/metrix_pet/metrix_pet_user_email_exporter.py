import os

import tablib
from django.conf import settings


def export(UserTask, User):

    """12_18_이메일주소 출력"""
    headers = ['이름', '이메일주소']
    dataset = tablib.Dataset(headers=headers)

    user_tasks = UserTask.objects.filter(
        task__project__in=[324]

    )
    users = User.objects.filter(user_projects__project_id=324).distinct()

    for i, user in enumerate(users, start=1):
        try:
            print(f'{i}/{users.count()}')
            user_name = user.name
            user_email = user.email

        except IndexError as e:
            print(e)



        dataset.append([
            user_name,
            user_email,
        ])


    export_root = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/user_emails.xlsx')
    with open(export_root, 'wb') as f:
        f.write(dataset.xlsx)
