import paho.mqtt.client as mqtt
import time
import numpy as np
from collections import deque

MQTT_SERVER = "argus.paris.inria.fr"  # specify the broker address
TOPIC = "mqtt/latency"  # this is the name of topic
TOPIC_ACK = TOPIC + "_ack"  # acknowledgment topic
client = mqtt.Client()
client.connect(MQTT_SERVER)
client.subscribe(TOPIC_ACK)

current_time = time.time()
latency_list = []
msg_count = 0

def on_message(client, userdata, msg):
    global current_time
    global latency_list
    global msg_count
    global time_sent
    
        
    latency = time.time() - time_sent  # Calculate latency
    assert msg.payload.decode('utf-8') == random_payload, "Payload mismatch"
    latency_list.append(latency)
    msg_count += 1
    
    if msg_count < 10000:
        random_payload = str(random.randint(0, 10000)) #Generate a random payload
        current_time = time.time()  # Update the current time for the next message
        time_sent = time.time()  # Record the time when the message is sent
        client.publish(MQTT_PATH, random_payload) # Publish a message with the random payload
    else:
        print("Received 10000 messages, stopping...")
        client_ack.loop_stop()

client.on_message = on_message

# wait for subscription to be ready before sending first message
time.sleep(1)

time_sent = time.time()  # Record the time when the first message is sent
client.publish(MQTT_PATH, '')  # Initial message to start the loop
#to be able to echo 100000 messages

print('length of latency_list:', len(latency_list))
if(latency_list):
    print("Average latency :  {} seconds".format(np.mean(latency_list)))
else:
    print("No messages received. Check connection or topic.")
