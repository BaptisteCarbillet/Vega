import cv2
import numpy as np
import paho.mqtt.client as mqtt
i = 0
def on_message(client, userdata, msg):
    global i
    # Convert payload back to image
    np_arr = np.frombuffer(msg.payload, dtype=np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if frame is not None:
        
        resized_frame = cv2.resize(frame, (640, 480))
        cv2.imshow("MQTT Webcam", resized_frame)
        #save the frame to a file, in a folder named "received_frames"
        
        #cv2.imwrite("img/received_frames/frame{}.jpg".format(i), resized_frame)
        #i += 1
        if cv2.waitKey(1/60) & 0xFF == ord('q'):
            client.disconnect()
            cv2.destroyAllWindows()

broker ='argus.paris.inria.fr'
topic = "camera"
client = mqtt.Client()
client.on_message = on_message
client.connect(broker)
client.subscribe(topic)
client.loop_forever()