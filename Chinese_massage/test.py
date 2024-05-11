'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-06 17:50:26
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-11 15:22:58
FilePath: /Chinese_massage/test.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class AudioRecognitionThread(QThread):
    finished = pyqtSignal(str)

    def run(self):
        acupoint = Process_Audio.thread_function("鼻子", "咳嗽", "失眠")
        self.finished.emit(acupoint)

class MainWindow(QMainWindow):
    def __init__(self):
        # 其他代码...

        self.audio_thread = AudioRecognitionThread()
        self.audio_thread.finished.connect(self.audio_recognition_finished)

    def btn_read_voice_click(self):
        self.audio_thread.start()

    def audio_recognition_finished(self, acupoint):
        print("穴位关键字：", acupoint)
        # 处理语音识别完成后的逻辑

# 其他代码...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
