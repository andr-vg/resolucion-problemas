from sys import stdin, stdout
from math import sqrt

# check for distance between 2 points
def distance(p1, p2):
  dx = p1[0] - p2[0]
  dy = p1[1] - p2[1]
  d = abs(sqrt(dx**2 + dy**2))
  return d
  
def perimeter(pol):
  tot = 0
  for i in range(len(pol)-1):
    tot += distance(pol[i], pol[i+1])
  return tot

# obtain coords (x, y) of tree using 
# distance D between P and (x, y)
# and the rect that cross vertex P and Q
def get_coords_per_tree(P, Q, D):
  x1, y1 = P
  x2, y2 = Q
  # direction vector from P to Q
  PQ = (x2-x1, y2-y1)
  # magnitude between P,Q
  mag_pq = sqrt(PQ[0]**2+PQ[1]**2)
  # normalize direction vector PQ to obtain unit vector
  PQ_norm = (PQ[0] / mag_pq, PQ[1] / mag_pq)
  # obtain coords using PQ_norm, D and P
  x = x1 + D * PQ_norm[0]
  y = y1 + D * PQ_norm[1]
  return x, y
  
def get_coords(pol, D, N):
  coords = [pol[0]]
  d_ini = D
  i = 0
  for j in range(N - 2):
    # D > d(Pi, Pi+1) -> no tree can be added, try again with next i
    while d_ini > distance(pol[i], pol[i+1]):
      # subtract d(Pi, Pi+1) to distance until find a place to set tree 
      d_ini = d_ini - distance(pol[i], pol[i+1])
      i += 1
    # D <= d(Pi, Pi+1) -> put one tree and add D to distance
    x, y = get_coords_per_tree(pol[i], pol[i+1], d_ini)
    coords.append((x, y))
    d_ini += D
  coords.append(pol[-1])
  return coords
  
# read total of roads
N = int(stdin.readline())
res = []
for j in range(N):
  # read total of vertices and trees
  n_vert, n_trees = [int(v) for v in stdin.readline().split()]
  # read each coord of polygon and save it in list
  # in this case, the coords are given clockwise order
  pol = []
  for i in range(n_vert):
    x, y = [float(u) for u in stdin.readline().split()]
    pol.append((x, y))
  # get distance between trees
  D = perimeter(pol) / (n_trees - 1)
  # obtain coords of each tree
  res.append(get_coords(pol, D, n_trees))
for i in range(len(res)):
  stdout.write(f"Road #{i+1}:\n")
  for coord in res[i]:
    stdout.write("{:.2f}".format(coord[0])+' '+"{:.2f}".format(coord[1])+'\n')
  stdout.write("\n")