import os
from datetime import datetime

from django.conf import settings


def save_log(save_root_path, task_id):
    """로그파일 생성관리"""
    today = datetime.date.today().isoformat()

    log_data = f'{task_id}\t{save_root_path}\t{today}\n'
    log_directory = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/358/log_txt')
    with open(log_directory, 'a+t') as f:
        f.write(log_data)