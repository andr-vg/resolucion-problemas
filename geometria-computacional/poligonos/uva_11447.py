from sys import stdin, stdout

# use shoelace formula to compute area
def area(pol):
  tot = 0
  for i in range(len(pol)-1):
    x0, y0 = pol[i]
    x1, y1 = pol[i+1]
    tot += (x0*y1 - x1*y0)
  return tot / 2
  
# the capacity of each reservoir is given by the volume V:
# V = area_of_polygon * W 
def capacity(pol, W):
  return area(pol) * W

# read total of reservoirs
T = int(stdin.readline())
res = []
for j in range(T):
  # blank space
  _ = stdin.readline()
  # read total of vertices from polygon
  N = int(stdin.readline())
  # read each coord of polygon and save it in list
  # in this case, the coords are given clockwise order
  pol = []
  ans = ""
  for i in range(N):
    x, y = stdin.readline().split()
    pol.append((int(x), int(y)))
  # replicate first point as last
  pol.append(pol[0])
  # get width
  W = int(stdin.readline())
  # initial capacity (%), water consumition (mt3) and water falling (mt3)
  cap_i, water_c, water_f = [float(x) for x in stdin.readline().split()]
  # total capacity
  tot_c = capacity(pol, W)
  # initial capacity
  ini_c = cap_i * tot_c / 100
  # check for lack of water
  half_c = ini_c - water_c
  if half_c < 0:
    half_c = 0
    ans += "Lack of water. "
  # check for excess of water
  final_c = half_c + water_f
  if final_c > tot_c:
    final_c = 100
    ans += "Excess of water. "
  else: 
    final_c = int(final_c * 100 / tot_c)
  ans += f"Final percentage: {final_c}%"
  # save answer
  res.append(ans)

for r in res:
  stdout.write(r+'\n')