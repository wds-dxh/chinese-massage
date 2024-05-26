'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-05-06 17:50:26
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-05-20 14:09:02
FilePath: /Chinese_massage/test.py
Description: 读取摄像头视频并保存图片
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''

import cv2 # 导入opencv库
import os
import time


def save_camera_image():
    cap = cv2.VideoCapture(0)  # 打开摄像头
    if not cap.isOpened():
        print('无法打开摄像头')
        return
    # 获取摄像头的默认分辨率
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print('摄像头的默认分辨率为:', width, height)
    # 设置摄像头的分辨率为640x480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print('摄像头的分辨率为:', width, height)

    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            # 保存图片
            file_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.jpg'
            cv2.imwrite(file_name, frame)
            print('保存图片:', file_name)
        elif key == ord('q'):
            break   

if __name__ == '__main__':
    save_camera_image()
    