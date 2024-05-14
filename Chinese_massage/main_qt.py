'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-11 14:16:06
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-11 15:57:19
FilePath: /Chinese_massage/main_qt.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
import sys
 
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QPushButton, QWidget
from PyQt6.QtGui import QPixmap, QImage, QGuiApplication
from PyQt6.QtCore import QThread, pyqtSignal
import cv2
import Process_Audio
import os
os.environ['YOLO_VERBOSE'] = str(False)#不打印yolov8信息
from ultralytics import YOLO
 
class AudioRecognitionThread(QThread):
    finished = pyqtSignal(str)

    def run(self):
        acupoint = Process_Audio.thread_function("鼻子", "咳嗽", "失眠")
        acupoint_str = str(acupoint)  # 将结果转换为字符串
        self.finished.emit(acupoint_str)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_thread = AudioRecognitionThread()
        self.audio_thread.finished.connect(self.audio_recognition_finished)

        self.medel = YOLO('./models/yolov8m-pose.pt')
        self.acupoint = 0
        self.setWindowTitle('中医推拿系统')
        self.btn_read_voice = QPushButton('语音识别')
        self.btn_camera = QPushButton('打开摄像头')  # 控制摄像头的状态
        self.lbl_img = QLabel('显示摄像头图像')  # 创建标签控件来显示摄像头的图像, 标签的大小由QGridLayout的布局来决定
        self.lbl_img.setStyleSheet('border: 1px solid black;')  # 给标签设置黑色边框
        self.lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 让标签要显示的内容居中
        self.lbl_img.setMinimumSize(640, 480)  # 宽和高保持和摄像头获取的默认大小一致
        self.btn_camera.clicked.connect(self.btn_camera_click)
        self.btn_read_voice.clicked.connect(self.btn_read_voice_click)
        top_widget = QWidget()  # 创建一个顶层窗口部件
        grid = QGridLayout()# 创建一个网格布局
        grid.addWidget(self.lbl_img, 0, 0, Qt.AlignmentFlag.AlignTop)  # 放置顶部
        grid.addWidget(self.btn_camera, 1, 0, Qt.AlignmentFlag.AlignBottom)  # 放置底部,Qt.AlignmentFlag.AlignBottom是指定按钮放在底部
        grid.addWidget(self.btn_read_voice, 1, 1, Qt.AlignmentFlag.AlignBottom)

        top_widget.setLayout(grid)
        self.setCentralWidget(top_widget)   # 设置窗口的中心部件
 
        self.center_win()  # 居中显示主窗口
 
        self.is_open_camera = False  # 是否打开了摄像头标志位
        self.video_cap = None
        self.camera_timer = QtCore.QTimer(self)  # 创建读取摄像头图像的定时器
        self.camera_timer.timeout.connect(self.play_camera_video)   # 定时器超时信号连接到槽函数play_camera_video
 
    def center_win(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def btn_read_voice_click(self):
        # self.acupoint = Process_Audio.thread_function("鼻子","咳嗽","失眠")
        # print("穴位关键字：",self.acupoint)
        self.audio_thread.start()

    def audio_recognition_finished(self, acupoint):
        self.acupoint = acupoint
        print("穴位关键字：", acupoint)
        # 处理语音识别完成后的逻辑
    def btn_camera_click(self):
        print("self.acupoint",self.acupoint)
        if not self.is_open_camera: # 按下 打开摄像头 按钮
            self.video_cap = cv2.VideoCapture(0)  # 打开默认摄像头（索引为0）
            print('camera fps:', self.video_cap.get(cv2.CAP_PROP_FPS))
            # 每个20毫秒获取一次摄像头的图像进行刷新, 具体设置多少合适, 可以参考你的摄像头帧率cv2.CAP_PROP_FPS,
            # 刷新频率设置一个小于 1000 / cv2.CAP_PROP_FPS 的值即可
            self.camera_timer.start(20)  # 20毫秒刷新一次
            self.is_open_camera = True
            self.btn_camera.setText('关闭摄像头')
        else:  # 按下 关闭摄像头 按钮
            self.camera_timer.stop()
            self.video_cap.release()
            self.video_cap = None
            self.lbl_img.clear()
            self.btn_camera.setText('打开摄像头')
            self.is_open_camera = False
 
    def play_camera_video(self):
        if self.is_open_camera:
            # ret, frame = self.video_cap.read()  # 读取视频流的每一帧
            # self.video_cap.grab()   # 读取视频流的每一帧
            _, frame = self.video_cap.read()  # 读取视频流的每一帧
            frame = Process_Audio.process_fram(self.medel,frame,self.acupoint)
            # frame = Process_Audio.process_fram(self.medel,frame,1)
            # print("SELF.ACUPONT",self.acupoint)
            height, width, channel = frame.shape  # 获取图像高度、宽度和通道数, 通常为为640x480x3
            # opencv获取的图像默认BGR格式
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 转换BRG 到 RGB
            # 或者
            # 将OpenCV格式转换成QImage格式, 需要进行颜色通道交换(.rgbSwapped())
            img = QImage(frame.data, width, height, QImage.Format.Format_RGB888)
            img = img.rgbSwapped()  # 进行颜色通道交换，rgbSwapped是因为OpenCV读取的图像是BGR格式的，而QImage是RGB格式的
            pixmap = QPixmap.fromImage(img)  # 从QImage生成QPixmap对象
            pixmap = QPixmap(pixmap).scaled(
                self.lbl_img.width(), self.lbl_img.height(),
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.lbl_img.setPixmap(pixmap)  # 在标签上显示图片
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()   #会循环执行函数MainWindow.play_camera_video()           
    sys.exit(app.exec())