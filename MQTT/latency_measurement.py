import paho.mqtt.client as mqtt
import time
from collections import deque

MQTT_SERVER = "argus.paris.inria.fr"  # specify the broker address
MQTT_PATH = "mqtt/latency"  # this is the name of topic

client_pub = mqtt.Client()
client_ack = mqtt.Client()
client_pub.connect(MQTT_SERVER + "_ping")
client_ack.connect(MQTT_SERVER + "_pong")

timestamp_queue = deque(maxlen=10000)  
latency_list = []
def on_message_ack(client, userdata, msg):
    received_time = time.time()
    latency = received_time - timestamp_queue.pop()
    latency_list.append(latency)



client_ack.on_message = on_message_ack
client_ack.subscribe(MQTT_PATH + "_pong")
client_ack.loop_forever()

sent_msg = 0
while True:
    timestamp = time.time()
    timestamp_queue.append(timestamp)
    client_pub.publish(MQTT_PATH + "_ping", timestamp)
    time.sleep(0.1)  # Adjust the sleep time as needed for your application
    sent_msg += 1
    if sent_msg == 10000:
        print("Average latency over last 10000 messages: ", sum(latency_list) / len(latency_list))
        sent_msg = 0
        latency_list.clear()
