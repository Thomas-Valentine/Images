import png
import random
import math

def Colour(C1,C2,Q,x,y):
    Q_ = []
    q_ = 0
    c = len(Q)
    q = random.randint(1,100)
    for i in range(len(Q)):
        q_ += Q[i]
        if q_ >= q:
            c = i
            break
    [r1,g1,b1] = C1[c]
    [r2,g2,b2] = C2[c]
    q = random.uniform(0,1)
    r = int(round(r1 + q*(r2 - r1)))
    g = int(round(g1 + q*(g2 - g1)))
    b = int(round(b1 + q*(b2 - b1)))
    return [r,g,b]

def N(x,y,s):
    if P[x][y] == -1 and [x,y] not in s:
        s.append([x,y])

def Flood(x0,y0,c):
    s = [[x0,y0]]
    while len(s) > 0:
        z = s.pop(0)
        x = z[0]
        y = z[1]
        P[x][y] = c
        if y < yh - 1:
            if X[x][y][2] == 1:
                N(x, y + 1, s)
        if y > 0:
            if X[x][y - 1][2] == 1:
                N(x, y - 1, s)
        if x < xh - 1:
            if X[x][y][0] == 1:
                N(x + 1, y, s)
            if y < yh - 1:
                if X[x][y][3] == 1:
                    N(x + 1, y + 1, s)
            if y > 0:
                if X[x][y][1] == 1:
                    N(x + 1, y - 1, s)
        if x > 0:
            if X[x - 1][y][0] == 1:
                N(x - 1, y, s)
            if y < yh - 1:
                if X[x - 1][y + 1][1] == 1:
                    N(x - 1, y + 1, s)
            if y > 0:
                if X[x - 1][y - 1][3] == 1:
                    N(x - 1, y - 1, s)
    return [x0,y0]

def R(t):
    a = 0.48458
    ps = 0
    px = []
    px_ = []
    for i in range(4):
        pt = (1 + math.cos(2*(t + 0.25*math.pi*i)))*a**(i % 2)
        px.append(pt)
        ps += pt
    for i in range(4):
        px_.append(1 if random.uniform(0,1) < px[i]*p/ps else 0)
    return px_

def V(x,y):
    r = math.sqrt(x**2 + y**2)
    if x == 0:
        t = 0.5*math.pi
    else:
        t = math.atan(y/x)
    v = t + math.pi*0.5
    return v

xh = 1920
yh = 1080
k = 15
xk = math.floor(xh/k) + 1
yk = math.floor(yh/k) + 1
p = 1


C1 = [[0,0,0],[255,255,255],[random.randint(0,255),random.randint(0,255),random.randint(0,255)]]
C2 = [[random.randint(0,255),random.randint(0,255),random.randint(0,255)],[random.randint(0,255),random.randint(0,255),random.randint(0,255)],[random.randint(0,255),random.randint(0,255),random.randint(0,255)]]
Q = [random.randint(50,75),random.randint(0,25)]


print("generating direction field...")
T = [[],[]]
for x in range(xk):
    T[0].append([])
    T[1].append([])
    for y in range(yk):
        t = random.uniform(-math.pi,math.pi)
        T[0][x].append([math.cos(t),math.sin(t)])
        T[1][x].append([0,0])
for i in range(50):
    for x in range(xk):
        for y in range(yk):
            [xs,ys] = T[i % 2][x][y]
            if x > 0:
                xs += T[i % 2][x - 1][y][0]
                if y > 0:
                    xs += T[i % 2][x - 1][y - 1][0]*0.5
                    ys += T[i % 2][x - 1][y - 1][1]*0.5
                if y < yk - 1:
                    xs += T[i % 2][x - 1][y + 1][0]*0.5
                    ys += T[i % 2][x - 1][y + 1][1]*0.5
            if x < xk - 1:
                xs += T[i % 2][x + 1][y][0]
                if y > 0:
                    xs += T[i % 2][x + 1][y - 1][0]*0.5
                    ys += T[i % 2][x + 1][y - 1][1]*0.5
                if y < yk - 1:
                    xs += T[i % 2][x + 1][y + 1][0]*0.5
                    ys += T[i % 2][x + 1][y + 1][1]*0.5
            if y > 0:
                ys += T[i % 2][x][y - 1][1]
            if y < yk - 1:
                ys += T[i % 2][x][y + 1][1]
            rs = math.sqrt(xs**2 + ys**2)
            if rs == 0:
                t = random.uniform(-math.pi,math.pi)
                [xs,ys] = [math.cos(t),math.sin(t)]
            else:
                xs /= rs
                ys /= rs
            T[(i + 1) % 2][x][y] = [xs,ys]

print("sampling adjacencies...")
X = []
P = []
for x in range(xh):
    X.append([])
    P.append([])
    for y in range(yh):
        x0 = math.floor(x/k)
        y0 = math.floor(y/k)
        [xs,ys] = T[0][x0][y0]
        if xs == 0:
            t = 0.5*math.pi
        else:
            t = math.atan(ys/xs)
        X[x].append(R(t))
        P[x].append(-1)

print("flooding...")
C = []
for x in range(xh):
    for y in range(yh):
        if P[x][y] == -1:
            [xc,yc] = Flood(x,y,len(C))
            C.append(Colour(C1,C2,Q,xc,yc))

print("converting to image...")
img = []
for y in range(yh):
    row = ()
    for x in range(xh):
        [r,g,b] = C[P[x][y]]
        row = row + (r,g,b)
    img.append(row)

with open('image.png','wb') as f:
    w = png.Writer(xh,yh,greyscale = False)
    w.write(f,img)
print("done")
