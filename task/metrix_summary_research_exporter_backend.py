import os
import subprocess
from datetime import date
import hashlib
import tablib
from pathlib import Path
from django import forms
from django.conf import settings

from apps.dataset.base_backends.exporter_backend import BaseExportBackend


class ExportBackend(BaseExportBackend):
    file_excel_path = forms.CharField(
        label='메타정보 엑셀파일 경로',
        help_text='NAS의 projects 폴더에 위치한 엑셀 파일의 경로를 "/" 로 구분하여 입력해주세요.<br>'
                  '예) "metrix_summary/file.xlsx"를 입력하면 NAS의 "projects/metrix_summary/file.xlsx"에서 불러옵니다.'
    )

    # metadata_xlsx = os.path.join(settings.PROJECT_ROOT, 'metrix_summary', '기타', '영상요약_메타정보.xlsx')

    def clean(self):
        cleaned_data = super().clean()
        file_excel_path = cleaned_data.get('file_excel_path')
        if file_excel_path:
            file_excel_path = Path(os.path.join(settings.PROJECT_ROOT, file_excel_path))
            if not file_excel_path.exists():
                self.add_error('file_excel_path', '엑셀파일이 존재하지 않습니다. 경로를 확인해 주세요')

        return cleaned_data

    def export_dataset(self):
        user_tasks = self.get_user_tasks()
        file_excel_path = self.configuration['file_excel_path']
        file_excel_path = os.path.join(settings.PROJECT_ROOT, file_excel_path)
        file_excel = open(file_excel_path, 'rb')
        dataset_metadata = tablib.import_set(file_excel, format='xlsx')

        count_total = user_tasks.count()

        dataset = []
        file_name_to_data = {}
        seconds_to_index = {}

        for row in dataset_metadata.dict:
            file_name_to_data[row['파일명']] = {
                'video_name': row['영상명'],
                'video_length': row['영상 길이'],
                'video_quality': row['화질(720p/ 1080p)'],
                'video_license': row['라이선스'],
                'start_ad': row['광고시작구간'],
                'end_ad': row['광고종료구간']
            }

        for counter, i in enumerate(range(0, 100000, 3)):
            number_range = range(i, i + 3)
            seconds_to_index[number_range] = counter

        # 파일명 -> 영상길이

        headers = [
            '카테고리',
            'ID',
            '파일명',
            '영상명',
            '영상길이',
            '화질',
            '라이선스',
            '광고시작구간',
            '광고종료구간',
            '3초 단위 구간',
            '주요 장면',
            '대표 장면'
        ]
        dataset=[]
        path_remove = '/mnt/projects/metrix_summary/'

        for i, user_task in enumerate(user_tasks, start=1):
            self.set_progress(i, count_total, description='내보내는 중')

            file_path = user_task.task.raw_data.data['file']
            file_path = file_path.replace(path_remove, '')
            file_path = Path(file_path)

            category = file_path.stem.split('_')[1]

            category = ''.join([i for i in category if not i.isdigit()])
            user_id = abs(hash(user_task.user.name))
            file_name = file_path.stem.replace('압축버전_', '')
            video_name = file_name_to_data[file_name]['video_name']
            # video_length = file_name_to_data[file_name]['video_length']

            try:
                video_length = user_task.task.raw_data.data['video_length']
            except KeyError:
                # video_length = get_video_length(user_task.task.raw_data.file.path)
                video_length = get_video_duration(user_task.task.raw_data.file.path)

            video_quality = file_name_to_data[file_name]['video_quality']
            video_license = file_name_to_data[file_name]['video_license']
            start_ad = file_name_to_data[file_name]['start_ad']
            end_ad = file_name_to_data[file_name]['end_ad']

            # 유저태스크 데이터 정리 구간
            data = user_task.data
            markings = data['marked_times']

            # 3초 단위 구간
            try:
                raw_data_video_length = user_task.task.raw_data.data['video_length']
            except KeyError:
                raw_data_video_length = get_video_duration(user_task.task.raw_data.file.path)
                user_task.task.raw_data.data['video_length'] = raw_data_video_length
                user_task.task.raw_data.save()

            is_divisible_three = False

            if raw_data_video_length % 3 == 0:
                is_divisible_three = True
            raw_data_video_length = int(raw_data_video_length)
            section_three_seconds = ''

            for key, value in seconds_to_index.items():
                if raw_data_video_length in key:
                    section_three_seconds = value
                    if is_divisible_three:
                        section_three_seconds -= 1

            section_three_seconds = list(range(0, section_three_seconds + 1))
            section_three_seconds = [str(number) for number in section_three_seconds]

            # 주요 장면
            major_sections = []
            for key, marking in markings.items():
                try:
                    # major_sections.append(int((marking['range_index'] - 1) / 3))
                    major_sections.append(int(marking['range_index'] / 3))
                except TypeError:
                    pass

            major_sections = [str(number) for number in major_sections]

            # 대표 장면
            primary_sections = []
            for key, marking in markings.items():
                checked = marking['checked']
                range_index = marking['range_index']
                if checked:
                    for k, v in seconds_to_index.items():
                        if range_index in k:
                            primary_sections.append(v)

            primary_sections = [str(number) for number in primary_sections]

            # dataset.append([
            #     category,
            #     user_id,
            #     file_name,
            #     video_name,
            #     video_length,
            #     video_quality,
            #     video_license,
            #     start_ad,
            #     end_ad,
            #     ', '.join(section_three_seconds),
            #     ', '.join(major_sections),
            #     ', '.join(primary_sections)
            # ])

            dataset.append({
                '카테고리': category,
                'ID': user_id,
                '파일명': file_name,
                '영상명': video_name,
                '영상길이': video_length,
                '화질': video_quality,
                '라이선스': video_license,
                '광고시작구간': start_ad,
                '광고종료구간': end_ad,
                '3초 단위 구간':', '.join(section_three_seconds),
                '주요 장면': ', '.join(major_sections),
                '대표 장면': ', '.join(primary_sections),
            })

        # today = date.today().isoformat()
        # export_path = os.path.join(settings.EXPORT_ROOT, self.configuration['export_path'])
        # file_saved_name = f'{today}research_export.xlsx'
        # file_saved_name = Path(file_saved_name)
        #
        # with open(os.path.join(export_path, file_saved_name), 'wb') as f:
        #     f.write(dataset.xlsx)

        self.save_xlsx(dataset, 'test.xlsx')


def get_video_duration(file_path):
    duration = float(subprocess.check_output(
        ['ffprobe', '-i', file_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of',
         'csv=%s' % ('p=0')]))

    return duration
