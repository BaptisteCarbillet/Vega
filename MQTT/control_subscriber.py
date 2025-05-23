import paho.mqtt.client as mqtt #import library
import os

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
        os.system('../robomaster_sdk_can/./stop_wheel')
    elif command == 'FORWARD':
        
        os.system('../robomaster_sdk_can/./mv_wheel 30 30 30 30')

 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)
client.loop_forever()