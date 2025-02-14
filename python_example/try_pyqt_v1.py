import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)

        # 设置标题栏背景颜色
        self.setStyleSheet("background-color: #2E3440;")

        # 标题栏图标和标题
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(QIcon("icon.png").pixmap(16, 16))  # 替换为你的图标路径
        self.title_label = QLabel("Custom Qt Application", self)
        self.title_label.setStyleSheet("color: #ECEFF4; font-size: 14px;")

        # 最小化按钮
        self.minimize_button = QPushButton("-", self)
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #4C566A;
                color: #ECEFF4;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        self.minimize_button.clicked.connect(self.parent.showMinimized)

        # 最大化按钮
        self.maximize_button = QPushButton("□", self)
        self.maximize_button.setFixedSize(20, 20)
        self.maximize_button.setStyleSheet("""
            QPushButton {
                background-color: #4C566A;
                color: #ECEFF4;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        self.maximize_button.clicked.connect(self.toggle_maximize)

        # 关闭按钮
        self.close_button = QPushButton("×", self)
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #BF616A;
                color: #ECEFF4;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #D08770;
            }
        """)
        self.close_button.clicked.connect(self.parent.close)

        # 将控件添加到布局中
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.title_label)
        self.layout.addStretch()  # 添加弹性空间
        self.layout.addWidget(self.minimize_button)
        self.layout.addWidget(self.maximize_button)
        self.layout.addWidget(self.close_button)

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Qt Application")
        self.resize(800, 600)

        # 设置无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置主界面内容
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 添加自定义标题栏
        self.title_bar = CustomTitleBar(self)
        self.layout.addWidget(self.title_bar)

        # 添加内容区域
        self.content = QWidget(self)
        self.content.setStyleSheet("background-color: #3B4252;")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(10, 10, 10, 10)

        # 添加一个示例内容（标签）
        self.label = QLabel("This is the main content area.", self.content)
        self.label.setStyleSheet("color: #ECEFF4; font-size: 16px;")
        self.content_layout.addWidget(self.label)

        self.layout.addWidget(self.content, stretch=1)  # 设置内容区域可以拉伸

        # 设置任务栏托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # 替换为你的图标路径
        self.tray_menu = QMenu()
        self.show_action = QAction("Show", self)
        self.show_action.triggered.connect(self.show)
        self.tray_menu.addAction(self.show_action)
        self.quit_action = QAction("Quit", self)
        self.quit_action.triggered.connect(self.close)
        self.tray_menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        # 设置深色背景样式
        self.set_dark_theme()

    def set_dark_theme(self):
        # 设置全局样式表
        dark_stylesheet = """
            QWidget {
                background-color: #2E3440;
                color: #ECEFF4;
            }
            QMenu {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
            }
            QMenu::item:selected {
                background-color: #4C566A;
            }
            QSystemTrayIcon {
                background-color: #2E3440;
            }
        """
        self.setStyleSheet(dark_stylesheet)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Info", "Application minimized to tray.")
        QApplication.quit()

    def keyPressEvent(self, event):
        # 捕获 Ctrl+C 快捷键
        if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
