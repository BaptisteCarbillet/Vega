import paho.mqtt.client as mqtt #import library
import os
import time
import threading
import subprocess
from robomaster_sdk_can.robot import Robot

MQTT_SERVER = "argus.paris.inria.fr" #specify the broker address
MQTT_TOPIC = "mqtt/control" #this is the name of topic
speed = 30
angle = 75 # defautl angle move for the gimbal, 7.5 degrees

robot = Robot()

def heartbeat_loop():
    
    subprocess.Popen([BIN_PATH + './send_heartbeat'],shell=True)
        

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)
    robot.center_gimbal()

 

def on_message(client, userdata, msg):
    global speed
    print(msg.topic+" "+str(msg.payload))
    command = msg.payload.decode('utf-8')
    if command == 'STOP':
        robot.stop_robot()
    
    elif command == 'FORWARD':
        robot.move_wheel(speed, speed, speed, speed)
    
    elif command == 'BACKWARD':
        robot.move_wheel(-speed, -speed, -speed, -speed)
        
    elif command == 'RIGHT':
        robot.move_wheel(-speed, speed, -speed, speed)
        
    elif command == 'LEFT':
        robot.move_wheel(speed, -speed, speed, -speed)
    
    elif command == 'ROTATION_RIGHT':
        robot.move_wheel(-speed, speed, speed, -speed)
        
    elif command == 'ROTATION_LEFT':
        robot.move_wheel(speed, -speed, -speed, speed)
    
    elif command == 'INCREASE_SPEED':
        speed += 10
        
    elif command == 'DECREASE_SPEED':
        speed -= 10
    
    elif command == 'RIGHT_GIMBAL':
        robot.move_gimbal(angle, 0)
    
    elif command == 'LEFT_GIMBAL':
        robot.move_gimbal(-angle, 0)
    
    elif command == 'UP_GIMBAL':
        robot.move_gimbal(0, angle)
    
    elif command == 'DOWN_GIMBAL':
        robot.move_gimbal(0, -angle)

    elif command == 'CENTER_GIMBAL':
        robot.center_gimbal()
    
    else:
        pass

 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)

#heartbeat_thread = threading.Thread(target=heartbeat_loop,daemon=True)
#heartbeat_thread.start()


client.loop_forever()