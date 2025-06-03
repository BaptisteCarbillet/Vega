import paho.mqtt.client as mqtt #import library
import os
import time
import threading
import subprocess
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_PATH = os.path.join(SCRIPT_DIR, '../robomaster_sdk_can/')

print(BIN_PATH)
MQTT_SERVER = "argus.paris.inria.fr" #specify the broker address
MQTT_PATH = "mqtt/control" #this is the name of topic
speed = 30
angle = 75 # defautl angle move for the gimbal, 7.5 degrees
def heartbeat_loop():
    
    subprocess.Popen([BIN_PATH + './send_heartbeat'],shell=True)
        

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_PATH)
    os.system(BIN_PATH + './center_gimbal')

 

def on_message(client, userdata, msg):
    global speed
    print(msg.topic+" "+str(msg.payload))
    command = msg.payload.decode('utf-8')
    if command == 'STOP':
        subprocess.Popen([BIN_PATH + './stop_wheel'],shell=True)
    elif command == 'FORWARD':
        subprocess.Popen([BIN_PATH + './mv_wheel {} {} {} {}'.format(speed,speed,speed,speed)],shell=True)
    elif command == 'BACKWARD':
        subprocess.Popen([BIN_PATH + './mv_wheel -{} -{} -{} -{}'.format(speed,speed,speed,speed)],shell=True)
    elif command == 'RIGHT':
        subprocess.Popen([BIN_PATH + './mv_wheel -{} {} -{} {}'.format(speed,speed,speed,speed)],shell=True)
    elif command == 'LEFT':
        subprocess.Popen([BIN_PATH + './mv_wheel {} -{} {} -{}'.format(speed,speed,speed,speed)],shell=True)
    elif command == 'ROTATION_RIGHT':
        subprocess.Popen([BIN_PATH + './mv_wheel -{} {} {} -{}'.format(speed,speed,speed,speed)],shell=True)
    elif command == 'ROTATION_LEFT':
        subprocess.Popen([BIN_PATH + './mv_wheel {} -{} -{} {}'.format(speed,speed,speed,speed)],shell=True)
    elif command == 'INCREASE_SPEED':
        speed += 10
        
    elif command == 'DECREASE_SPEED':
        speed -= 10
    elif command == 'RIGHT_GIMBAL':
        subprocess.Popen([BIN_PATH + './mv_gimbal {} 0'.format(angle)],shell=True)
    elif command == 'LEFT_GIMBAL':
        subprocess.Popen([BIN_PATH + './mv_gimbal -{} 0'.format(angle)],shell=True)
    elif command == 'UP_GIMBAL':
        subprocess.Popen([BIN_PATH + './mv_gimbal 0 {}'.format(angle)],shell=True)
    elif command == 'DOWN_GIMBAL':
        subprocess.Popen([BIN_PATH + './mv_gimbal 0 -{}'.format(angle)],shell=True)
    elif command == 'CENTER_GIMBAL':
        subprocess.Popen([BIN_PATH + './center_gimbal'],shell=True)
    else:
        pass

 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)

heartbeat_thread = threading.Thread(target=heartbeat_loop,daemon=True)
heartbeat_thread.start()


client.loop_forever()