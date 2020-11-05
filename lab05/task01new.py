import cv2
import numpy as np

trackbar_value = 75# Global variable for the latest trackbar value, default is 32
anyChange = False

def updateValue(new_value):
    # make sure to write the new value into the global variable
    global trackbar_value
    global anyChange
    trackbar_value = new_value
    anyChange = True
    return


blobparams = cv2.SimpleBlobDetector_Params()
#blobparams.filterByArea = False
blobparams.minArea = 20
blobparams.filterByCircularity = False
blobparams.minDistBetweenBlobs = 20#!!!change here
detector = cv2.SimpleBlobDetector_create(blobparams)

#Working with image files stored in the same folder as .py file
#Load the image from the given location
img = cv2.imread('sample02.tiff')
#Load the image from the given location in grayscale
img_grayscale = cv2.imread('sample02.tiff', 0)



#Thresholding the image at 75
ret, thresh = cv2.threshold(img_grayscale, 75, 255, cv2.THRESH_BINARY)
keypoints = detector.detect(thresh)#creates multiple objects, writes in variable

if len(keypoints)!=0: 
    print(keypoints[0].size)#Displays size of one object


img_grayscale = cv2.resize(img_grayscale, (0,0), fx=0.5, fy=0.5)#downscales img's width and height by 2
thresh = cv2.resize(thresh, (0,0), fx=0.5, fy=0.5)
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
cv2.imshow('Original', img)
cv2.imshow('Grayscale', img_grayscale)
cv2.imshow('Threshold', thresh)
cv2.createTrackbar("Example trackbar", "Threshold", trackbar_value, 200, updateValue)


while True:
    # Read a single image
    if anyChange == True:
        anyChange = False
        ret,thresh = cv2.threshold(img_grayscale, trackbar_value, 255, cv2.THRESH_BINARY)
        keypoints = detector.detect(thresh)
                
    #frame=cv2.bitwise_not(frame)
        #to show the detected keypoints on the screen
        thresh = cv2.drawKeypoints(thresh,keypoints,np.array([]),(0,0,255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # Add trackbar value as text on the read frame
        cv2.putText(thresh, str(trackbar_value), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        
       
        for keypoint in keypoints: # keypoints is a list of objects with for loop I take one by one and find the place of each keypoint
            cv2.putText(thresh, str((int(keypoint.pt[0]), int(keypoint.pt[1]))), (int(keypoint.pt[0]), int(keypoint.pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
        cv2.imshow('Threshold', thresh)
        cv2.imshow('Original', img)
        
       

    # Quit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#cv2.waitKey(0)
cv2.destroyAllWindows()