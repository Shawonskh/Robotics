import cv2
import time

# Open the camera
cap = cv2.VideoCapture(0)

framerate=0

while True:
    timeold=time.time()   
    ret, frame =cap.read() # Read the image from the camera   
# Write some text onto the frame
    cv2.putText(frame, str(framerate), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
##  cv2.putText(frame, "Hello", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Show this image on a window named "Original"
    cv2.imshow('Original', frame)
        # Quit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    timenew=time.time()
    
    framerate=1/(timenew-timeold)
    framerate=int(framerate)
    print(framerate)
# When everything done, release the capture
print('closing program')
cap.release()
cv2.destroyAllWindows()