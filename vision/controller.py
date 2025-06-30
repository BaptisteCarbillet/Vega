import cv2
import numpy as np
import subprocess
import os 
import time
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_PATH = os.path.join(SCRIPT_DIR, '../robomaster_sdk_can/')

print(BIN_PATH)
class FrameProcessor:

    def __init__(self, frame):
        self.frame = frame
        self.reduced_frame = frame[300:, ::]  # Crop the image to reduce processing
        self.edges = cv2.Canny(self.reduced_frame, 100, 200)
        self.lines = cv2.HoughLines(self.edges, 1, np.pi / 180, threshold=100)

    
    
    
    def get_angle(self):
        if self.lines is None:
            self.angle = None
        self.angle = self.deviation_from_vertical(self.lines)

    @staticmethod
    
    def deviation_from_vertical(lines):
        angle_deg = lines[:,0,1] * 180 / np.pi  # Convert radians to degrees
        deviation = angle_deg   # since 90° (π/2) is vertical
        # Wrap to [-90, +90]
        deviation = np.where(deviation > 90, deviation - 180, deviation)
        
        return deviation
    



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
        subprocess.Popen([BIN_PATH + './center_gimbal'], shell=True)
        subprocess.Popen([BIN_PATH + './mv_ginmbal -150 0'], shell=True)
        #cap = cv2.VideoCapture(0)
        #if not cap.isOpened():
        #        raise Exception("Could not open video device")
        ret, frame = self.cap.read()
        
        frame = cv2.resize(frame, (640, 480))

        self.frame = FrameProcessor(frame)
        self.measurement = self.frame.get_angle() if self.frame.lines is not None else -1
        t1 = time.time()
        print(f"Frame processing time: {t1 - t0:.4f} seconds")

    def compute(self, measurement):
        error = self.setpoint - measurement
        self.integral += error
        derivative = error - self.previous_error
        
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.previous_error = error
        
        return output
    
    
controller = PIDcontroller(kp=1.0, ki=0.1, kd=0.05, setpoint=0.0)
while True:
    controller.get_measurement()
    