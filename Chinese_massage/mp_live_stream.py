'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-04-02 14:52:56
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-04-06 20:12:30
FilePath: /test/test.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from draw_wds import draw_landmarks_on_image

model_path = './pose_landmarker_heavy.task'

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

detecte_result = None
# Create a pose landmarker instance with the live stream mode:
def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global detecte_result
    # annotated_image = draw_landmarks_on_image(image, result)
    # cv2.imshow("Annotated Image", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
    # cv2.waitKey(0)  # 等待按下任意键
    # cv2.destroyAllWindows()
    detecte_result = result



options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result
    )

landmarker =  PoseLandmarker.create_from_options(options)
  
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
while cap.isOpened():
    star_time = time.time()
    # time.sleep(0.1) 
    success, image = cap.read()  #读取到的图像是BGR格式，不是RGB格式。是numpy.ndarray类型
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    frame_timestamp_ms = int(time.time() * 1000)
    landmarker.detect_async(mp_image, frame_timestamp_ms)
    fps = 1 / (time.time() - star_time)
    if detecte_result is not None:
        annotated_image = draw_landmarks_on_image(image, detecte_result)
        cv2.putText(annotated_image, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('MediaPipe Pose Landmark', annotated_image)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()