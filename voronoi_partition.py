import png
import random
import math

def distance(u, v):
    return math.sqrt((u[0] - v[0])**2 + (u[1] - v[1])**2)

def CalculateColour(x, y):
    minDistance = height + 1
    for i in range(numPoints):
        if distance(points[i][:2], [x, y]) < minDistance:
            minDistance = distance(points[i], [x, y])
            closestPoint = i
    [r, g, b] = points[closestPoint][2:]
    return [r, g, b]
        
height = 1000
points = []
numPoints = 100
for i in range(numPoints):
    points.append([random.uniform(0, height), random.uniform(0, height), round(random.uniform(0, 255)), round(random.uniform(0, 255)), round(random.uniform(0, 255))])

img = []
for y in range(height):
    row = ()
    for x in range(height):
        [r, g, b] = CalculateColour(x, y)
        row = row + (r, g, b)
    img.append(row)

with open('image.png', 'wb') as f:
    w = png.Writer(height, height, greyscale = False)
    w.write(f, img)
    
