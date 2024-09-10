import cv2
from cvzone.FaceDetectionModule import FaceDetector
from PyQt6.QtCore import pyqtSignal, QObject
from threading import Thread


class FaceTracking(QObject):

    sender_pose = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.detector = FaceDetector()
        self.state = 0

    def start_tracking(self):
        self.state = 1
        connection_thread = Thread(target=self.track, daemon=True)
        connection_thread.start()

    def stop_tracking(self):
        self.state = 0



    def track(self):
        cap = cv2.VideoCapture(0)
        while self.state:
            success, img = cap.read()
            img, bboxs = self.detector.findFaces(img, draw=False)

            if bboxs:
                #get the coordinate
                fx, fy = bboxs[0]["center"][0], bboxs[0]["center"][1]
                pos = [fx, fy]


    
    def track(self):
        cap = cv2.VideoCapture(0)
        while self.state:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            img, faces = self.detector.findFaces(frame, draw=False)
            if faces:
                x, y = faces[0]["center"][0], faces[0]["center"][1]
                # Show the camera and a point in the center of the face 
                # cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                # cv2.imshow("Frame", frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
                self.sender_pose.emit(
                    x / 640,
                    y / 480
                )

            else:
                self.sender_pose.emit(0.5, 0.5)
        cap.release()
        cv2.destroyAllWindows()
