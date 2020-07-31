import math
index = 1
n = 1
while(index < 1000):
    numbers = 2 * n + 1
    test = 3
    i = 0
    while(test <= math.sqrt(numbers)):
        if ((numbers % test) != 0):
            test = test + 2
        else:
            i = -1
            break

    n = n + 1
    if (i == 0):
        index = index + 1
print numbers
        
        
        
