W, L = 3168, 3880

file = open(r"stat.txt", "r")
output_file = open(r"stat_norm.txt", "w")
for i in range(152):
    x = file.readline().strip() 
    y = file.readline().strip()
    output_file.write(str(float(x)/W)+"\n")
    output_file.write(str(float(y)/L)+"\n")
