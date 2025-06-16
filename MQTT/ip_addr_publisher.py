import paho.mqtt.client as mqtt
import os
broker = 'argus.paris.inria.fr'

def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print('IP adress not published yet, retrying...')
        pass
        


unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish

mqttc.user_data_set(unacked_publish)

mqttc.connect(broker)
mqttc.loop_start()

ip_addr = os.popen("hostname -I | awk '{print $1}'").read().strip()

received = False

ack_client = mqtt.Client()
def on_message(client, userdata, msg):
    global received
    if msg.topic == "mqtt/ip_addr_ack":
        print(f"Received acknowledgment for IP address: {msg.payload.decode()}")
        received = True
ack_client.on_message = on_message
ack_client.connect(broker)
ack_client.subscribe("mqtt/ip_addr_ack")
ack_client.loop_start()



while not received:
    try:
        
        mqttc.publish("mqtt/ip_addr",  ip_addr, qos=1)
        
    except Exception as e:
        print(f"Error publishing IP address: {e}")
        break

ack_client.disconnect()
mqttc.disconnect()


