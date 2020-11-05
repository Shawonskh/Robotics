from math import atan2, degrees

# ask all required vector coordinates. Keep in mind these are not the same as point coordinates

x1 =input('Enter A vector x coordinate -- ')

y1 =input('Enter A vector y coordinate -- ')

x2 = input('Enter B vector x coordinate -- ')

y2 = input('Enter B vector y coordinate -- ')

dot = x1*x2 + y1*y2      # dot product
det = x1*y2 - y1*x2      # determinant
angle = degrees(atan2(det, dot))  # atan2(y, x) or atan2(sin, cos)

print(angle) # the final angle between the vectors in degrees from -180 to 180.
