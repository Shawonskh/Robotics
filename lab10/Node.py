import math

# This class represents a region of space for pathfinding. Nodes have x and y
# coordinates, type, parent, gScore and fScore
class Node:

    # Create a new node
    # x - int: x coordinate
    # y - int: y coordinate
    # type - int: type of node showing whether it's passable or part of a path
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.parent = None
        self.fScore = None
        self.gScore = None

    # This method returns a string representation. It's automatically used when
    # str(node) is used.
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    # Defines equality for nodes when node1 == node2 is used
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Defines comparison of nodes for node1 < node2
    def __lt__(self, other):
        return self.fScore < other.fScore

    # Get the distance from this node to another node
    def dist(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    # Sets the parent of this node. The parent is the previous node in the path
    def setParent(self, parent):
        self.parent = parent


# This function converts a matrix of numbers representing the field into a
# matrix of nodes.
def createNodesFromField(field):
    nodes = []
    start = None
    finish = None
    for y, row in enumerate(field):
        nodes.append([])
        for x, point in enumerate(row):
            node = Node(x, y, point)
            nodes[y].append(node)
            if point == 2:
                start = node
            elif point == 3:
                finish = node

    return nodes, start, finish
