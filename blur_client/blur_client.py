import os
import requests

from tkinter import *
from tkinter import filedialog, messagebox

os.environ['TK_SILENCE_DEPRECATION'] = '1'

class BlurClient:
    def __init__(self):
        self._build_interface()

    def start(self):
        self.root.mainloop()

    def _build_interface(self):
        self.root = Tk()
        self.root.title('비식별화')
        self.root.resizable(False, False)

        self.video_path = StringVar()
        label1 = Label(self.root, text='비디오 파일 경로')
        label1.grid(row=1, column=1, ipadx=3, padx=3)
        entry1 = Entry(self.root, width=30, state='readonly', textvariable=self.video_path)
        entry1.grid(row=2, column=1, ipadx=3, padx=3)

        button1 = Button(self.root, text='찾기', command=self.get_videopath)
        button1.grid(row=2, column=2, ipadx=3, padx=3, sticky='w')

        button2 = Button(self.root, text='비식별화 실행', command=self.run)
        button2.grid(row=3, column=1, columnspan=2, rowspan=2, pady=20)

    def get_videopath(self):
        filename = filedialog.askopenfilename(title='비디오 파일 선택',
                                              filetypes=[('mp4 형식', '.mp4 .MP4'),
                                                         ('avi 형식', '.avi .AVI'),
                                                         ('모든 파일', '.*')])
        self.video_path.set(filename)

    def run(self):
        try:
            video_path = self.video_path.get()
        except Exception as e:
            messagebox.showwarning('Warning', f'입력값을 가져올 수 없습니다.'
                                              f'\n잘못 입력되거나 빠진 부분이 있는지 확인해보세요'
                                              f'\nError Msg: {e}')
            return

        out_path = filedialog.asksaveasfilename(title='저장 비디오 파일 이름', initialfile='output.mp4',
                                                filetypes=[('mp4 파일', '.mp4 .MP4'),
                                                           ('모든 파일', '.*')])

        top = Toplevel(master=self.root)
        top.title('실행 중...')
        Message(top, text='비식별화 처리 중...잠시 기다려주세요', padx=20, pady=20).pack()

        self._blur_video(video_path, out_path)

        top.destroy()
        messagebox.showinfo(title='비식별화 완료',
                            message=f'비식별화가 완료되었습니다.\n저장 경로: {out_path}')

    @staticmethod
    def _blur_video(video_path, out_path):
        data = {
            'name': bytes(os.path.basename(video_path), encoding='utf8'),
            'file': open(video_path, 'rb').read(),
            'threshold': bytes('0.7', encoding='utf8'),
        }

        res = requests.post('http://dev.datamaker.io:55804/api/net/blur/', files=data)
        if res.status_code != 200:
            return False

        with open(out_path, 'wb') as out_file:
            out_file.write(res.content)

        return True

if __name__ == '__main__':
    client = BlurClient()
    client.start()
