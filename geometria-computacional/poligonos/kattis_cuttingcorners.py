from sys import stdin, stdout
from math import sqrt, degrees, acos

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

def neighbors(i, n):
    if i == 0:
        prev = -1
        next = 1
    elif i == n - 1:
        prev = i - 1
        next = 0
    else:
        prev = i - 1
        next = i + 1
    return prev, next

def cut_polygon(pol, n):
    if n <= 3:
        return pol
    # compute angles between each vertex
    angles = []
    for i in range(n):
        prev, next = neighbors(i, n)
        angles.append(angle(pol[prev], pol[i], pol[next]))        
      
    # obtain pointly vertex
    min_angle = min(angles)      
    i = angles.index(min_angle)
    prev, next = neighbors(i, len(pol))
    prev_1, _ = neighbors(prev, len(pol))
    _, next_2 = neighbors(next, len(pol))
    angle_prev = angle(pol[prev_1], pol[prev], pol[next])
    angle_next = angle(pol[prev], pol[next], pol[next_2])
    while (angle_prev > min_angle and angle_next > min_angle) and len(pol) > 3:
        # drop vertex
        angles[prev] = angle_prev
        angles[next] = angle_next
        angles.pop(i)
        pol.pop(i)
        # try with next pointly vertex
        min_angle = min(angles)
        i = angles.index(min_angle)
        prev, next = neighbors(i, len(pol))
        prev_1, _ = neighbors(prev, len(pol))
        _, next_2 = neighbors(next, len(pol))
        angle_prev = angle(pol[prev_1], pol[prev], pol[next])
        angle_next = angle(pol[prev], pol[next], pol[next_2])    
    return pol

# read total of roads
line = stdin.readline()
res = []
while line:
    # read total of vertices and trees
    values = [int(v) for v in line.split()]
    n = values[0]
    pol = [(values[i], values[i+1]) for i in range(1, len(values[1:]), 2)]
    if len(pol) > 0:
        # cut polygon and save result
        res.append(cut_polygon(pol, n))
        # read next line
        line = stdin.readline()
    else:
        break
        
for pol in res:
    r = f"{len(pol)}"
    for x in pol[0:]:
        r += f" {str(x[0])} {str(x[1])}" 
    stdout.write(f"{r}\n")