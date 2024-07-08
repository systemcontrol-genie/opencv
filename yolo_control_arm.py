import threading
import cv2
from ultralytics import YOLO
import time
from xarm.wrapper import XArmAPI
from xarm import version

class RobotMain:
    def __init__(self, arm):
        self.arm = arm
        self.cap = cv2.VideoCapture(0)
        self.model = self.load_model()
        self.roi1 = (50, 50, 300, 300)  # Example ROI coordinates
        self.roi2 = (350, 50, 600, 300)
        self.roi3 = (650, 50, 900, 300)
        self.ret = None
        self.frame = None
        self.results = None

    def load_model(self):
        # Load your model here
        model = YOLO("best.pt")
        pass

    def is_within_roi(self, bbox, roi):
        x1, y1, x2, y2 = bbox
        rx1, ry1, rx2, ry2 = roi
        return x1 >= rx1 and y1 >= ry1 and x2 <= rx2 and y2 <= ry2

    def motion_grab_capsule_A(self):
        code = self._arm.set_cgpio_analog(0, 5)
        if not self._check_code(code, 'set_cgpio_analog'):
            return
        code = self._arm.set_cgpio_analog(1, 5)
        if not self._check_code(code, 'set_cgpio_analog'):
            return
        self._angle_speed = 100
        self._angle_acc = 100

        self._tcp_speed = 100
        self._tcp_acc = 1000
        code = self._arm.set_servo_angle(angle=[179.5, 33.5, 32.7, 113.0, 93.1, -2.3], speed=self._angle_speed,
        mvacc=self._angle_acc, wait=False, radius=20.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        code = self._arm.set_position(*self.position_jig_A_grab, speed=self._tcp_speed,
        mvacc=self._tcp_acc, radius=0.0, wait=True)
        code = self._arm.open_lite6_gripper()
        if not self._check_code(code, 'open_lite6_gripper'):
            return
        code = self._arm.close_lite6_gripper()
        if not self._check_code(code, 'close_lite6_gripper'):
            return
        time.sleep(2)
        code = self._arm.stop_lite6_gripper()
        if not self._check_code(code, 'stop_lite6_gripper'):
            return

    def motion_grab_capsule_B(self):
        code = self._arm.set_position(*self.position_jig_B_grab, speed=self._tcp_speed,
        mvacc=self._tcp_acc, radius=0.0, wait=True)
        code = self._arm.close_lite6_gripper()
        if not self._check_code(code, 'close_lite6_gripper'):
            return
        time.sleep(2)
        code = self._arm.stop_lite6_gripper()
        if not self._check_code(code, 'stop_lite6_gripper'):
            return
        
    def motion_grab_capsule_c(self):
        code = self._arm.set_servo_angle(angle=[182.6, 27.8, 27.7, 55.7, 90.4, -6.4], speed=self._angle_speed,
        mvacc=self._angle_acc, wait=False, radius=20.0)
        if not self._check_code(code, 'set_servo_angle'):
            return
        # code = self._arm.set_position(*[-76.6, -144.6, 194.3, 5.7, 88.9, -50.1], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
        # if not self._check_code(code, 'set_position'):
        # return
        code = self._arm.set_position(*self.position_jig_C_grab, speed=self._tcp_speed,
        mvacc=self._tcp_acc, radius=0.0, wait=True)
        code = self._arm.close_lite6_gripper()
        if not self._check_code(code, 'close_lite6_gripper'):
            return
        time.sleep(2)
        code = self._arm.stop_lite6_gripper()
        if not self._check_code(code, 'stop_lite6_gripper'):
            return
    def motion_check_sealing(self):
        print('sealing check')
        self._angle_speed = 200
        self._angle_acc = 200
        self.clientSocket.send('motion_sheck_sealing'.encode('utf-8'))
        code = self._arm.set_position(*self.position_sealing_check, speed=self._tcp_speed,
        mvacc=self._tcp_acc, radius=0.0, wait=True)
        if not self._check_code(code, 'set_position'):
            return

    def run(self):
        try:
            while True:
                self.ret, self.frame = self.cap.read()
                if not self.ret:
                    print("Error: Could not read frame.")
                    break

                try:
                    self.results = self.model(self.frame, conf=0.5)  # Assuming your model returns results in this format
                except Exception as e:
                    print(f"Error during model inference: {e}")
                    continue

                for result in self.results:
                    boxes = result.boxes  # Boxes object

                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Extract coordinates as integers
                        conf = box.conf[0]
                        cls = int(box.cls[0])
                        label = f'{self.model.names[cls]} {conf:.2f}'
                        bbox = [x1, y1, x2, y2]  # Define bbox as a list of coordinates

                        color = (255, 255, 255)  # Default color for boxes not in any ROI
                        try:
                            if self.is_within_roi(bbox, self.roi1):
                                color = (255, 0, 0)
                                if cls == 0:
                                    self.motion_grab_capsule_A()
                                    self.motion_check_sealing()
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
                                elif cls == 2:
                                    self.motion_place_capsule()
                                    self.motion_grab_cup()
                                elif cls == 3:
                                    self.motion_grab_capsule_c()
                                    self.motion_trash_capsule()
                        except Exception as e:
                            print(f"Error during robot motion: {e}")

                        cv2.rectangle(self.frame, (self.roi1[0], self.roi1[1]), (self.roi1[2], self.roi1[3]), (0, 255, 0), 2)
                        cv2.rectangle(self.frame, (self.roi2[0], self.roi2[1]), (self.roi2[2], self.roi2[3]), (200, 200, 0), 2)
                        cv2.rectangle(self.frame, (self.roi3[0], self.roi3[1]), (self.roi3[2], self.roi3[3]), (10, 100, 0), 2)
                        cv2.rectangle(self.frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(self.frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                cv2.imshow("test", self.frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            self.cap.release()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    print('xArm-Python-SDK Version:{}'.format(version.__version__))
    arm = XArmAPI('192.168.1.167', baud_checkset=False)
    robot_main = RobotMain(arm)

    socket_thread = threading.Thread(target=robot_main.socket_connect)
    socket_thread.start()

    # Ensure the socket is connected before starting the run thread
    thread = threading.Thread(target=robot_main.run)
    thread.start()
    thread.join()
    socket_thread.join()