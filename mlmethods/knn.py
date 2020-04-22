import math

def euclidDist(p1,p2):
    return (math.sqrt((math.pow(abs(p2[0]-p1[0]),2) + math.pow(abs(p2[1]-p1[1]),2))))

print(euclidDist([1,1], [2,2]))
