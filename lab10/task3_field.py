import cv2
import math

from FieldDisplay import *
from Node import *
from task2_aruco import *


def createField(markers):
    # <-- Write a function for creating a 2d field of numbers like in task1, where
    # the ArUco markers show the obstacles.
    return field

if __name__ == "__main__":

    # read the image from file
    frame = cv2.imread('example.jpg', 0)

    markers = detect(frame)

    # Display the resulting image with markers
    cv2.imshow('markers', frame)

    # Create the field from the image
    field = createField(markers)

    # Create the pathfinding nodes for visualization
    nodes, start, finish = createNodesFromField(field)

    display = FieldDisplay(640, 480, len(nodes[0]), len(nodes))
    display.draw(nodes)

    # Quit the program when any key is pressed
    cv2.waitKey(0)

    # When everything done, release the capture
    print('closing program')
    cv2.destroyAllWindows()
    display.close()
