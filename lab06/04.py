import numpy as np
import cv2
import time
import gopigo as go

go.stop()

cap = cv2.VideoCapture(0)
start_time = time.time()
counter=0

def updateValue(new_value):
    # make sure to write the new value into the global variable
    global trackbar_value
    global uusvalue
    #tekitame uue globaalse value
    trackbar_value = new_value
    return


lH=9
def lHa(uus):
    global lH
    lH = uus
    return lH
lS=149
def lSa(uus):
    global lS
    lS = uus
    return lS
lV=74
def lVa(uus):
    global lV
    lV = uus
    return lV
hH=17
def hHa(uus):
    global hH
    hH = uus
    return hH
hS=255
def hSa(uus):
    global hS
    hS = uus
    return hS
hV=255
def hVa(uus):
    global lV
    hV = uus
    return hV




trackbar_value = 82

cv2.namedWindow("Processed")


cv2.createTrackbar("HueL", 'Processed', lH, 255, lHa)
cv2.createTrackbar("SaturationL", 'Processed', lS, 255, lSa)
cv2.createTrackbar("ValueL", 'Processed', lV, 255, lVa)
cv2.createTrackbar("HueH", 'Processed', hH, 255, hHa)
cv2.createTrackbar("SaturationH", 'Processed', hS, 255, hSa)
cv2.createTrackbar("ValueH", 'Processed', hV, 255, hVa)


Ret, frame = cap.read()

old = 0 
test = 0
while True:
    
    ret, frame = cap.read()
   
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        
    r=[len(frame)-200, len(frame)-190, 0, len(frame[0])]
    frame =frame[r[0]:r[1], r[2]:r[3]]

    
    lowerLimits = np.array([lH, lS, lV])
    upperLimits = np.array([hH, hS, hV])
    
    thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
    #thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)
    
    
    outimage = cv2.bitwise_and(frame, frame, mask = thresholded)
    
    blobparams = cv2.SimpleBlobDetector_Params()
    
    blobparams.filterByArea = 1
    blobparams.minArea = 70
    blobparams.maxArea = 100000
    blobparams.filterByCircularity = False
    blobparams.minDistBetweenBlobs = 100
    blobparams.filterByConvexity = 0
    blobparams.filterByInertia = 0
    blobparams.filterByColor = 0
    
    detector = cv2.SimpleBlobDetector_create(blobparams)
    
    keypoints = detector.detect(thresholded)
    thresholded = cv2.bitwise_not(thresholded)
    
    
    
   
    
    frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
   
    
    
        
    for keypoint in keypoints:
        cv2.putText(frame, str((round(keypoint.pt[0],2),round(keypoint.pt[1],2))), (int(keypoint.pt[0]),int(keypoint.pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    #print(len(keypoints))
            
    go.set_speed(70)
    #go.stop()
    if len(keypoints) ==  0:
        go.set_speed(70)
        go.right()
        time.sleep(0.05)
        go.stop()
    elif len(keypoints) ==  1:
        go.set_speed(60)
        go.right()
        time.sleep(0.05)
        go.stop()
    
    elif len(keypoints) == 2:
        
        
        
        if int(keypoints[0].pt[0]) > 490 or int(keypoints[0].pt[0]) < 170:
            print("firsttime")
            
            
            if int(keypoints[1].pt[0]) > 490 or int(keypoints[1].pt[0]) < 170:
                
                
                    
                print("right")
                go.set_speed(60)
                #go.left_rot()
                #time.sleep(0.1)
                go.forward()
                time.sleep(2)
                
                    
                
                
        centre = int((keypoints[1].pt[0]+keypoints[0].pt[0])/2)
        test = 0
       
        print(int(keypoints[0].pt[0]))
        print(int(keypoints[1].pt[0]))
        
        if 325 >= centre and centre <=310:
            go.forward()
            time.sleep(0.5)
            go.stop()
            
        elif centre < 310:
            go.left()
            time.sleep(0.05)
            go.stop()
        elif centre > 325:
            go.right()
            time.sleep(0.05)
            go.stop()
        
            
  
     
        
        
            
        
        
        
    new = old
    old = time.time()
    
    
    
    cube = round(1/(old - new))
    
    #counter +=1
    #if (time.time() - start_time) >= 1:
    #cv2.putText(frame, str(aeg), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        #counter = 0
        #start_time = time.time()
    
    
    
    cv2.imshow("Original", frame)
    
    
    cv2.imshow("Processed", thresholded)
    
    
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
go.stop()   
print("closing program")
cap.release()
cv2.destroyAllWindows()