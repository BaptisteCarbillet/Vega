import cv2
import numpy as np



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

    def get_frame(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Could not open video device")
        ret, frame = cap.read()
        cap.release()
        frame = cv2.resize(frame, (640, 480))

        self.frame = FrameProcessor(frame)
        

    def compute(self, measurement):
        error = self.setpoint - measurement
        self.integral += error
        derivative = error - self.previous_error
        
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.previous_error = error
        
        return output