import cv2
from ultralytics import YOLO

class Yolo_opencv:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO("yolov8n.pt")
        self.roi1 = [480, 145, 560, 225]
        self.roi2 = [390, 145, 470, 225]
        self.roi3 = [300, 145, 370, 225]
    
    def is_within_roi(self,bbox,roi): 
        x1, y1, x2, y2 = bbox
        rx1, ry1, rx2, ry2 = roi
        return x1 >= rx1 and y1 >= ry1 and x2 <= rx2 and y2 <= ry2
    
    def frame_yolo(self):
        while True:
            self.ret, self.frame = self.cap.read()
            if not self.ret:
                print("Error: Could not read frame.")
                break

            self.results = self.model(self.frame, conf=0.5) # Assuming your model returns results in this format

            for result in self.results:
                boxes = result.boxes # Boxes object
 
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0]) # Extract coordinates as integers
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    label = f'{self.model.names[cls]} {conf:.2f}'
                    bbox = [x1, y1, x2, y2] # Define bbox as a list of coordinates
                    if self.is_within_roi(bbox, self.roi1):
                        color = (255, 0, 0)
                        if cls == 0:
                            self.motion_grab_capsule_A()
                            self.motion_check_sealing()
                            if cls == 1:
                                pass
                            elif cls == 2:
                                self.motion_place_capsule()
                                self.motion_grab_cup()
                        elif cls == 3:
                            self.motion_grab_capsule_A()
                            self.motion_trash_capsule()

                    elif self.is_within_roi(bbox, self.roi2):
                        color = (0, 255, 0)
                        if cls == 0:
                            self.motion_grab_capsule_B()
                            self.motion_check_sealing()
                            if cls == 1:
                                pass
                            elif cls == 2:
                                self.motion_place_capsule()
                                self.motion_grab_cup()
                        elif cls == 3:
                            self.motion_grab_capsule_B()
                            self.motion_trash_capsule()

                    elif self.is_within_roi(bbox, self.roi3):
                        color = (0, 0, 255)
                        if cls == 0:
                            self.motion_grab_capsule_c()
                            self.motion_check_sealing()
                            if cls == 1:
                                pass
                            elif cls == 2:
                                self.motion_place_capsule()
                                self.motion_grab_cup()
                        elif cls == 3:
                            self.motion_grab_capsule_c()
                            self.motion_trash_capsule()
                    else:
                        color = (255, 255, 255) # Default color for boxes not in any ROI

                    cv2.rectangle(self.frame, (self.roi1[0], self.roi1[1]), (self.roi1[2], self.roi1[3]), (0, 255, 0), 2)
                    cv2.rectangle(self.frame, (self.roi2[0], self.roi2[1]), (self.roi2[2], self.roi2[3]), (200, 200, 0), 2)
                    cv2.rectangle(self.frame, (self.roi3[0], self.roi3[1]), (self.roi3[2], self.roi3[3]), (10, 100, 0), 2)
                    cv2.rectangle(self.frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(self.frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            cv2.imshow("test", self.frame)
 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ =="__main__":
    yolo=Yolo_opencv()
    yolo.frame_yolo()