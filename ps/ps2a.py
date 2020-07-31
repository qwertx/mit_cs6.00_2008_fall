continuous = 0
n = 0
while(continuous <= 6):
    flag = 0
    for c in range(0, n / 20 + 1):
        for b in range (0, n / 9 + 1):
            for a in range (0, n / 6 + 1):
                if(6 * a + 9 * b + 20 * c == n):
                    #print a, b, c
                    flag = -1
    
    if(flag == 0):
        #print n
        continuous = 0
    else:
        continuous += 1
    n += 1
largest = n - 8
print "Largest number of McNuggets that\
 cannot be bought in exact quantity: %d" % largest
