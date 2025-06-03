import cv2
import numpy as np
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    # Convert payload back to image
    np_arr = np.frombuffer(msg.payload, dtype=np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if frame is not None:
        cv2.imshow("MQTT Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            client.disconnect()
            cv2.destroyAllWindows()

broker ='argus.paris.inria.fr'
topic = "camera"
client = mqtt.Client()
client.on_message = on_message
client.connect(broker)
client.subscribe(topic)
client.loop_forever()