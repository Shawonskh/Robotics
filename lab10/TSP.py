import itertools
import math

class TSP:
    def __init__(self):
        self.points = []  # list of point IDs on path
        self.distances = {}  # map of distances between each point pair
        self.paths = {}
        self.startID = 0  # start point ID

    # Register a point that needs to be visited
    # pointID - int: id number of the point
    def add_point(self, pointID):
        self.points.append(pointID)  # adding new point to the regular path points list

    # Register the start point
    # pointID - int: id number of the point
    def add_start_point(self, pointID):
        self.startID = pointID  # Start ID is kept always in the beginning of the path array

    # Register the path and distance between two points
    # point1ID - int: id of the first point
    # point2ID - int: id of the second point
    # path - list of Node: the path to get from point1 to point2
    # length - float: the length of the path from point1 to point2
    def add_path(self, point1ID, point2ID, path, length):
        if(point1ID in self.distances):
            self.paths[point1ID][point2ID] = path
            self.distances[point1ID][point2ID] = length
        else:
            self.paths[point1ID] = {point2ID : path}
            self.distances[point1ID] = {point2ID : length}

        if(point2ID in self.distances):  # The distance is stored in both ways for faster access
            self.paths[point2ID][point1ID] = reversed(path)
            self.distances[point2ID][point1ID] = length
        else:
            self.paths[point2ID] = {point1ID : reversed(path)}
            self.distances[point2ID] = {point1ID : length}

    # Find the shortest path for visiting all registered points
    def shortest_path(self):
        perm = list(itertools.permutations(self.points))  # Get all possible orders of the normal path nodes
        perm_lists = []
        for elem in perm:
            from_start_permutation = list(elem)
            from_start_permutation.insert(0, self.startID)
            perm_lists.append(from_start_permutation)  # Add the starting position in front of each order
        min_dist = math.inf
        min_perm = []
        for elem in perm_lists:  # Go through all the possibilities...
            this_dist = 0
            for i in range(len(elem) - 1):
                this_dist += self.distances[elem[i]][elem[i + 1]]  # ... calculate distance by adding distances between every two points on the path...
            if this_dist < min_dist:  # ... and if the distance is smaller than any found previously, then save it as smallest and continue search
                min_dist = this_dist
                min_perm = elem
        # Combine the final path:
        the_best_path = []
        for point_order in range(len(min_perm[:-1])):
            point1 = min_perm[point_order]
            point2 = min_perm[point_order + 1]
            the_best_path += self.paths[point1][point2]
        return min_dist, min_perm, the_best_path
