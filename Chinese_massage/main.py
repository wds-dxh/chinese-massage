'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-06 11:49:53
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-06 11:59:35
FilePath: \Chinese_massage\main.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
import pyttsx3
import time
import cv2
import os
os.environ['YOLO_VERBOSE'] = str(False)#不打印yolov8信息
from ultralytics import YOLO
import numpy as np
from tool import AipSpeech

'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-06 11:58:41
description: 语音识别，并判断有无穴位关键字，用于显示穴位推拿   
param {*} name(穴位名称)
return {*}
'''
#定义全局变量，传递穴位关键字
acupoint = None
say_eng = pyttsx3.init() #初始化一个实例
say = True
say_name1 = "穴位1，"
say_name2 = "穴位2，"
say_name3 = "穴位3，"
def thread_function(name1,name2,name3):     #定义一个线程函数，用于语音识别。name是检测病人的症状，从而判需要按摩的穴位
    global acupoint
    #如果按下g键，调用语音识别
    if cv2.waitKey(1) & 0xFF == ord("g"):
        text = AipSpeech.thread_readvoice()
        if name1 in text:
            say_eng.say(say_name1)  # say 用于传递要说的文本的方法
            say_eng.runAndWait()  # 运行并处理语音命令
            acupoint = 1
        if name2 in text:
            say_eng.say(say_name2)
            say_eng.runAndWait()
            acupoint = 2
        if name3 in text:
            say_eng.say(say_name3)
            say_eng.runAndWait()    
            acupoint = 3
    else:
        acupoint = None
        say_eng.say("未识别到穴位关键字")  # say 用于传递要说的文本的方法
        say_eng.runAndWait()








if __name__ == '__main__':

    # 加载YOLOv8模型
    model = YOLO('./models/yolov8x-pose.pt')


    start_time = time.time()
    cap = cv2.VideoCapture(0)
    while True:
        # 读取视频流
        ret, frame = cap.read()
        # 在该帧上运行YOLOv8推理
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
        if frame is not None:
            
            results = model.predict(frame,conf=0.45,imgsz=(640, 480),max_det=3,save=False)
            # 在帧上可视化结果
            annotated_frame = results[0].plot()
            

            # 计算FPS
            fps = 1.0 / (time.time() - start_time)
            cv2.putText(annotated_frame, f"{fps:.1f} FPS", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            start_time = time.time()
            cv2.imshow("YOLOv8推理", annotated_frame)

            # 如果按下'q'则中断循环
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # 如果视频结束则中断循环
            break


    cv2.destroyAllWindows()