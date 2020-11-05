import numpy as np
import cv2

# open the camera
cap = cv2.VideoCapture(0)

while True:
    #read the image from the camera
    ret, frame = cap.read()

    #You will need this later
    #frame = cv2.cvtColor(frame, ENTER_CORRECT_CONSTANT_HERE)

    # colour detection limits
    lB = 125
    lG = 125
    lR = 125
    hB = 255
    hG = 255
    hR = 255
    lowerLimits = np.array([lB, lG, lR])
    upperLimits = np.array([hB, hG, hR])

    # Our operations on the frame come here
    thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
    outimage = cv2.bitwise_and(frame, frame, mask = thresholded)

    cv2.imshow('Original', frame)

    # Display the resulting frame
    cv2.imshow('Processed', outimage)

    # Quit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
print 'closing program'
cap.release()
cv2.destroyAllWindows()

