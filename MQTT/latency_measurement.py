import paho.mqtt.client as mqtt
import time
import numpy as np
from collections import deque

MQTT_SERVER = "argus.paris.inria.fr"  # specify the broker address
MQTT_PATH = "mqtt/latency"  # this is the name of topic

client = mqtt.Client()
client.connect(MQTT_SERVER)
client_ack = mqtt.Client()
client_ack.connect(MQTT_SERVER)
client_ack.subscribe(MQTT_PATH + "_ack")
current_time = time.time()
latency_list = []
msg_count = 0

def on_message(client, userdata, msg):
    global current_time
    global latency_list
    global msg_count
    latency = time.time() - current_time
    latency_list.append(latency)
    msg_count += 1
    print(f"[{msg_count}] Latency: {latency:.6f}s")
    if msg_count < 10000:
        current_time = time.time()  # Update the current time for the next message
        client.publish(MQTT_PATH, '')
    else:
        print("Received 10000 messages, stopping...")
        client_ack.loop_stop()

client_ack.on_message = on_message
client_ack.subscribe(MQTT_PATH + "_ack")
client_ack.loop_start()
# wait for subscription to be ready before sending first message
time.sleep(1)
print("Sending initial message")
current_time = time.time()
client.publish(MQTT_PATH, '')  # Initial message to start the loop
#to be able to echo 100000 messages
while msg_count < 10000:
    time.sleep(0.1)  # Wait for some time to collect messages
print('length of latency_list:', len(latency_list))
if(latency_list):
    print("Average latency :  {} seconds".format(np.mean(latency_list)))
else:
    print("No messages received. Check connection or topic.")