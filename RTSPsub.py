import cv2
import paho.mqtt.client as mqtt
import os




broker = 'argus.paris.inria.fr'
ip_receiver = mqtt.Client()
ip_receiver.connect(broker)

def on_message(client, userdata, msg):
    global pi_ip_addr
    if msg.topic == "mqtt/ip_addr":
        pi_ip_addr = msg.payload.decode()
        print(f"Received IP address: {pi_ip_addr}")
        client.disconnect()

 # Function to get the Raspberry Pi IP address

ip_receiver.on_message = on_message
ip_receiver.subscribe("mqtt/ip_addr")
ip_receiver.loop_start()
# Wait for the IP address to be received
while 'pi_ip_addr' not in globals():
    pass
# Stop the loop once the IP address is received
ip_receiver.loop_stop()

#Send acknowledgment
ack_client = mqtt.Client()
ack_client.connect(broker)
ack_client.publish("mqtt/ip_addr_ack", "IP address received", qos=1)
ack_client.disconnect()

rtsp_url = "rtsp://{}:8554/stream".format(pi_ip_addr)

cap = cv2.VideoCapture(rtsp_url)
i = 0
# Set buffer size to reduce latency
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    cv2.imshow('RTSP Stream', frame)
    key = cv2.waitKey(1) & 0xFF
    # Press 'q' to quit, 'w' to save the frame
    if key == ord('q'):
        break
    elif key == ord('w'):
        # Save the current frame to a file
        
        cv2.imwrite('img/saved_frames/saved_frame{}.jpg'.format(i), frame)
        i+=1
        

cap.release()
cv2.destroyAllWindows()