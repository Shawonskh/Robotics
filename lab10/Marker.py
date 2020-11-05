class Marker:

	# A marker includes an id number and corner coordinates. The coordinates can be
	# accessed in several ways:
	# marker.x1 gets the x-coordinate of the first corner, and similarly for other
	# coordinates.
	# marker.x gets a list of all x-coordinates
	# marker.corners is a list of coordinate pairs for all corners
	def __init__(self, id, corners):
		self.id = id
		self.corners = corners

		self.x1 = corners[0][0]
		self.y1 = corners[0][1]

		self.x2 = corners[1][0]
		self.y2 = corners[1][1]

		self.x3 = corners[2][0]
		self.y3 = corners[2][1]

		self.x4 = corners[3][0]
		self.y4 = corners[3][1]

		self.x = [self.x1, self.x2, self.x3, self.x4]
		self.y = [self.y1, self.y2, self.y3, self.y4]

# Parse the structure returned by ArUco detector into a list of markers
def parseMarkers(detected):
	corners = detected[0]
	ids = detected[1]

	markers = []

	for i, corner in enumerate(corners):
		marker = Marker(ids[i][0], corner[0])
		markers.append(marker)

	return markers
