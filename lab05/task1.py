import cv2

#Working with image files stored in the same folder as .py file
#Load the image from the given location
img = cv2.imread('sample01.tiff')
#Load the image from the given location in grayscale
img_grayscale = cv2.imread('sample01.tiff', 0)

#Thresholding the image (Refer to opencv.org for more details)
ret, thresh = cv2.threshold(img_grayscale, 127, 255, cv2.THRESH_BINARY)
 
#Display the images
cv2.imshow('Original', img)
cv2.imshow('Grayscale', img_grayscale)
cv2.imshow('Threshold', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

