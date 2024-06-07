from sys import stdin, stdout
from math import sqrt

# distancia entre 2 puntos
def distance(p1, p2):
  dx = p1[0] - p2[0]
  dy = p1[1] - p2[1]
  d = abs(sqrt(dx**2 + dy**2))
  return d

def ccw(a, b, c):
    dx1 = b[0] - a[0]
    dx2 = c[0] - a[0]
    dy1 = b[1] - a[1]
    dy2 = c[1] - a[1]
    # producto cruz < 0 -> cw
    if dy1 * dx2 > dy2 * dx1:
        return -1
    # producto cruz > 0 -> ccw
    if dy2 * dx1 > dy1 * dx2:
        return 1
    # producto cruz con diferente signo -> ccw
    if dx1 * dx2 < 0 or dy1 * dy2 < 0:
        return 1
    # colineales o sentido de giro indeterminado
    return 0 

# si un punto está contenido en un polígono convexo
# todos los puntos en orden ccw
def point_in_convex_polygon(p, pol):
    for i in range(len(pol)-1):
        if ccw(pol[i], p, pol[i+1]) <= 0: 
            return False
    return True

# reordenamos el polígono si no está en sentido ccw
# calculamos si p está en el polígono
def reorder_and_check(p, pol):
    n = len(pol)
    if n < 4:
        return False
    # reordeno si el polígono no está en sentido ccw
    if ccw(pol[1], pol[0], pol[2]) < 0:
        reversed_pol = []
        for i in range(n-1, -1, -1):
            reversed_pol.append(pol[i])
        pol = reversed_pol
    # chequeo si está en algún borde
    # sucede cuando d(Pi, point) + d(point, Pi+1) = d(Pi, Pi+1)
    for i in range(n-1):
        if distance(pol[i], p) + distance(p, pol[i+1]) - distance(pol[i], pol[i+1]) == 0:
            return True
    # calculamos si p está incluido en el poligono
    return point_in_convex_polygon(p, pol)

# Andrew's Monotone Chain Algorithm Implementation
def convex_hull(S):
    n = len(S)
    # ordeno los puntos por x e y de izq a derecha 
    S = sorted(S, key=lambda k: (k[1], k[0]))
    # los puntos forman un punto/línea/triángulo
    if n <= 3:    
        return S
    CH = [None for i in range(2*n)]
    k = 0
    # calculamos la envolvente inferior
    for i in range(n):
        while k >= 2 and not ccw(CH[k-2], CH[k-1], S[i]) > 0:
            k -= 1
        CH[k] = S[i]
        k += 1
    # calculamos la envolvente superior
    t = k + 1
    for i in range(n-2, -1, -1):
        while k >= t and not ccw(CH[k-2], CH[k-1], S[i]) > 0:
            k -= 1
        CH[k] = S[i]
        k += 1
    # se elimina punto replicado (el primer valor en el último)
    CH = CH[:k-1]
    return CH

def read_coords(n):
    points = []
    for i in range(n):
        x, y = [int(value) for value in stdin.readline().split()]
        points.append((x, y))
    return points

# donde nos guardaremos el resultado
res = []
while True:
    # lectura de nro de policías, ladrones y ciudadanos
    c, r, o = [int(value) for value in stdin.readline().split()]
    if c == 0 and r == 0 and o == 0:
        break
    # lectura de coordenadas
    c_points = read_coords(c)
    r_points = read_coords(r)
    o_points = read_coords(o)
    # determinamos los convex hull de policías y ladrones
    CH_C = convex_hull(c_points)
    CH_R = convex_hull(r_points)
    # replicamos primer punto en la última posición
    if len(CH_C) > 0:
        CH_C.append(CH_C[0]) 
    if len(CH_R) > 0:
        CH_R.append(CH_R[0])
    # verificamos para cada ciudadano, si se encuentra contenido en CH_C, CH_R o en ninguno
    citizens = []
    for i in range(o):
        if reorder_and_check(o_points[i], CH_C):
            citizens.append([o_points[i], "safe"])
        elif reorder_and_check(o_points[i], CH_R):
            citizens.append([o_points[i], "robbed"])
        else:
            citizens.append([o_points[i], "neither"])
    res.append(citizens)
    # lectura de espacio en blanco
    _ = stdin.readline()
    
# imprimimos resultados en formato pedido
for i in range(len(res)):
    stdout.write(f"Data set {i+1}:\n")
    for j in range(len(res[i])):
        stdout.write("     Citizen at ({},{}) is {}.\n".format(res[i][j][0][0], res[i][j][0][1], res[i][j][1]))
    stdout.write("\n")