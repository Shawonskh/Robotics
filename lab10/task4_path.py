import cv2
from TSP import *
from task1_astar import *
from task2_aruco import *
from task3_field import *

def findShortestPath(markers, robotID):
    tsp = TSP()
    # <-- Write a function for calculating the shortest path using the TSP library.
    # Use the robotID given to the function to determine which point is the start
    # of the path

    return path

if __name__ == "__main__":
    # read the image from file
    frame = cv2.imread('example.jpg', 0)

    markers = detect(frame)

    # Display the resulting image with markers
    cv2.imshow('markers', frame)

    path = findShortestPath(markers, 20)

    # Create the field from the image
    field = createField(markers)
    # Create the pathfinding nodes for visualization
    nodes, start, finish = createNodesFromField(field)

    for node in path:
        nodes[node.y][node.x].type = 4

    display = FieldDisplay(640, 480, len(nodes[0]), len(nodes))
    display.draw(nodes)

    # Quit the program when any key is pressed
    cv2.waitKey(0)

    # When everything done, release the capture
    print('closing program')
    cv2.destroyAllWindows()
    display.close()
