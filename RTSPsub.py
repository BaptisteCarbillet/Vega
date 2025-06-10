import cv2


pi_ip_addr = "128.93.82.122"
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