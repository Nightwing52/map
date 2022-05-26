from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

W, L = 500, 612
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

def scale(dist):
    return max(0, 256-int(dist)*5)
def is_close(a, b): 
    return ((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)/196608 < 0.1

file = open(r"stat_norm.txt", "r")
stations = np.zeros((152, 2))
for i in range(152):
    x = W*float(file.readline().strip())
    y = L*float(file.readline().strip())
    stations[i, 0] = x
    stations[i, 1] = y
file.close()

img = Image.open("red_small.png")
data = img.load()

for i in range(W): #x
    print(i/W)
    for j in range(L): #y
        if is_close(data[i, j], BLACK):
            dist = np.min(np.sqrt((i-stations[:, 0])**2+(j-stations[:, 1])**2))
            scale_dist = scale(dist)
            data[i, j] = (0, scale_dist, scale_dist)

img.save("out.png")