import cv2
import numpy as np
import subprocess
import random
import os 
import time
import math
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from robomaster_sdk_can.robot import Robot
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_PATH = os.path.join(SCRIPT_DIR, '../robomaster_sdk_can/')

#print(BIN_PATH)
class FrameProcessor:

    def __init__(self, frame):
        
        self.frame = frame
        self.reduced_frame = frame[300:, ::]  # Crop the image to reduce processing
        
    def process_frame(self):
        
        
        #This function process the frame : It get reduced, converted to grayscale, thresholded and contours are found.
        


        self.reduced_frame = cv2.cvtColor(self.reduced_frame, cv2.COLOR_BGR2GRAY)
        _, self.reduced_frame = cv2.threshold(self.reduced_frame, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        self.contours, _ = cv2.findContours(self.reduced_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        #erosion and dilation to remove noise
        kernel = np.ones((5, 5), np.uint8)
        self.reduced_frame = cv2.erode(self.reduced_frame, kernel, iterations=5)
        self.reduced_frame = cv2.dilate(self.reduced_frame, kernel, iterations=5)

    def compute_angles(self):

        ### This function compute the angle between the line and the vertical axis for control
        #Check that there is a contour
        if self.contours:
            epsilon = 0.02 * cv2.arcLength(self.contours[0], True)
            approx = cv2.approxPolyDP(self.contours[0], epsilon, True)
            if len(approx) != 4:
                print("Contour does not have 4 corners, cannot compute angle.")
                self.angle = None
                return self.angle

            # 2. Pull out the 4 corners
            #    (approx is shape (4,1,2); we reshape to (4,2))
            pts = approx.reshape(4, 2)

            lower_points = pts[pts[:, 1].argsort()[2:]]  # 2 lowest points
            upper_points = pts[pts[:, 1].argsort()[:2]]  # 2 highest points

            lower_left = lower_points[lower_points[:, 0].argmin()]  # leftmost of the lower points
            lower_right = lower_points[lower_points[:, 0].argmax()]  # rightmost of the lower points
            upper_left = upper_points[upper_points[:, 0].argmin()]  # leftmost of the upper points
            upper_right = upper_points[upper_points[:, 0].argmax()]  # rightmost of the upper points

            dx_left,dy_left = -upper_left + lower_left
            dx_right,dy_right = -upper_right + lower_right

            angle_rad_left = math.atan2(dy_left, -dx_left)
            angle_deg_left = math.degrees(angle_rad_left) -90

            angle_rad_right = math.atan2(dy_right, -dx_right)
            angle_deg_right = math.degrees(angle_rad_right) -90

            angle_deg = (angle_deg_left + angle_deg_right) / 2

            self.angle = angle_deg
            return self.angle
        else:
            print("No contours found.")
            return None


    
    def compute_centroid(self):

        ### This find the center of mass of the contour of the line

        #Check that there is a contour
        if self.contours:
            
            #find largest contour
            self.contours = sorted(self.contours, key=cv2.contourArea, reverse=True)
            for contour in self.contours:
                
                M = cv2.moments(contour)
                
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    self.cX = cX
                    self.cY = cY
                    return cX, cY
                else:
                    print("Zero area contour, skipping.")
        else:
            
            return None, None


class PIDcontroller:
    def __init__(self, kp_y=1.0, ki_y=0.0, kd_y=0.0, kp_omega = 0.0,ki_omega = 0.0,kd_omega = 0.0,setpoint_angular=0.0,setpoint_horizontal=320):
        self.kp_y = kp_y
        self.ki_y = ki_y
        self.kd_y = kd_y

        self.kp_omega = kp_omega
        self.ki_omega = ki_omega
        self.kd_omega = kd_omega

        self.setpoint_angular = setpoint_angular
        self.setpoint_horizontal = setpoint_horizontal
        
        self.previous_error_y = 0.0
        self.integral_y = 0.0

        self.previous_error_omega = 0.0
        self.integral_omega = 0.0
        
        self.cap = cv2.VideoCapture(0,cv2.CAP_V4L2)

        self.measurement_y = None
        self.measurement_omega = None

    def get_and_process_frame(self):
        t0 = time.time()
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (640, 480))
        
        self.frame = FrameProcessor(frame)
        
        self.frame.process_frame()
        

    def get_measurement_horizontal(self):
        
        self.measurement_y = self.frame.compute_centroid()[0]
        
        
        if self.measurement_y is not None:
            cX, cY = self.frame.cX, self.frame.cY
            cv2.circle(self.frame.reduced_frame, (cX, cY), 5, (0, 255, 0), -1)
            
    def get_measurement_angular(self):
        
        if self.frame.contours:
            self.measurement_omega = self.frame.compute_angles()
            
            
        
            
    def compute(self):
        error_y = -self.setpoint_horizontal + self.measurement_y
        self.integral_y += error_y
        derivative_y = error_y - self.previous_error_y
        
        output_y = (self.kp_y * error_y) + (self.ki_y * self.integral_y) + (self.kd_y * derivative_y)
        
        self.previous_error_y = error_y
        print(f"Error: {error_y}, Output: {output_y}")

        # Compute angular control
        if self.measurement_omega is None:
            print("No angle measurement available, skipping angular control.")
            return output_y, 0.0
        error_omega =  -self.measurement_omega + self.setpoint_angular
        self.integral_omega += error_omega
        derivative_omega = error_omega - self.previous_error_omega
        
        output_omega = (self.kp_omega * error_omega) + (self.ki_omega * self.integral_omega) + (self.kd_omega * derivative_omega)
        print(f"Angular Error: {error_omega}, Angular Output: {output_omega}")
        return output_y, output_omega
    
robot = Robot(publish=True)   

robot.center_gimbal()
#Ku : 0.00115
#Tu : 0.372
controller = PIDcontroller(kp_y=0.0006, ki_y=0.000, kd_y=0, kp_omega=2, ki_omega=0, kd_omega=0, setpoint_angular=0.0, setpoint_horizontal=320)


while True:
    t0 = time.time()
    controller.get_and_process_frame()
    controller.get_measurement_horizontal()
    controller.get_measurement_angular()
    print(f"Frame acquisition and processing took {time.time() - t0:.3f} seconds")
    robot.publish(controller.frame.reduced_frame)
    output_y,output_omega = controller.compute()
    
    robot.move_robot(0.1,output_y,0 if output_omega is None else output_omega,3)
    

