from sys import stdin, stdout
from math import sqrt, degrees, acos, pi

# check for distance between 2 points
def distance(p1, p2):
  dx = p1[0] - p2[0]
  dy = p1[1] - p2[1]
  d = abs(sqrt(dx**2 + dy**2))
  return d
  
# get angle between 3 points
def angle(a, b, c):
  # angle in degrees by turning from a to c around b on cw
  # vectors AB, BC
  ab = (b[0] - a[0], b[1] - a[1])
  bc = (c[0] - b[0], c[1] - b[1])
  # dot prod 
  dot_prod = ab[0] * bc[0] + ab[1] * bc[1]
  mag_ab = sqrt(ab[0]**2 + ab[1]**2)
  mag_bc = sqrt(bc[0]**2 + bc[1]**2)
  # cos theta
  cos_theta = dot_prod / (mag_ab * mag_bc)
  # angle in radians
  angle_rad = acos(cos_theta)
  # angle to degrees
  angle_deg = degrees(angle_rad)
  # always return the minimum angle
  return 180 - angle_deg

# check if 3 points make a left turn (ccw) around a
def ccw(a, b, c):
  dx1 = b[0] - a[0]
  dx2 = c[0] - a[0]
  dy1 = b[1] - a[1]
  dy2 = c[1] - a[1]
  # det dy1 * dx2 - dy2 * dx1 > 0
  if dy1 * dx2 > dy2 * dx1:
    return -1
  # det dy1 * dx2 - dy2 * dx1 < 0
  if dy2 * dx1 > dy1 * dx2:
    return 1
  # cross product different sign
  if dx1 * dx2 < 0 or dy1 * dy2 < 0:
    return 1
  return 0 #  colineals or turn is not determined 
  
# check if a point is inside of a polygon
# the sum of the angles between each pair of vertex and the point P is 360°
def in_polygon(pol, p):
  epsilon = 1e-9
  if len(pol) <= 4:
    return "F"
  # check if polygon is given in ccw and reorder
  if ccw(pol[1], pol[0], pol[2]) < 0:
    reversed_pol = []
    for i in range(len(pol)-1, -1, -1):
      reversed_pol.append(pol[i])
    pol = reversed_pol
  # check if point is on an edge or vertex
  # it happens when the sum of distance between d(Pi, point) + d(point, Pi+1) = d(Pi, Pi+1)
  for i in range(len(pol)-1):
    if distance(pol[i], p) + distance(p, pol[i+1]) - distance(pol[i], pol[i+1]) == 0:
      return "F"
  # get sum of angles (if makes a right turn plus angle, otherwise subtract angle)
  tot = 0
  for i in range(len(pol)-1):
    if ccw(p, pol[i], pol[i+1]) >= 0:
      tot -= angle(pol[i], p, pol[i+1])
    else:
      tot += angle(pol[i], p, pol[i+1])
  return "T" if abs(tot - 360) < epsilon else "F"

# read total of vertices from polygon
n = int(stdin.readline())
res = []
while n:
  # read each coord of polygon and save it in list
  # in this case, the coords are given clockwise order
  pol = []
  for i in range(n):
    x, y = stdin.readline().split()
    pol.append((int(x), int(y)))
  # replicate first point as last
  pol.append(pol[0])
  # get point P
  px, py = stdin.readline().split()
  p = (int(px), int(py))
  # get and save area
  res.append(in_polygon(pol, p))
  # read next line
  n = int(stdin.readline())

for r in res:
  stdout.write(r+'\n')