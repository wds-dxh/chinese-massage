'''
Author: wds-dxh wdsnpshy@163.com
Date: 2024-04-02 14:52:56
LastEditors: wds-dxh wdsnpshy@163.com
LastEditTime: 2024-04-10 12:14:17
FilePath: /Chinese_massage/mp_image.py
Description: 
微信: 15310638214 
邮箱：wdsnpshy@163.com 
Copyright (c) 2024 by ${wds-dxh}, All Rights Reserved. 
'''
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from draw_wds import draw_landmarks_on_image

class get_landmarks():
    #初始化，输入模型路径
    def __init__(self, model_path = './pose_landmarker_heavy.task'):
        # self.model_path = './pose_landmarker_heavy.task'
        self.model_path = model_path
        self.BaseOptions = mp.tasks.BaseOptions
        self.PoseLandmarker = mp.tasks.vision.PoseLandmarker
        self.PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.options = self.PoseLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path=self.model_path),
            running_mode=self.VisionRunningMode.IMAGE)
        self.landmarker = self.PoseLandmarker.create_from_options(self.options)

    def get_result_landmarks(self, image):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        result = self.landmarker.detect(mp_image)
        return result
    
    def get_result_image(self, image):
        annotated_image = draw_landmarks_on_image(image, self.get_result_landmarks(image))
        return annotated_image



#测试是否能够正常运行
if __name__ == '__main__':
    get_landmarks = get_landmarks()
    import cv2
    
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    while cap.isOpened():
        star_time = time.time()
        success, image = cap.read()
        annotated_image = get_landmarks.get_result_image(image)
        fps = 1 / (time.time() - star_time)
        cv2.putText(annotated_image, f'FPS: {int(fps)}', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow("Annotated Image", annotated_image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()




    