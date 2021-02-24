import tablib
import time

import math

from pprint import pprint

import json

import os

from django.core.management import BaseCommand

from apps.task.models import UserTask


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("run_evaluation")



def main():


    headers = ['1 코', '2 이마', '3 입꼬리',
               '4 아래 입술 중앙', '5 목', '6 오른쪽 앞다리 시작',
               '7 왼쪽 앞다리 시작', '8 오른쪽 앞발목', '9 왼쪽 앞발목',
               '10 오른쪽 대퇴골', '11 왼쪽 대퇴골', '12 오른쪽 뒷발목',
               '13 왼쪽 뒷발목', '14 꼬리 시작', '15 꼬리 끝', '정확도']


    dataset = tablib.Dataset(headers)
    t1 = Evaluation()
    kwargs = {
        '1': 0.02, '3': 0.02, '4': 0.02,

    }
    t1.set_boundary_ratio_detail(**kwargs)
    correctness, params = t1.main()

    dataset.append([
        params['1'],params['2'],params['3'],
        params['4'],params['5'],params['6'],
        params['7'],params['8'],params['9'],
        params['10'],params['11'],params['12'],
        params['13'],params['14'],params['15'],
        correctness
    ])

    save_excel(dataset)


def save_excel(data):
    export_root = os.path.join(os.getcwd(), '정확도_테스트.xlsx')
    with open(export_root, 'wb') as f:
        f.write(data.export('xlsx'))
    print("완료")



class Evaluation:
    """오토라벨링 정확도 측정 클래스"""


    def __init__(self):
        self.code_batch_ratio = 0.05

        self.code_boundary_detail_ratio = {str(i): self.code_batch_ratio for i in range(1, 16)}

        self.radius_set = None




    def set_boundary_ratio_detail(self, **kwargs):
        for k, v in kwargs.items():
            self.code_boundary_detail_ratio[k] = v

        print(self.code_boundary_detail_ratio)


    def main(self):

        annotation_random_json_path = os.path.join(os.getcwd(), 'metrix_pet_annotation_random.json')
        with open(annotation_random_json_path, encoding='utf-8') as f:
            random_json = json.load(f)

        auto_label_json_path = os.path.join(os.getcwd(), 'random_auto_label.json')
        with open(auto_label_json_path, encoding='utf-8') as f:
            auto_label_json = json.load(f)


        "user_task_id로 해당 데이터 접근"
        total_correct = 0
        answer_count = self.get_answer_count(random_json)
        print(f'랜덤 추출 프레임 총 개수: {answer_count}')
        temp_answer_count = 0
        for file in random_json:
            annotations = file['annotations']
            for anno in annotations:
                temp_answer_count += 1
                id = anno["id"]

                user_task = UserTask.objects.get(pk=id)

                frame_url = user_task.task.raw_data.file.path
                video_path = user_task.task.raw_data.data['file_video']

                radius_set = self.get_radius(user_task)
                print(radius_set)
                labels = user_task.data

                correct = 0
                for label in labels:
                    # pprint(labels)
                    if label['label']['category'] =='point':
                        x = label['label']['data']['x']
                        y = label['label']['data']['y']
                        code = label['classification']['code']

                        a_x, a_y = self.get_auto_keypoint(auto_label_json, video_path, frame_url, code)
                        # print(a_x, a_y)
                        dist = self.get_dist_btn_keypoints(x, y, a_x, a_y)

                        inpoint = (dist <= radius_set[str(code)])

                        if inpoint:
                            correct +=1
                        else:
                            pass

                correct /= 15
                total_correct += correct
            print(f"temp_correctness: {total_correct / temp_answer_count}")

        print(f"_correctness: {total_correct / answer_count}")

        return (total_correct / answer_count) ,self.code_boundary_detail_ratio



    def get_dist_btn_keypoints(self, x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** self.code_batch_ratio


    def get_radius(self, user_task):

        radius_set = {}
        code_boundary_detail_ratio = self.code_boundary_detail_ratio
        for k, v in code_boundary_detail_ratio.items():

            try:
                labels = user_task.data
                for label in labels:
                    if label['label']['category'] == 'rect':
                        w = label['label']['data']['width']
                        h = label['label']['data']['height']
                        diagonal = math.sqrt((w * w) + (h * h))
                        radius = diagonal * code_boundary_detail_ratio[k]
                        radius_set[k] = radius

            except Exception:
                pass
        self.radius_set = radius_set
        return radius_set


    def get_auto_keypoint(self, data, video_path, frame_url, code):
        """오토라벨링 키포인트 찾기"""
        x, y = 0, 0
        try:
            annotations = [file["annotations"] for file in data if file["video_path"] == str(video_path)]
            keypoints = [anno['keypoints'] for anno in annotations[0] if anno['frame_url'] == str(frame_url)]
            data = [keypoint['label']['data'] for keypoint in keypoints[0] if keypoint['classification']['code'] == str(code)][0]
            x, y = data['x'], data['y']

        except IndexError:
            pass

        return x, y
    #     for file in data if file["video_path"]:
    #         annotations = file["annotations"]
    #         keypoints = [anno['keypoints'] for anno in annotations if anno['frame_url'] == str(frame_url)]
    #         data = [keypoint["label"]["data"] for keypoint in keypoints if keypoint["classification"]["code"] == str(code)]


    def get_answer_count(self, data):
        answer_count = 0
        for file in data:
            annotations = file["annotations"]
            for frame in annotations:
                answer_count +=1

        return answer_count
