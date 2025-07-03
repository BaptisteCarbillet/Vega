import os 
import threading
import signal
import subprocess
import time
import paho.mqtt.client as mqtt
import cv2
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_PATH = os.path.join(SCRIPT_DIR, '../robomaster_sdk_can/')



class Robot:
    def __init__(self,publish = False):
        
        if publish:
            self.client = mqtt.Client()
            self.client.connect('argus.paris.inria.fr')
            self.topic = 'camera'
        self.chassis_process = None

    def stop_chassis_process(self):

        if self.chassis_process and self.chassis_process.poll() is None:
            self.chassis_process.kill()
            print("Chassis process stopped.")

        else:
            pass
            

    def heartbeat_loop(self):

        subprocess.Popen([BIN_PATH + './send_heartbeat'], shell=True)

    def start_heartbeat(self):
        heartbeat_thread = threading.Thread(target=self.heartbeat_loop)
        heartbeat_thread.daemon = True  
        heartbeat_thread.start()
    

    def stop_robot(self):
        self.stop_chassis_process()
        subprocess.Popen([BIN_PATH +  './stop_wheel'], shell=True)

    def center_gimbal(self):
        subprocess.Popen(["exec " + BIN_PATH +  './center_gimbal'], shell=True)

    def move_wheel(self, fr_rpm, fl_rpm, br_rpm, bl_rpm):
        self.stop_chassis_process()
        self.chassis_process = subprocess.Popen(["exec " + BIN_PATH +  f'./mv_wheel {fr_rpm} {fl_rpm} {br_rpm} {bl_rpm}'], shell=True)


    def move_gimbal(self, yaw, pitch):
        subprocess.Popen([BIN_PATH +  f'./mv_gimbal {yaw} {pitch}'], shell=True)

    def move_robot(self, vx, vy, omega,timeout=5):
        self.stop_chassis_process()
        self.chassis_process = subprocess.Popen(["exec " + BIN_PATH +  f'./mv_robot {vx} {vy} {omega} {timeout}'], shell=True)
    
    

    def publish(self,frame):
        if self.client:
            ret,buffer = cv2.imencode('.jpg', frame)
            self.client.publish(self.topic, buffer.tobytes())
        else:
            print("MQTT client not initialized. Cannot publish frame.")
