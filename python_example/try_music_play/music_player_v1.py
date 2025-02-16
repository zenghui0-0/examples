import sys
from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QAction, QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon, QColor, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt


class MusicPlayerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initMediaPlayer()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('音乐播放器')
        self.setGeometry(300, 300, 400, 300)

        # 设置深色背景
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: #D8DEE9;
            }
            QListWidget {
                background-color: #4C566A;
                color: #D8DEE9;
                border: 1px solid #5E81AC;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #4C566A;
                color: #D8DEE9;
                border: 1px solid #5E81AC;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
            QLabel {
                color: #D8DEE9;
            }
        """)

        # 自定义标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏默认标题栏
        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(30)
        self.title_bar.setStyleSheet("background-color: #3B4252;")

        # 标题栏布局
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0)

        # 标题
        self.title_label = QLabel('音乐播放器', self.title_bar)
        self.title_label.setStyleSheet("font-weight: bold;")
        title_layout.addWidget(self.title_label)

        # 最小化按钮
        self.btn_minimize = QPushButton('—', self.title_bar)
        self.btn_minimize.setFixedSize(20, 20)
        self.btn_minimize.clicked.connect(self.showMinimized)
        title_layout.addWidget(self.btn_minimize)

        # 关闭按钮
        self.btn_close = QPushButton('×', self.title_bar)
        self.btn_close.setFixedSize(20, 20)
        self.btn_close.clicked.connect(self.close)
        title_layout.addWidget(self.btn_close)

        # 音乐列表
        self.music_list = QListWidget(self)
        self.music_list.addItems(["music1.mp3", "music2.mp3", "music3.mp3"])  # 添加音乐文件
        self.music_list.itemClicked.connect(self.select_music)

        # 播放/暂停按钮
        self.btn_play_pause = QPushButton('播放', self)
        self.btn_play_pause.clicked.connect(self.toggle_music)

        # 底部按钮布局
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.btn_play_pause)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.music_list)
        main_layout.addLayout(bottom_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.png'))  # 设置托盘图标，需要准备一个 icon.png 文件

        # 创建托盘的右键菜单
        tray_menu = QMenu()
        restore_action = QAction("恢复", self)
        quit_action = QAction("退出", self)
        restore_action.triggered.connect(self.restore_from_tray)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

        # 绑定托盘图标双击事件
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def initMediaPlayer(self):
        # 初始化媒体播放器
        self.media_player = QMediaPlayer(self)
        self.current_music = None
        self.is_playing = False

    def select_music(self, item):
        # 选择音乐
        self.current_music = item.text()
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.current_music)))
        self.btn_play_pause.setText('播放')

    def toggle_music(self):
        # 切换音乐播放状态
        if not self.current_music:
            QMessageBox.warning(self, '提示', '请先选择一首音乐！')
            return

        if self.is_playing:
            self.media_player.pause()
            self.btn_play_pause.setText('播放')
            self.is_playing = False
        else:
            self.media_player.play()
            self.btn_play_pause.setText('暂停')
            self.is_playing = True

    def closeEvent(self, event):
        # 重写关闭事件，提供最小化到托盘的选项
        reply = QMessageBox.question(
            self,
            '最小化到托盘',
            '是否最小化到托盘？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            event.ignore()  # 忽略关闭事件
            self.minimize_to_tray()
        else:
            event.accept()  # 接受关闭事件
            self.quit_app()

    def minimize_to_tray(self):
        # 最小化到托盘
        self.hide()
        self.tray_icon.show()
        self.tray_icon.showMessage('提示', '程序已最小化到托盘')

    def restore_from_tray(self):
        # 从托盘恢复窗口
        self.showNormal()  # 恢复窗口
        self.activateWindow()  # 激活窗口
        self.tray_icon.hide()  # 隐藏托盘图标

    def on_tray_icon_activated(self, reason):
        # 双击托盘图标恢复窗口
        if reason == QSystemTrayIcon.DoubleClick:
            self.restore_from_tray()

    def quit_app(self):
        # 退出应用程序
        self.media_player.stop()  # 停止音乐播放
        self.tray_icon.hide()
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    music_player = MusicPlayerApp()
    music_player.show()
    sys.exit(app.exec_())