from sys import stdin, stdout
from math import sqrt, degrees, acos, fabs

def distance(p0, p1):
    dx = p0[0] - p1[0]
    dy = p0[1] - p1[1]
    d = abs(sqrt(dx**2 + dy**2))
    return d

def area(pol):
    # usamos la formula de shoelace
    tot = 0
    for i in range(len(pol)-1):
        x0, y0 = pol[i]
        x1, y1 = pol[i+1]
        tot += (x0*y1 - x1*y0)
    return abs(tot / 2)

def to_vec(A, B):
    return (B[0] - A[0], B[1] - A[1])

def cross(A, B):
    return A[0] * B[1] - A[1] * B[0]

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

def angle(a, b, c):
    # ángulo en grados del punto a al punto c alrededor de b
    # vectores AB, BC
    ab = (b[0] - a[0], b[1] - a[1])
    bc = (c[0] - b[0], c[1] - b[1])
    # producto punto y magnitudes ab y bc 
    dot_prod = ab[0] * bc[0] + ab[1] * bc[1]
    mag_ab = sqrt(ab[0]**2 + ab[1]**2)
    mag_bc = sqrt(bc[0]**2 + bc[1]**2)
    # cos theta
    cos_theta = dot_prod / (mag_ab * mag_bc)
    # angulo en radianes a través del acos
    try:
        angle_rad = acos(cos_theta)
    except: # para evitar errores de redondeo cerca de los límites del coseno
        angle_rad = acos(round(cos_theta))
    # conversión a grados retornando el ángulo mínimo
    return 180 - degrees(angle_rad)

def line_intersect_seg(P, Q, A, B):
    # utilizamos la ecuación de la recta formada por los puntos A y B:
    # A x + B y + C = 0
    dy = B[1] - A[1]
    dx = A[0] - B[0]
    c = B[0] * A[1] - A[0] * B[1]
    # distancia perpendicular entre P y la recta AB
    u = fabs(dy * P[0] + dx * P[1] + c)
    # distancia perpendicular entre Q y la recta AB
    v = fabs(dy * Q[0] + dx * Q[1] + c)
    # retornamos las coordenadas de intersección ponderando la distancia de P y Q hasta la recta AB
    return ((P[0] * v + Q[0] * u) / (u + v), (P[1] * v + Q[1] * u) / (u + v))

def cut_polygon(pol, AB):
    # dividimos en dos el polígono a través de la recta AB
    A, B = AB[0], AB[1]
    pol1, pol2 = [], []
    n = len(pol)
    for i in range(n):
        left1 = cross(to_vec(A, B), to_vec(A, pol[i]))
        left2 = 0
        if i != n - 1:
            left2 = cross(to_vec(A, B), to_vec(A, pol[i+1]))
        if left1 > 0:
            pol1.append(pol[i])
        elif left1 < 0:
            pol2.append(pol[i])
        else:
            pol1.append(pol[i])
            pol2.append(pol[i])
        if left1 * left2 < 0:
            point_int = line_intersect_seg(pol[i], pol[i+1], A, B)
            pol1.append(point_int)
            pol2.append(point_int)
    if len(pol1) > 0 and pol1[0] != pol1[-1]:
        pol1.append(pol1[0])
    if len(pol2) > 0 and pol2[0] != pol2[-1]:
        pol2.append(pol2[0])
    return pol1, pol2

def in_polygon(pol, p):
    epsilon = 1e-9
    if len(pol) < 4: # menos de 3 vértices, no es un polígono
        return False
    # sumamos (restamos) los ángulos si el sentido es ccw (cw)
    tot = 0
    for i in range(len(pol)-1):
        if ccw(pol[i], p, pol[i+1]) >= 0:
            tot += angle(pol[i], p, pol[i+1])
        else:
            tot -= angle(pol[i], p, pol[i+1])
    return True if abs(tot - 360) < epsilon else False

def get_polygon(pol, lines, point):
    # dividimos el polígono por todas las rectas posibles, manteniendo siempre el subpolígono que contiene la fuente (point)
    for line in lines:
        pol1, pol2 = cut_polygon(pol, line)
        pol = pol1 if in_polygon(pol1, point) else pol2
    return pol

# donde nos guardaremos el resultado
res = []
while True:
    # coordenadas del polígono dadas en sentido horario (cw)
    try:
        # parametros de entrada
        N, W, H, x, y = [int(value) for value in stdin.readline().split()]
    except:
        break
    # poligono inicial => jardín rectangular
    pol = [(0, 0), (0, H), (W, H), (W, 0)]
    # replicamos primer punto en la ultima posición
    pol.append(pol[0])
    lines = []
    # coordenadas origen y destino de cada recta
    for i in range(N):
        x1, y1, x2, y2 = [int(value) for value in stdin.readline().split()]
        lines.append([(x1, y1), (x2, y2)])
    # recortamos hasta obtener el subpolígono que contiene la fuente en (x, y)
    pol = get_polygon(pol, lines, (x, y))
    # calculamos el área del subpolígono resultante
    res.append(area(pol))
# imprimo resultado con el formato pedido
for i in range(len(res)):
    stdout.write("Case #{}: {:.3f}\n".format(i+1, res[i]))