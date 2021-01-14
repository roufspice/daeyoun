import os
import cv2
from pathlib import Path

from django.conf import settings


def export(Task):
    
    """
    20_12_18_
    이미지 해상도 변경 및 다운로드 관련 코드_301 프로젝트  """
    # Task_id 추출!
    
    tasks = Task.objects.filter(project__in=[358])
    tasks_id = tasks.values_list('id', flat=True)
    tasks_id = list(set(list(tasks_id)))
    total_count = len(tasks_id)
    
    for i, task_id in enumerate(tasks_id, start=1):
        # 태스크아이디로 그 태스크를 찾고, 해당 raw_data.data.경로를 찾기!
        # task_id는 파일명 path_video는 디렉토리명
    
        task = Task.objects.filter(id=task_id).distinct()
        path_video = task.values_list('raw_data__data__file_video', flat=True)
        path_video = list(path_video).pop(0)
        path_video = Path(path_video).name
    
        file_path = task.values_list('raw_data__file')
        file_path = list(file_path).pop(0)
        file_path = file_path[0]
    
        file_name = os.path.join(settings.MEDIA_ROOT, file_path)
    
        # 이미지 불러오기
        img = cv2.imread(file_name, cv2.IMREAD_COLOR)
    
        # img_modified = auto_boundingbox(img)
        print(img.shape)
    
        # 이미지 세이브하기
        save_root_path = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/358')
        save_root_path = Path(save_root_path)
        save_root_path = save_root_path / path_video
        # print(save_root_path)
    
        # 폴더가 없을 경우 자동 생성
        save_root_path.mkdir(exist_ok=True)
        save_root_path = save_root_path / f'{task_id}.jpg'
    
    
        cv2.imwrite(str(save_root_path), img)
    
        print(f'{i}/{total_count}')
    
        if i > 5:
            break
