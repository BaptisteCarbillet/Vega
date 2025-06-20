import paho.mqtt.client as mqtt

MQTT_SERVER = "argus.paris.inria.fr"  # specify the broker address
MQTT_PATH = "mqtt/latency"  # this is the name of topic
client_send_ack = mqtt.Client()

# subscribe only when connected
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", str(rc))
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    client_send_ack.publish(MQTT_PATH + "_ack", msg.payload)

client_send_ack.on_connect = on_connect
client_send_ack.on_message = on_message
client_send_ack.connect(MQTT_SERVER)
client_send_ack.loop_forever()
