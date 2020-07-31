x = 6
y = 9
z = 20
largest = 0
for n in range(0,200):
    flag = 0
    for c in range(0, n / z + 1):
        for b in range (0, n / y + 1):
            for a in range (0, n / x + 1):
                if(x * a + y * b + z * c == n):
                    #print a, b, c
                    flag = -1
    
    if(flag == 0):
        largest = n
print "Given package sizes %d, %d, and %d,\
 the largest number of McNuggets that cannot\
 be bought in exact quantity is: %d" % (x, y, z, largest)
