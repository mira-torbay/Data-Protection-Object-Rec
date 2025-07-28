import cv2
from ultralytics import YOLO


def scan(camera):
    model = YOLO("yolov8n.pt")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # camera is already opened and managed by the caller
    while True:
        ret, frame = camera.read()
        if not ret:
            return False

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) == 0:
            print("NO FACE DETECTED - Camera may be covered")
            return False

        results = model(frame)[0]
        detected = [model.model.names[int(cls)] for cls in results.boxes.cls]

        if 'cell phone' in detected or 'camera' in detected:
            print("PHONE OR CAMERA DETECTED")
            return False

        # draw boxes
        annotated_frame = results.plot()
        
        # Draw face detection rectangles on the annotated frame
        for (x, y, w, h) in faces:
            cv2.rectangle(annotated_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.imshow("Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # don't release camera here, it's managed by the caller
    cv2.destroyAllWindows()
    return True
