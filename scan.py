import cv2
import torch
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)  # note: 0 is default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    detected = [model.model.names[int(cls)] for cls in results.boxes.cls]

    if 'cell phone' in detected or 'camera' in detected:
        print("Phone or camera detected.")
    else:
        print("No phone or camera detected.")

    # draw boxes
    results.render()  # adds boxes to frame
    cv2.imshow("Detection", results.ims[0])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
