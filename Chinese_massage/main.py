'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-06 11:49:53
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-11 14:12:59
FilePath: /Chinese_massage/main.py
Description: 使用YOLOv8模型检测人体关键点，用于穴位推拿，准确度很高。
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
import threading
import pyttsx3      #pip install pyttsx3 -i https://pypi.tuna.tsinghua.edu.cn/simple
import time         #pip install py3-tts -i https://pypi.tuna.tsinghua.edu.cn/simple
import cv2
import os
os.environ['YOLO_VERBOSE'] = str(False)#不打印yolov8信息
from ultralytics import YOLO
import numpy as np
from tool import AipSpeech
from tool import get_point

"""
交互内容:
1.医生你好，我最近鼻塞，有点小感冒，眼睛也会胀痛。
回答：你可以按揉凤池穴，请看位置

医生你好，我最近有点咳嗽
回答：你可以按揉肩中俞穴，请看位置

医生你好，我最近有点失眠，胸闷不舒服
回答：你可以按揉心俞穴，请看位置
"""


'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-06 11:58:41
description: 语音识别，并判断有无穴位关键字，用于显示穴位推拿   
param {*} name(穴位名称)
return {*}
'''
#定义全局变量，传递穴位关键字
acupoint = None
def thread_function(name1,name2,name3):     #定义一个线程函数，用于语音识别。name是检测病人的症状，从而判需要按摩的穴位
    say_eng = pyttsx3.init() #初始化一个实例
    say_name1 = "你可以按揉凤池穴，请看位置"
    say_name2 = "你可以按揉肩中俞穴，请看位置"
    say_name3 = "你可以按揉心俞穴，请看位置"
    global acupoint
    while True:
            text = AipSpeech.thread_readvoice()
            print("语音识别结果：",text)
            if name1 in text:
                print("鼻子")
                say_eng.say(say_name1)  # say 用于传递要说的文本的方法
                # say_eng.runAndWait()  # 运行并处理语音命令
                acupoint = 1
                # time.sleep(5)
            if name2 in text:
                print("咳嗽")
                say_eng.say(say_name2)
                # say_eng.runAndWait()
                acupoint = 2
                # time.sleep(5)
            if name3 in text:
                print("失眠")
                say_eng.say(say_name3)
                # say_eng.runAndWait()    
                acupoint = 3
                # time.sleep(5)
            else:
                print("未识别到病症")
            say_eng.runAndWait() 
            time.sleep(5)
            say_eng.stop()
            #释放资源
            say_eng.endLoop()



if __name__ == '__main__':
    #运行语音识别线程
    thread_1 = threading.Thread(target=thread_function, args=("鼻子","咳嗽","失眠"))
    # thread_1.start()
    # thread_1.join()
    
    # 加载YOLOv8模型 
    model = YOLO('./models/yolov8m-pose.pt')
    start_time = time.time()
    url = "./test.mp4"
    cap = cv2.VideoCapture(url)
    # 获取摄像头的长宽
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = w/3
    height = h/3
    # print(w,h)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    #保存视频
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')#mac不要用XVID，用mp4v
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (int(width), int(height)))
    while True:
        # 读取视频流
        ret, frame = cap.read()
        # frame = cv2.imread("test.png")   
        if frame is not None:
            results = model.predict(frame,conf=0.1,max_det=10,save=False)
            # 在帧上可视化结果
            frame = results[0].plot()

            #绘画关键点测试，绘画关键点，6和7
            pions = results[0].keypoints.xy
            pions_list = get_point.convert_pions(pions)
            if len(pions_list) == 0:
                continue
            # #画出所有关键点
            # for i in range(len(pions_list)):#是浮点数，需要转换成整数
            #     cv2.circle(frame, (int(pions_list[i][0]), int(pions_list[i][1])), 5, (0, 255, 255), -1)
            #     cv2.putText(frame, str(i), (int(pions_list[i][0]), int(pions_list[i][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            #凤池穴
            Fengchi_Point_xy = [(pions_list[6][0]+pions_list[5][0])/2+30,(pions_list[3][1]-pions_list[5][1])/1.5+pions_list[5][1]]
            #肩中俞穴
            Jianzhong_Point_xy = [(pions_list[6][0]+pions_list[5][0])/2+40,pions_list[5][1]]
            #心俞穴
            Xinyu_Point_xy = [(pions_list[6][0]+pions_list[5][0])/2+30,(pions_list[11][1]-pions_list[5][1])/2+pions_list[5][1]]

            #根据语音识别结果，画出需要按摩的穴位
            if acupoint == 1:
                cv2.circle(frame, (int(Fengchi_Point_xy[0]), int(Fengchi_Point_xy[1])), 10, (0, 255, 0), -1)
                cv2.putText(frame, "Fengchi_Point_xy", (int(Fengchi_Point_xy[0]), int(Fengchi_Point_xy[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if acupoint == 2:
                cv2.circle(frame, (int(Jianzhong_Point_xy[0]), int(Jianzhong_Point_xy[1])), 10, (0, 255, 0), -1)
                cv2.putText(frame, "Jianzhong_Point_xy", (int(Jianzhong_Point_xy[0]), int(Jianzhong_Point_xy[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if acupoint == 3:
                cv2.circle(frame, (int(Xinyu_Point_xy[0]), int(Xinyu_Point_xy[1])), 10, (0, 255, 0), -1)
                cv2.putText(frame, "Xinyu_Point_xy", (int(Xinyu_Point_xy[0]), int(Xinyu_Point_xy[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # 计算FPS
            fps = 1.0 / (time.time() - start_time)
            cv2.putText(frame, f"{fps:.1f} FPS", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            start_time = time.time()
            cv2.imshow("YOLOv8推理", frame)
            out.write(frame)

            # 如果按下'q'则中断循环
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # 如果视频结束则中断循环
            print("视频结束")
            break
    cv2.destroyAllWindows()
    cap.release()
    out.release()