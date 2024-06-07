from sys import stdin, stdout
from math import sqrt, ceil

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

def to_vec(A, B):
    return (B[0] - A[0], B[1] - A[1])

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

# verifico si un punto Q esta ente las líneas paralelas que pasan por P y el segmento AB
def point_between_lines(Q, P, A, B):
    # caso Ay = By, verifico si Qy está entre Py y Ay
    if A[1] == B[1]:
        y_min = min(A[1], P[1])
        y_max = max(A[1], P[1])
        if Q[1] >= y_min and Q[1] <= y_max:
            return True
    # verifico si Qx está entre Px y Ax
    else:
        # caso Ax = Bx
        if A[0] == B[0]:
            x1 = A[0]
            x2 = P[0]
        # caso general
        else:
            # ecuacion de una linea
            m = (B[1] - A[1]) / (B[0] - A[0])
            x1 = (Q[1] - A[1]) / m + A[0]
            x2 = (Q[1] - P[1]) / m + P[0]
        x_min = min(x1, x2)
        x_max = max(x1, x2)
        if Q[0] >= x_min and Q[0] <= x_max:
            return True
    return False

# distancia minima entre un punto P y el segmento AB
# usando la proyeccion de AP sobre AB
def min_distance_to_segment(P, A, B):
    # obtenemos vectores AB y AP:
    AB = to_vec(A, B) 
    AP = to_vec(A, P)
    # producto escalar entre AP * AB 
    AP_AB = AP[0]*AB[0] + AP[1]*AB[1]
    # producto escalar entre AB * AB 
    AB_AB = AB[0]**2 + AB[1]**2
    # escalar de la proyeccion de AP sobre AB
    t = AP_AB / AB_AB
    if t >= 0 and t <= 1:
        # P_proy es el punto en el segmento AB cuya distancia a P es minima
        # P_proy = A + t * AB
        P_proy = (A[0] + t * AB[0], A[1] + t * AB[1])
        D = distance(P, P_proy)
    elif t < 0:
        # la distancia minima es la distancia de A a P
        D = distance(A, P) 
    else:
        # la distancia minima es la distancia de B a P
        D = distance(B, P)
    return D

def min_width(pol, n):
    min_distance = None
    # comparamos distancia de cada punto respecto al resto
    for i in range(n):
        # proximos vertices
        k = (i + 1) % n
        next_k = (k + 1) % n
        # siempre que el próximo no sea el mismo punto
        while next_k != i:
            # calculamos la distancia minima entre el vertice y el
            # segmento formado por los siguientes 2 vertices
            # redondeamos al multiplo mas cercano de 1/100
            d = ceil(min_distance_to_segment(pol[i], pol[k], pol[next_k]) * 100) / 100
            # actualizamos distancia minima hasta ahora
            if min_distance == None or d < min_distance:
                # verificamos si esta distancia incluye a todos los puntos dentro de [x_min, x_max] o [y_min, y_max]
                included = True
                j = 0
                # si al menos un punto esta fuera del rango entre estos puntos, no actualizamos la distancia minima
                while (included) and j < n:
                    # verificamos cuando j no es el mismo punto P, A o B 
                    if not j in [i, k, next_k]:
                        if not point_between_lines(pol[j], pol[i], pol[k], pol[next_k]):
                            included = False
                    j += 1
                if included:                    
                    min_distance = d
            k = next_k
            # proximo vertice
            next_k = (k + 1) % n
    return min_distance              

res = []
while True:
    # nro de puntos de cada poligono
    n = int(stdin.readline())
    if n == 0:
        break
    pol = []
    # guardamos los puntos en una lista
    for i in range(n):
        x, y = [int(value) for value in stdin.readline().split()]
        pol.append((x,y))
    # calculamos convex hull para no calcular entre puntos internos
    ch = convex_hull(pol)
    # calculamos el ancho mínimo y guardamos resultado
    res.append(min_width(ch, len(ch)))
# imprimimos resultado
for i in range(len(res)):
    stdout.write("Case {}: {:.2f}\n".format(i+1, res[i]))