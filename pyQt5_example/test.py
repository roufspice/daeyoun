import sys

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QDesktopWidget, QVBoxLayout, QCheckBox, \
    QLabel, QComboBox


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('Button1', self)
        btn1.setCheckable(True)
        btn1.toggle()
        # btn2 = QPushButton(self)
        # btn2.setText('Button2')

        #button
        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        # vbox.addWidget(btn2)

        #checkbox
        cb = QCheckBox('True', self)
        cb.move(20, 20)
        cb.toggle()
        cb.stateChanged.connect(self.print)

        #combo_box
        self.lbl = QLabel('Option1',self)
        self.lbl.move(30, 120)

        cb = QComboBox(self)
        cb.addItem('Option1')
        cb.addItem('Option2')
        cb.addItem('Option3')
        cb.addItem('Option4')
        cb.move(30,150)






        self.setLayout(vbox)
        self.setWindowTitle("First Application")
        self.setWindowIcon(QIcon('web.png'))  #어플리케이션의 아이콘을 설정하도록 합니다.
        # self.statusBar().showMessage('Test My App')
        # self.move(300, 300)  # 위젯을 스크린의 300, 300위치로 이동시킵니다.
        # self.resize(400, 200)  # 위젯의 크기를 너비, 높이
        self.setGeometry(300, 300, 300, 200) # ax, ay, w, h
        self.center()


        self.show()

    def print(self, state):
        if state == Qt.Checked:
            print('hello')





    # 화면 정가운데
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



if __name__ == '__main__':
    app = QApplication(sys.argv)  #모든 PyQt5 어플리케이션은 어플리케이션 객체를 생성해야 합니다.
    ex = MyApp()
    sys.exit(app.exec_())
