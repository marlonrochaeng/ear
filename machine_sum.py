import math
import os

file = list(open(os.path.join("1024x32", "A.u_c_hihi")))

somas = []
media = 0

for j in range(1,1025):
    soma_wt = 0
    for i in range(1,33):
        soma_wt += float(file[i*j-1])
    somas.append(soma_wt)
    media += soma_wt
somas.sort()
print(media/len(somas))
