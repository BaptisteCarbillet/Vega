import time
import paho.mqtt.client as mqtt
import cv2

broker = 'argus.paris.inria.fr'
topic = 'camera'

client = mqtt.Client()
client.connect(broker)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Encode frame as JPEG
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        continue

    # Convert to bytes and publish
    client.publish(topic, buffer.tobytes())

    time.sleep(1/30)  
cap.release()
client.disconnect()