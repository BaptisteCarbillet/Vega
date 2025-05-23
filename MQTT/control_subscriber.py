import paho.mqtt.client as mqtt #import library
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_PATH = os.path.join(SCRIPT_DIR, '../robomaster_sdk_can/')


MQTT_SERVER = "argus.paris.inria.fr" #specify the broker address
MQTT_PATH = "mqtt/control" #this is the name of topic

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_PATH)
 

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    command = msg.payload.decode('utf-8')
    if command == 'STOP':
        os.system(BIN_PATH + './stop_wheel')
    elif command == 'FORWARD':
        os.system(BIN_PATH + './mv_wheel 30 30 30 30')
    elif command == 'BACKWARD':
        os.system(BIN_PATH + './mv_wheel -30 -30 -30 -30')
    elif command == 'RIGHT':
        os.system(BIN_PATH + './mv_wheel -30 30 -30 30')
    elif command == 'LEFT':
        os.system(BIN_PATH + './mv_wheel 30 -30 30 -30')
    elif command == 'ROTATION_RIGHT':
        os.system(BIN_PATH + './mv_wheel -30 30 30 -30')
    elif command == 'ROTATION_LEFT':
        os.system(BIN_PATH + './mv_wheel 30 -30 -30 30')
    else:
        
        pass

 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)
client.loop_forever()