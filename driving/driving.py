import glob
import os
import json
from pathlib import Path
from natsort import natsorted
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import Label, Frame, filedialog, messagebox


def validate_directory(directory):
    no_files = True
    for ext in ['.jpg', '.png', '.JPG', '.PNG']:
        if any(f.endswith(ext) for f in os.listdir(directory)):
            no_files = False
            break

    if no_files:
        messagebox.showerror('오류', '이미지 파일을 찾을 수 없습니다.')

    if not any(f.endswith('.json') for f in os.listdir(directory)):
        messagebox.showerror('오류', 'JSON 파일을 찾을 수 없습니다.')
        return False

    return True


def downscale(image):
    width = 1080
    w_ratio = width/float(image.size[0])
    height = int((float(image.size[1])*float(w_ratio)))
    return image.resize((width, height), Image.ANTIALIAS)


def get_data(image_path):
    image_path = Path(image_path)
    json_path = image_path.parent / f'{image_path.stem}.json'
    if not json_path.exists():
        return []

    with open(str(json_path)) as f:
        return json.load(f)['annotations']


def draw(image_draw, annotations):
    polygon = []
    for annotation in annotations:
        print(annotation)
        category = annotation['category']
        data = annotation['data']

        if category == 'polygon':
            points = []
            for point in data:
                points.append((point['x'], point['y']))
            polygon.append(points)

        elif category == 'polyline':
            polyline = []
            for point in data:
                polyline.append(point['x'])
                polyline.append(point['y'])

            image_draw.line(polyline, fill='cyan')

        elif category == 'rect':
            box = list(data.values())
            box[2] += box[0]
            box[3] += box[1]
            image_draw.rectangle(box, outline='lime')

        elif category == 'point':
            r = 3
            x = data['x']
            y = data['y']
            left = (x-r, y-r)
            right = (x+r, y+r)
            image_draw.ellipse((left, right), fill='red')

    for points in polygon:
        image_draw.polygon(points, outline='yellow')


class Viewer(tk.Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('datamaker')
        self.master.minsize(250, 100)
        self.master.bind('<Left>', self.seek_previous)
        self.master.bind('<Right>', self.seek_next)

        self.images = []
        self.index = -1
        self.index_label = tk.StringVar()
        self.file_name_label = tk.StringVar()
        self.current_image = None

        self.frame = Frame(self)
        tk.Button(self.frame, text="폴더 열기", command=self.open).pack(side=tk.LEFT)
        # tk.Button(self.frame, text="이전", command=self.seek_previous).pack(side=tk.LEFT)
        # tk.Button(self.frame, text="다음", command=self.seek_next).pack(side=tk.LEFT)
        Label(self.frame, textvariable=self.index_label).pack(side=tk.LEFT)
        Label(self.frame, textvariable=self.file_name_label).pack(side=tk.LEFT)
        inst = tk.StringVar()
        inst.set('좌, 우 방향키로 이동하세요')
        Label(self.frame, textvariable=inst).pack(side=tk.RIGHT)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.label = Label(self)
        self.label.pack()
        self.pack()

    def load_image(self):
        image_path = self.images[self.index]
        image = Image.open(image_path, 'r')
        image = image.convert('RGB')

        annotations = get_data(image_path)
        if annotations:
            image_draw = ImageDraw.Draw(image)
            draw(image_draw, annotations)

        image = downscale(image)
        self.current_image = ImageTk.PhotoImage(image)
        self.label.config(
            image=self.current_image,
            width=self.current_image.width(),
            height=self.current_image.height()
        )

    def open(self):
        directory = Path(filedialog.askdirectory(title="폴더 선택"))

        os.chdir(directory)
        is_valid = validate_directory(directory)

        if not is_valid:
            return

        self.index = 0
        self.current_image = None
        self.images = []

        for ext_pattern in ['*.jpg', '*.png']:
            for file in glob.glob(ext_pattern):
                self.images.append(file)

        self.images = natsorted(self.images)
        self.load_image()
        self.set_labels()

    def seek_previous(self, event):
        self.index -= 1
        # if first
        if self.index < 0:
            self.index = 0

        self.current_image = self.images[self.index]
        self.load_image()
        self.set_labels()

    def seek_next(self, event):
        self.index += 1
        # if last
        if self.index > len(self.images):
            self.index = len(self.images) - 1

        self.load_image()
        self.set_labels()

    def set_labels(self):
        self.index_label.set(f'{self.index + 1}/{len(self.images)}')
        self.file_name_label.set(f'{Path(self.images[self.index]).name}')


if __name__ == "__main__":
    Viewer().mainloop()
