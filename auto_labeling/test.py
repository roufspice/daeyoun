class DetectronAPI:
    def __init__(self, config=f'{os.path.dirname(__file__)}/config/yaml/default_keypoint.yaml', **kwargs):
        self._load_config(config, **kwargs)
        self.predictor = DefaultPredictor(self.cfg)

    def _load_config(self, config, **kwargs):
        self.cfg_manager = ConfigManager(config)
        self.cfg_manager.set(**kwargs)
        self.cfg = self.cfg_manager()
        self.metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])

    @staticmethod
    def _register_dataset(dataset):
        dataset.register()
        dataset.build_metadata()

    def infer(self, url, enable_default=False):
        image = self.url_to_image(url)
        pred_json = self.infer_image(image)

        if enable_default and not pred_json:
            pred_json = self.get_default_box(image)

        return pred_json

    def infer_image(self, image):
        outputs = self.predictor(image)
        instances = outputs['instances'].to('cpu')

        pred_json = self.pred_to_json(instances)

        return pred_json

    def pred_to_json(self, instances):
        """
        Parse instance structure into JSON
        """
        pred_json = []
        try:
            num_instances = len(instances)
        except NotImplementedError:
            return pred_json
        for i in range(num_instances):
            x0, y0, x1, y1 = instances.pred_boxes[i].tensor.tolist()[0]
            inst_json = {
                'box': {
                        'x': int(x0),
                        'y': int(y0),
                        'width': int(x1 - x0),
                        'height': int(y1 - y0),
                    },
                'score': float(instances.scores[i].item()),
                'class': self.metadata.thing_classes[instances.pred_classes[i].item()],
            }

            if hasattr(instances, 'pred_keypoints'):
                json_keypoints = []
                for j, keypoint in enumerate(instances.pred_keypoints[i]):
                    inst_key = {
                        'label': {
                            'data': {
                                'x': int(keypoint[0].item()),
                                'y': int(keypoint[1].item()),
                            },
                            'category': 'point',
                        },
                        'classification': {
                            'code': self.metadata.keypoint_names[j],
                            'attributes': [],
                        },
                        'score': keypoint[2].item(),
                    }
                    json_keypoints.append(inst_key)
                inst_json['keypoints'] = json_keypoints

            if hasattr(instances, 'pred_masks'):
                inst_json['polygon'] = self.mask_to_polygon(instances.pred_masks[i])

            pred_json.append(inst_json)
        return pred_json

    @staticmethod
    def url_to_image(url):
        image = io.imread(url)
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    @staticmethod
    def mask_to_polygon(mask, eps0=0.01):
        image = torch.zeros_like(mask, dtype=torch.uint8).masked_fill(mask, 255).cpu().numpy()

        contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        eps = eps0 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, eps, True)
        approx = approx[:, 0, :].tolist()

        pts = [{'x': x, 'y': y} for x, y in approx]
        return pts

    @staticmethod
    def get_default_box(image):
        h, w, c = image.shape
        pred_json = [{
            'box': {
                'x': w // 4,
                'y': h // 4,
                'width': w // 2,
                'height': h // 2,
            },
            'score': 0.5,
            'class': 'cat',
        }]
        return pred_json

    def dump(self, name):
        with open(name, 'wb') as f:
            pickle.dump(self, f)

    def visualize(self, data):
        if isinstance(data, str):
            image = self.url_to_image(data)
        else:
            image = data

        outputs = self.predictor(image)
        instances = outputs['instances'].to('cpu')
        visualizer = Visualizer(image[:, :, ::-1], self.metadata, scale=1.0)
        output = visualizer.draw_instance_predictions(instances)
        out_image = output.get_image()[:, :, ::-1]
        return out_image


def main(*args, **kwargs):
    """
    kwargs 포맷
    {
        'config': config 파일 path,
        'path': 이미지 경로,
    }
    """
    path = kwargs['path']
    config = kwargs['config']
    tracker = DetectronAPI(config)
    return tracker.infer(path)


if __name__ == '__main__':
    # import argparse
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--config', type=str, required=True,
    #                     help='Input config file')
    # parser.add_argument('--save', type=str, required=True,
    #                     help='Output dir')
    # args = parser.parse_args()
    #
    # tracker = DetectronAPI(args.config)
    # tracker.dump(args.save)
    from glob import glob
    from dataset.import_metrix_pet import MetrixPet

    mp = MetrixPet()
    mp.register()
    mp.build_metadata()

    tracker = DetectronAPI('./config/yaml/default_keypoint.yaml',
                           MODEL__ROI_HEADS__NUM_CLASSES=2,
                           SOLVER__MAX_ITER=100000,
                           OUTPUT_DIR='models/metrix_pet',
                           DATASETS__TRAIN=('metrix_pet',),
                           DATASETS__TEST=(),
                           MODEL__ROI_KEYPOINT_HEAD__NUM_KEYPOINTS=15,
                           MODEL__WEIGHTS='./models/metrix_pet/model_final.pth')

    images = glob('/home/ubuntu/sample/20201209/**/*.jpg', recursive=True)

    for im_path in images:
        image = tracker.visualize(im_path)
        out_path = im_path.replace('20201209', '20201209_out', 1)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        cv2.imwrite(out_path, image)
