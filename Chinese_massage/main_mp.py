'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-04-19 14:15:06
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-04-20 17:20:06
FilePath: /Chinese_massage/Chinese_massage/main.py
Description: 使用mp来检测关键点，然后根据关键点的位置来进行按摩，效果很差，不建议使用
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
from tool.getresult_img import get_landmarks
import cv2
from tool import AipSpeech
model_path = './tool/pose_landmarker_heavy.task'


if __name__ == '__main__':
    #相机参数设置
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    get_landmarks = get_landmarks(model_path = model_path)
    while cap.isOpened():
        success, image = cap.read()
        image = cv2.flip(image, 1)

        annotated_image, x_list, y_list = get_landmarks.get_result_image(image)
        #画出第11,12,23,24个关键点，数据是归一化的。
        if len(x_list) > 1 and len(y_list) > 1:
            # print(x_list[0], y_list[0])
            cv2.circle(image, (int(x_list[11]*width), int(y_list[11]*height)), 5, (255, 0, 0), -1)
            cv2.circle(image, (int(x_list[12]*width), int(y_list[12]*height)), 5, (0, 0, 255), -1)
            cv2.circle(image, (int(x_list[23]*width), int(y_list[23]*height)), 5, (255, 0, 0), -1)
            cv2.circle(image, (int(x_list[24]*width), int(y_list[24]*height)), 5, (0, 0, 255), -1)
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(1) & 0xFF == 27:#等待按键，如果按键为27则退出循环，1ms后继续下一次循环
            break
    cap.release()
    cv2.destroyAllWindows()

