import os 
import threading
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_PATH = os.path.join(SCRIPT_DIR, '../robomaster_sdk_can/')



class Robot:
    def __init__(self):
        self.start_heartbeat()


    def heartbeat_loop(self):

        subprocess.Popen([BIN_PATH + './send_heartbeat'], shell=True)

    def start_heartbeat(self):
        heartbeat_thread = threading.Thread(target=self.heartbeat_loop)
        heartbeat_thread.daemon = True  
        heartbeat_thread.start()
    

    def stop_robot(self):
        subprocess.Popen([BIN_PATH + './stop_wheel'], shell=True)

    def center_gimbal(self):
        subprocess.Popen([BIN_PATH + './center_gimbal'], shell=True)

    def move_wheel(self, fr_rpm, fl_rpm, br_rpm, bl_rpm):
        subprocess.Popen([BIN_PATH + f'./mv_wheel {fr_rpm} {fl_rpm} {br_rpm} {bl_rpm}'], shell=True)


    def move_gimbal(self, yaw, pitch):
        subprocess.Popen([BIN_PATH + f'./mv_gimbal {yaw} {pitch}'], shell=True)

    def move_robot(self, vx, vy, omega):
        subprocess.Popen([BIN_PATH + f'./mv_robot {vx} {vy} {omega}'], shell=True)