import numpy as np
import cv2
import time

# open the camera
cap = cv2.VideoCapture(0)
framerate=0

LB_trac_value = 0
LB_old_value = 0
LG_trac_value = 25
LG_old_value = 0
LR_trac_value = 80
LR_old_value= 0
HB_trac_value= 200
HB_old_value = 0
HG_trac_value= 70
HG_old_value= 0
HR_trac_value = 255
HR_old_value = 0

blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByCircularity = False
blobparams.filterByArea = True
blobparams.minArea =100 #10
blobparams.maxArea =100000
#blobparams.filterByColor= True
#blobparams.blobColor=255
blobparams.minDistBetweenBlobs = 200
##blobparams.filterByConvexity = False
##blobparams.maxConvexity = 3000

detector = cv2.SimpleBlobDetector_create(blobparams)


def LB_updateValue(new_value):
    global LB_trac_value
    LB_trac_value = new_value
    return
def LG_updateValue(new_value):
    global LG_trac_value
    LG_trac_value = new_value
    return
def LR_updateValue(new_value):
    global LR_trac_value
    LR_trac_value = new_value
    return
def HB_updateValue(new_value):
    global HB_trac_value
    HB_trac_value= new_value
    return
def HG_updateValue(new_value):
    global HG_trac_value
    HG_trac_value= new_value
    return
def HR_updateValue(new_value):
    global HR_trac_value
    HR_trac_value = new_value
    return

cv2.namedWindow("Processed")
cv2.createTrackbar("Low Blue trackbar", "Processed", LB_trac_value, 255, LB_updateValue)
cv2.createTrackbar("Low Green trackbar", "Processed", LG_trac_value, 255, LG_updateValue)
cv2.createTrackbar("Low Red trackbar", "Processed", LR_trac_value, 255, LR_updateValue)
cv2.createTrackbar("High Blue trackbar", "Processed", HB_trac_value, 255, HB_updateValue)
cv2.createTrackbar("High Green trackbar", "Processed", HG_trac_value, 255, HG_updateValue)
cv2.createTrackbar("High Red trackbar", "Processed", HR_trac_value, 255, HR_updateValue)
cv2.SimpleBlobDetector_create()
while True:
    #read the image from the camera
    ret, frame = cap.read()
    timeold=time.time()
    #You will need this later
    #frame = cv2.cvtColor(frame, ENTER_CORRECT_CONSTANT_HERE)
# colour detection limits
    lB = LB_trac_value
    lG = LG_trac_value
    lR = LR_trac_value
    hB = HB_trac_value
    hG = HG_trac_value
    hR = HR_trac_value
    lowerLimits = np.array([lB, lG, lR])
    upperLimits = np.array([hB, hG, hR])

    # Our operations on the frame come here
    thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
    thresholded = cv2.bitwise_not(thresholded)

    keypoints = detector.detect(thresholded)
    #to show the detected keypoints on the screen
    thresh = cv2.drawKeypoints(frame, keypoints, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    outimage = cv2.bitwise_and(frame, frame, mask = thresholded)
    
    if len(keypoints)!=0: 
        print(keypoints[0].size)#Displays size of one object
    for keypoint in keypoints:
            thresh = cv2.resize(thresh, (0,0), fx=2, fy=2)
            cv2.putText(thresh, "X("+str(int(keypoint.pt[0]))+")"+"Y("+str(int(keypoint.pt[1]))+")", (2*(int(keypoint.pt[0])), (2*int(keypoint.pt[1]))), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            thresh = cv2.resize(thresh, (0,0), fx=0.5, fy=0.5)
    # Display the resulting frame
    cv2.imshow('Processed', outimage)
    cv2.imshow('Thresholded', thresholded)

    # Quit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    timenew=time.time()
    
    framerate=1/(timenew-timeold)
    framerate=int(framerate)
    framerate=str(framerate)
    cv2.putText(thresh, framerate, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Original', thresh)
    cv2.imshow('Thresholded', thresh)

# When everything done, release the capture
print('closing program')
cap.release()
cv2.destroyAllWindows()