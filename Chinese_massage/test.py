from ultralytics import YOLO
import cv2


# Load a pretrained YOLOv8n-cls Clasify model
model = YOLO('./models/yolov8m-pose.pt')

fram = cv2.imread('test.png')
fram = cv2.resize(fram, (640, 640), interpolation=cv2.INTER_LINEAR)
cv2.imshow('fram', fram)
cv2.waitKey(0)
# Run inference on an image
results = model(fram)  # results list

# View results
for r in results:
    list_xy = r.keypoints.xy.tolist()  # convert the Keypoints object to a list
    list_xy = list_xy[0]
    print(list_xy)
    
