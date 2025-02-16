import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt

# 广告页面
class AdPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # 主界面引用
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('广告页面')
        self.setGeometry(100, 100, 400, 300)

        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 添加广告图片
        self.ad_label = QLabel(self)
        pixmap = QPixmap('ad_image.jpg')  # 替换为你的广告图片路径
        self.ad_label.setPixmap(pixmap)
        self.ad_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.ad_label)

        # 添加倒计时标签
        self.countdown_label = QLabel('3', self)
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet('font-size: 30px; color: red;')
        layout.addWidget(self.countdown_label)

        # 添加跳过按钮
        self.skip_button = QPushButton('跳过广告', self)
        self.skip_button.clicked.connect(self.close_ad)
        layout.addWidget(self.skip_button)

        # 设置布局
        self.setLayout(layout)

        # 初始化倒计时
        self.countdown = 3

        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)  # 每秒触发一次

    def update_countdown(self):
        self.countdown -= 1
        self.countdown_label.setText(str(self.countdown))

        if self.countdown <= 0:
            self.timer.stop()
            self.close_ad()  # 关闭广告页面

    def close_ad(self):
        self.close()  # 关闭广告页面
        self.main_window.show()  # 显示主界面


# 主界面
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('主界面')
        self.setGeometry(100, 100, 400, 300)

        # 创建一个标签
        label = QLabel('欢迎回到主界面！', self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('font-size: 24px; color: blue;')

        # 设置主界面布局
        self.setCentralWidget(label)


# 主程序
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建主界面
    main_window = MainWindow()

    # 创建广告页面
    ad_page = AdPage(main_window)
    ad_page.show()  # 显示广告页面

    sys.exit(app.exec_())