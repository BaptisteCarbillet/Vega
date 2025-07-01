import cv2
import numpy as np
import subprocess
import os 
import time
import subprocess
from robomaster_sdk_can import Robot
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_PATH = os.path.join(SCRIPT_DIR, '../robomaster_sdk_can/')

#print(BIN_PATH)
class FrameProcessor:

    def __init__(self, frame):
        self.frame = frame
        self.reduced_frame = frame[300:, ::]  # Crop the image to reduce processing
        
    def process_frame(self):

        self.reduced_frame = cv2.cvtColor(self.reduced_frame, cv2.COLOR_BGR2GRAY)
        _, self.reduced_frame = cv2.threshold(self.reduced_frame, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        self.contours, _ = cv2.findContours(self.reduced_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    
    def compute_centroid(self):
        #Check that there is a contour
        if self.contours:
            for contour in self.contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    return cX, cY
                else:
                    print("Zero area contour, skipping.")
        else:
            
            return None, None


class PIDcontroller:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, setpoint=0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.previous_error = 0.0
        self.integral = 0.0
        self.cap = cv2.VideoCapture(0)
    

    def get_measurement(self):
        t0 = time.time()
        
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (640, 480))

        self.frame = FrameProcessor(frame)
        
        self.frame.process_frame()
        self.measurement = self.frame.compute_centroid()[0]
        print(f"Frame processed in {time.time() - t0:.2f} seconds")

    def compute(self):
        error = self.setpoint - self.measurement
        self.integral += error
        derivative = error - self.previous_error
        
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.previous_error = error
        print('output:', output)
        return output
    
robot = Robot()   
controller = PIDcontroller(kp=0.05, ki=0, kd=0.0, setpoint=320)
while True:
    controller.get_measurement()
    controller.compute()
    robot.move_robot(0,output,0,1)
    