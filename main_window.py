
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pynput.mouse import Listener, Button
from easygoogletranslate import EasyGoogleTranslate
import sys,re
import pyperclip
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit

translator = EasyGoogleTranslate(
    source_language='-',
    target_language='zh-CN',
    timeout=10
)
class UpdateThread(QThread):

    update_text = pyqtSignal(str)

    def run(self):
            def on_click(x, y, button, pressed):
                #print('All threads:', QThread.allThreads())
                if button == Button.left:
                    if not pressed:
                        self.update_text.emit('not pressed')


            # Collect events until released
            with Listener(on_click=on_click) as listener:
                listener.join()
class MainWindow(QMainWindow):
    def __init__(self, clipboard, parent=None):
        super(MainWindow, self).__init__(parent)
        self.clipboard = clipboard  # 存储传入的clipboard对象
        self.setGeometry(100, 500, 500,700)


        self.clipboard_text = ""
        #self.setWindowFlags(QWidget)

        #self.setFixedSize(450, 300)


        self.textbox = QTextEdit(self)


        self.setCentralWidget(self.textbox)

        self.textbox.setStyleSheet("background-color: black; color: white;")


        self.textbox.installEventFilter(self)
        self.drag_pos = None


        self.setWindowTitle('☀')

        self.start_thread()

        container = QWidget(self)

        # 创建一个水平布局
        layout = QHBoxLayout(container)

        # 创建并配置第一个 checkbox
        self.checkbox = QCheckBox("Open", self)
        self.checkbox.setShortcut(QKeySequence("Alt+t"))
        layout.addWidget(self.checkbox)

        # 创建并配置第二个 checkbox
        self.checkbox2 = QCheckBox("Mark", self)
        self.checkbox2.setChecked(True)
        self.checkbox2.setShortcut(QKeySequence("Alt+y"))
        layout.addWidget(self.checkbox2)

        self.checkbox3 = QCheckBox("With original text", self)
        # self.checkbox3.setChecked(True)
        self.checkbox3.setShortcut(QKeySequence("Alt+u"))
        layout.addWidget(self.checkbox3)

        # 将容器 widget 设置为 menu widget
        self.setMenuWidget(container)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        font = self.textbox.font()
        font_size = 26
        font.setPointSize(font_size)
        self.textbox.setFont(font)


    def check_clipboard(self,text):

       # print(self.checkbox.isChecked())
       #  print('click')
        if not self.checkbox.isChecked():
            pass
           # print("未勾选")
        else:
            if self.checkbox2.isChecked():
                # print('1')

                pyautogui.hotkey("ctrl","c")
            # print('2')

            clipboard =  self.clipboard.text()
            # print('3')

            if isinstance(clipboard,str) and len(clipboard)<3000:

                if "\n" in clipboard:
                    # print('4')

                    clipboard = re.sub(r'\s+', ' ', clipboard.strip())
                # print('5')

                # 如果剪贴板内容发生变化，更新文本框中的内容
                if clipboard != self.clipboard_text:

                    self.clipboard_text = clipboard
                    translation=translator.translate(self.clipboard_text)
                    print(clipboard)
                    print(translation)
                    try:

                        if self.checkbox3.isChecked():
                            self.textbox.setText(translation+'\n'+self.clipboard_text)
                        else:
                            self.textbox.setText(translation)
                    except:
                        print("error")

    def start_thread(self):
        thread = UpdateThread(self)
        thread.update_text.connect(self.check_clipboard)
        thread.start()



    def eventFilter(self, obj, event):
        if obj is self.textbox and event.type() == QEvent.MouseButtonPress:
            if event.buttons() == Qt.LeftButton:
                self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            else:
                self.drag_pos = None
        elif event.type() == QEvent.MouseMove and self.drag_pos is not None:
            self.move(event.globalPos() - self.drag_pos)
        elif event.type() == QEvent.Wheel and event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                font = self.textbox.font()
                font_size = font.pointSize() + 1
                font.setPointSize(font_size)
                self.textbox.setFont(font)
            elif event.angleDelta().y() < 0:
                font = self.textbox.font()
                font_size = font.pointSize() - 1
                if font_size > 0:
                    font.setPointSize(font_size)
                    self.textbox.setFont(font)
            return True

        return super().eventFilter(obj, event)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    clipboard = app.clipboard()
    window = MainWindow(clipboard)
    window.show()
    sys.exit(app.exec_())
