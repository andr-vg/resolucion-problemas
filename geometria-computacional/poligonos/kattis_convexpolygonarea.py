from sys import stdin, stdout

# use shoelace formula to compute area
def get_area(pol):
  tot = 0
  for i in range(len(pol)-1):
    x0, y0 = pol[i]
    x1, y1 = pol[i+1]
    tot += (x0*y1 - x1*y0)
  tot = tot / 2
  if ".0" in str(tot):
    num, decimals = str(tot).split(".")
  else:
    num = str(tot)
  return num

total = 0
# read total of polygons
tot = int(stdin.readline())
areas = []
for i in range(tot):
  # read each line and save in list
  line = stdin.readline().split()
  # get number of coords per polygon
  n_coords = int(line[0])
  # create polygon
  pol = []
  for i in range(1, n_coords*2 + 1, 2):
    x = int(line[i])
    y = int(line[i+1])
    pol.append((x, y))
  # replicate first point as last
  pol.append(pol[0])
  # get and save area
  areas.append(get_area(pol))

for area in areas:
  stdout.write(area+'\n')