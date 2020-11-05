import time

from Graphics import *


# This class handles drawing a map onto the screen and visualizing obstacles and paths
class FieldDisplay:

    # width - int: width of the graphical window in pixels
    # height - int: height of the graphical window in pixels
    # gridWidth - int: number of nodes in the x direction
    # gridHeight - int: number of nodes in the y direction
    def __init__(self, width, height, gridWidth, gridHeight):
        self.win = GraphWin('Path planning', width, height)
        # Set the internal coordinate system to match the node coordinates
        self.win.setCoords(0, gridHeight, gridWidth, 0)
        self.win.setBackground("white")

    # Draw a matrix of nodes into the graphical window
    # nodes - list of (list of Node)
    def draw(self, nodes):
        for row in nodes:
            for node in row:
                sq = Rectangle(Point(node.x, node.y), Point(node.x + 1, node.y + 1))
                sq.draw(self.win)
                if node.parent is not None:
                    circ = Circle(Point(node.x + 0.5, node.y + 0.5), 0.1)
                    circ.draw(self.win)
                    linex = (node.x - node.parent.x) * 0.5
                    liney = (node.y - node.parent.y) * 0.5
                    line = Line(Point(node.x + 0.5, node.y + 0.5), Point(node.x + 0.5 - linex, node.y + 0.5 - liney))
                    line.draw(self.win)
                # Obstacle
                if node.type == 0:
                    sq.setFill(color_rgb(0, 0, 0))
                # Passable terrain
                if node.type == 1:
                    sq.setFill(color_rgb(230, 230, 200))
                # Start
                if node.type == 2:
                    sq.setFill("green")
                # End
                if node.type == 3:
                    sq.setFill("red")
                # Path
                if node.type == 4:
                    sq.setFill(color_rgb(220, 130, 220))

    # Wait until a mouse click and close the window
    def closeOnMouse(self):
        self.win.getMouse()
        self.win.close()

    # Close the display immediately
    def close(self):
        self.win.close()
