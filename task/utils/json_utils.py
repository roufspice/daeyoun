import json
import os


def main():
    input_path = os.path.join(os.getcwd(), '20210112_cat_1_cat-arch-006178.mp4.json')
    json_f = load_json(input_path)
    new_fn = '안녕'
    new_action = '읏차'

    json_new = modified_json(json_f, new_fn, new_action)
    print(json_new)

    new_path = os.path.join(os.getcwd(), 'sample.json')
    save_json(new_path, json_new)



def load_json(input_path):
    with open(str(input_path), encoding='UTF8') as f:
        return json.load(f)


def modified_json(json, new_fn, new_action):
    json['file_video'] = str(new_fn)
    json['metadata']['action'] = str(new_action)
    return json

def save_json(new_path, data):
    with open(new_path, 'w', encoding='UTF8') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)



if __name__ == '__main__':
    main()

