import math

def shan(e):
    return -sum([p * math.log(p,2) for p in e if p > 0]) 
    
print(shan([9/14, 5/14]))
print(shan([11/14, 3/14]))
print(shan([1/3, 1/3, 1/3]))