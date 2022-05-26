from PIL import Image
from collections import deque

W, L = 3168, 3880
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

def __dist__(pix, tar): #returns distance between pixel and target
    return ((pix[0]-tar[0])**2+(pix[1]-tar[1])**2+(pix[2]-tar[2])**2)/196608

def is_close(a, b, tol=0.1): #determines if pixel a is close to color b; a, b = (r, g, b)
    return __dist__(a, b) < tol

def is_color(a, b):
    return a[0:3] == b

def cal_com(pixels):
    sum_x, sum_y = 0.0, 0.0
    for pixel in pixels:
        sum_x += pixel[0]
        sum_y += pixel[1]
    return (sum_x/len(pixels), sum_y/len(pixels))

def process(image, tol=0.1): #does blob detection; turns blobs of WHITE to WHITE; blobs not big enough are turned black
    img = Image.open(image)
    data = img.load()

    for i in range(W): #x
        if i % 100:
            print(i/W)
        for j in range(L): #y
            if is_close(data[i, j], WHITE, tol):
                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)]
                num_white_neigh = sum([int(is_close(data[neighbor[0], neighbor[1]], WHITE)) for neighbor in neighbors])
                if num_white_neigh >= 3:
                    data[i, j] = WHITE
                else:
                    data[i, j] = BLACK
            else:
                data[i, j] = BLACK
    img.save("red_proc.png")

def locate(image, cutoff, color=WHITE, out=RED): #locates subway stations; requires processed image
    img = Image.open(image)
    data = img.load()

    blobs = []
    for i in range(W): #x
        if i % 100:
            print(i/W)
        for j in range(L): #y  
            if is_color(data[i, j], color):
                white = [] #white pixels
                seen = [(i, j)] #seen pixels
                q = deque() #queue
                q.append((i, j))
                while q: #while not empty
                    curr = q.popleft()
                    white.append(curr)

                    #adding not-seen pixels
                    x, y = curr[0], curr[1]
                    neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                    valid_next = [is_color(data[neighbor[0], neighbor[1]], color) and neighbor not in seen for neighbor in neighbors]
                    for k, neighbor in enumerate(neighbors):
                        if valid_next[k]:
                            q.append(neighbor)
                            seen.append(neighbor)
                
                #if big enough add to blobs
                if len(white) > cutoff:
                    blobs.append(cal_com(white))
                    for pixel in white:
                        data[pixel[0], pixel[1]] = out
                else:
                    for pixel in white:
                        data[pixel[0], pixel[1]] = BLACK
            elif not is_color(data[i, j], out):
                data[i, j] = BLACK

    img.save("red_stat.png")
    return blobs

#process("red.png", tol=0.05)
blobs = locate("red_stat2.png", cutoff=95, color=RED, out=WHITE)

file = open(r"stat.txt", "w")
for blob in blobs:
    file.write(str(blob[0])+"\n")
    file.write(str(blob[1])+"\n")
file.close()