import cv2
from ultralytics import YOLO


def scan():
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(0)  # note: 0 is default webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            return False

        results = model(frame)[0]
        detected = [model.model.names[int(cls)] for cls in results.boxes.cls]

        if 'cell phone' in detected or 'camera' in detected:
            print("PHONE OR CAMERA DETECTED")
            return False

        # draw boxes
        annotated_frame = results.plot()
        cv2.imshow("Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return True
