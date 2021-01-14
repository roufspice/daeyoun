import json
import os

from django.conf import settings


def export(UserTask):
    user_tasks = UserTask.objects.filter(
                task__project__in=[320, 324],
                status__in=['confirmed']
            )

    paths_video = user_tasks.values_list('task__raw_data__data__file_video', flat=True)
    paths_video = list(set(list(paths_video)))

    count_total = user_tasks.count()
    print(len(paths_video))
    for i, path_video in enumerate(paths_video, start=1):
        path_video_relative = path_video.replace('/mnt/projects/metrix_pet/고객업로드/', '')
        annotations = []
        metadata = None

        user_tasks_video = user_tasks.filter(
            task__raw_data__data__file_video=path_video,
            ).order_by(
                'task__raw_data__data__frame'
            ).distinct('task__raw_data__data__frame')

        for user_task in user_tasks_video:
            labels = user_task.data or []
            raw_data = user_task.task.raw_data

            frame_data = raw_data.data
            image_path = raw_data.file.path

            # image_width, image_height = get_image_size(image_path)

            keypoints = {}
            bounding_box = None

            for label in labels:
                try:
                    if label['label']['category'] == 'point':
                        keypoint = {
                            'x': label['label']['data']['x'],
                            'y': label['label']['data']['y']
                        }

                        if not is_point_within(image_width, image_height, keypoint):
                            keypoint = None

                        keypoints[label['classification']['code']] = keypoint

                    elif label['label']['category'] == 'rect':
                        # Todo 바운더리 넘어가는 바운딩박스 체크
                        bounding_box = label['label']['data']

                        is_bounding_box_within_width(bounding_box, image_width, image_height)


                except KeyError:
                    pass

            annotation = {
                'frame_number': frame_data.get('frame'),
                'frame_url': f'https://dashboard.datamaker.io{raw_data.file.url}',
                'timestamp': frame_data.get('timestamp'),
                'keypoints': keypoints,
                'bounding_box': bounding_box
            }

            annotations.append(annotation)

            path_json = os.path.join(path_video.replace('.mp4', '.json'))

            try:
                with open(path_json) as file_json:
                    metadata = json.load(file_json)
            except IOError:
                pass

            dataset = {
                'file_video': path_video_relative,
                'metadata': metadata,
                'annotations': annotations
            }

            file_name_json = path_video_relative.replace('/', '_')
            path = os.path.join(settings.EXPORT_ROOT, 'metrix_pet/1215/')
            file_name_json = os.path.join(path, file_name_json)


            with open(f'{file_name_json}.json', 'w') as f:
                json.dump(dataset, f, indent=4, ensure_ascii=False)

                print(f'{i}/{len(paths_video)}')



def is_point_within(width, height, point):
    return point['x'] <= width and point['y'] <= height


def is_bounding_box_within_width(bounding_box, image_width, image_height):
    """바운딩박스 범위 체크 함수"""
    is_bounding_width = True if bounding_box['x'] + bounding_box['width'] <= image_width else False
    is_bounding_height = True if bounding_box['y'] + bounding_box['height'] <= image_height else False

    if not is_bounding_width:
        bounding_box['width'] = (image_width - bounding_box['x'])
    if not is_bounding_height:
        bounding_box['height'] = (image_height - bounding_box['y'])

    return all([is_bounding_width, is_bounding_height])


def is_keypoints_within_bounding_box(annotation):

    bounding_box = annotation["bounding_box"]
    keypoints = annotation["keypoints"]

    start_point_x = bounding_box['x']
    end_point_x = bounding_box['x'] + bounding_box['width']
    start_point_y = bounding_box['y']
    end_point_y = bounding_box['y'] + bounding_box['height']

    for key, value in keypoints.items():
        x = value['x']
        y = value['y']

        result_y = False if y < start_point_y or y > end_point_y else True
        result_x = False if x < start_point_x or x > end_point_x else True

        if not all([result_x, result_y]):
            print(keypoints[key])
            keypoints[key] = None