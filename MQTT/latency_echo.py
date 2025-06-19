import paho.mqtt.client as mqtt
import time
from collections import deque

MQTT_SERVER = "argus.paris.inria.fr"  # specify the broker address
MQTT_PATH = "mqtt/latency"  # this is the name of topic
client_send_ack = mqtt.Client()

client_send_ack.connect(MQTT_SERVER)

def on_message(client, userdata, msg):
    client_send_ack.publish(MQTT_PATH + "_ack", msg.payload)

client_send_ack.on_message = on_message
client_send_ack.subscribe(MQTT_PATH )
client_send_ack.loop_forever()
