import png
import random
import math

def R(t):
    px = []
    for i in range(4):
        pt = (1 + math.cos(2*(t + 0.25*math.pi*i)))*0.5
        px.append(pt)
    return px

def V1(C,c):
    r = C[1][0]
    g = C[1][1]
    b = C[1][2]
    C[0] += 1
    s = C[0]
    r1 = int(round(r*(s - 1)/s + c[0]/s))
    g1 = int(round(g*(s - 1)/s + c[1]/s))
    b1 = int(round(b*(s - 1)/s + c[2]/s))
    C[1] = [r1,g1,b1]

def V(x,y,c):
    r = X[x][y][0]
    g = X[x][y][1]
    b = X[x][y][2]
    r1 = max(min(r + c[0],255),0)
    g1 = max(min(g + c[1],255),0)
    b1 = max(min(b + c[2],255),0)
    X[x][y] = [r1,g1,b1]

h = 400
k = 80
p = 1

T = [[],[]]
for x in range(k):
    T[0].append([])
    T[1].append([])
    for y in range(k):
        t = random.uniform(-math.pi,math.pi)
        T[0][x].append([math.cos(t),math.sin(t)])
        T[1][x].append([0,0])
for i in range(150):
    for x in range(k):
        for y in range(k):
            [xs,ys] = T[i % 2][x][y]
            if x > 0:
                xs += T[i % 2][x - 1][y][0]
                if y > 0:
                    xs += T[i % 2][x - 1][y - 1][0]*0.5
                    ys += T[i % 2][x - 1][y - 1][1]*0.5
                if y < k - 1:
                    xs += T[i % 2][x - 1][y + 1][0]*0.5
                    ys += T[i % 2][x - 1][y + 1][1]*0.5
            if x < k - 1:
                xs += T[i % 2][x + 1][y][0]
                if y > 0:
                    xs += T[i % 2][x + 1][y - 1][0]*0.5
                    ys += T[i % 2][x + 1][y - 1][1]*0.5
                if y < k - 1:
                    xs += T[i % 2][x + 1][y + 1][0]*0.5
                    ys += T[i % 2][x + 1][y + 1][1]*0.5
            if y > 0:
                ys += T[i % 2][x][y - 1][1]
            if y < k - 1:
                ys += T[i % 2][x][y + 1][1]
            rs = math.sqrt(xs**2 + ys**2)
            if rs == 0:
                t = random.uniform(-math.pi,math.pi)
                [xs,ys] = [math.cos(t),math.sin(t)]
            else:
                xs /= rs
                ys /= rs
            T[(i + 1) % 2][x][y] = [xs,ys]
print("direction field generated")

X = []
for x in range(h):
    X.append([])
    for y in range(h):
        X[x].append([127,127,127])
for x in range(h):
    for y in range(h):
        d = 10
        c = [random.randint(-d,d),random.randint(-d,d),random.randint(-d,d)]
        x_ = x
        y_ = y
        for j in range(300):
            x1 = int(round(x_))
            y1 = int(round(y_))
            V(x1,y1,c)
            x0 = math.floor(x_*k/h)
            y0 = math.floor(y_*k/h)
            [xs,ys] = T[0][x0][y0]
            x_ += xs
            y_ += ys
            if x_ <= 0 or x_ >= h - 1 or y_ <= 0 or y_ >= h - 1:
                break
        x_ = x
        y_ = y
        for j in range(300):            
            x1 = int(round(x_))
            y1 = int(round(y_))
            V(x1,y1,c)
            x0 = math.floor(x_*k/h)
            y0 = math.floor(y_*k/h)
            [xs,ys] = T[0][x0][y0]
            x_ -= xs
            y_ -= ys
            if x_ <= 0 or x_ >= h - 1 or y_ <= 0 or y_ >= h - 1:
                break

img = []
for y in range(h):
    row = ()
    for x in range(h):
        [r,g,b] = X[x][y]
        row = row + (r,g,b)
    img.append(row)

with open('image.png','wb') as f:
    w = png.Writer(h,h,greyscale = False)
    w.write(f,img)
    
