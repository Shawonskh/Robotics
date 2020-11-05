from math import sqrt, degrees, atan2

class Drive:

    # The Drive object needs to know the path that it should follow
    # path - list of Node: shortest path return by the TSP library
    def __init__(self, path):  # Constructor
        self.path = path
        self.next_drive_index = 0
        self.current_point = path[0]

    # Get the next action the robot should execute, based on its front and back coordinates
    # robot_back - list of float: coordinates of the marker corner towards the back of the robot
    # robot_front - list of float: coordinates of the marker corner towards the front of the robot
    def get_action(self, robot_back, robot_front):
        robot_center = ((robot_front[0] + robot_back[0]) / 2, (robot_front[1] + robot_back[1]) / 2)  # find the center coordinate pair of the robot

        while sqrt((self.current_point.x * 10 - robot_center[0]) ** 2 + (self.current_point.y * 10 - robot_center[1]) ** 2) < 20:  # When close enough to destination point, then take next point
            self.next_drive_index += 1
            if self.next_drive_index == len(self.path) - 1:  # If arrived in final point, send stop
                return 'S'
            self.current_point = self.path[self.next_drive_index]  # take next point from path array

        length_to_next_destination = sqrt((self.current_point.x * 10 - robot_center[0]) ** 2 + (self.current_point.y * 10 - robot_center[1]) ** 2)

        if length_to_next_destination > 100:  # If further away than 100px, allow quite small angle deviation
            angle_miss_allowed = 5  # 5 degrees in each direction
        elif length_to_next_destination < 30:  # If very close, allow quite big miss, because the point will be reached anyway, and don't want to rotate too much around the point
            angle_miss_allowed = 30
        else:
            angle_miss_allowed = 30 - 25*(length_to_next_destination-30)/70  # Make linear function between 100 and 30 pixel distance

        x1 = robot_front[0] - robot_back[0]  # Robot vector x
        y1 = robot_front[1] - robot_back[1]  # Robot vector y

        x2 = self.current_point.x * 10 - robot_center[0]  # From robot center to next destination x
        y2 = self.current_point.y * 10 - robot_center[1]  # From robot center to next destination y

        dot = x1 * x2 + y1 * y2  # dot product
        det = x1 * y2 - y1 * x2  # determinant
        angle = degrees(atan2(det, dot))  # atan2(y, x) or atan2(sin, cos)

        # Right
        if angle > angle_miss_allowed:
            return 'R'
        # Left
        elif angle < -angle_miss_allowed:
            return 'L'
        # Forward
        else:
            return 'F'

