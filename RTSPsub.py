import cv2


pi_ip_addr = "128.93.82.122"
rtsp_url = "rtsp://{}:8554/stream".format(pi_ip_addr)

cap = cv2.VideoCapture(rtsp_url)

# Set buffer size to reduce latency
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    cv2.imshow('RTSP Stream', frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()