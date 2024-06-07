from sys import stdin, stdout

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

# Andrew's Monotone Chain Algorithm Implementation
def convex_hull(points, n):
    # order points by y bottom up and then x from left to right
    points = sorted(points, key=lambda k: (k[1], k[0]))
    if n < 3:    
        return points
    convex_hull = [None for i in range(2*n)]
    k = 0
    # obtain coords from lower hull
    for i in range(n):
        while k >= 2 and not ccw(convex_hull[k-2], convex_hull[k-1], points[i]) > 0:
            k -= 1
        convex_hull[k] = points[i]
        k += 1
    # obtain coords from upper hull
    t = k + 1
    for i in range(n-2, -1, -1):
        while k >= t and not ccw(convex_hull[k-2], convex_hull[k-1], points[i]) > 0:
            k -= 1
        convex_hull[k] = points[i]
        k += 1
    # resize convex hull (last one includes first point)
    convex_hull = convex_hull[:k-1]

    return convex_hull

# read total of coords
n = int(stdin.readline())
res = []
while n:
    # read each coord and save in list
    P = []
    for i in range(n):
        x, y = [int(k) for k in stdin.readline().split()]
        P.append((x, y))
    # compute algorithm and save polygon
    # also remove duplicates with set
    P = set(P)
    res.append(convex_hull(P, len(P)))
    # read next polygon
    n = int(stdin.readline())

for pol in res:
    stdout.write(str(len(pol))+'\n')
    for coord in pol:
        stdout.write(f'{coord[0]} {coord[1]}\n')