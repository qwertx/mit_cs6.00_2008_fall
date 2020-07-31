def subset(fromlist,tolist):
    n = len(fromlist)
    for i in range(1, 2**n):
        bi = bin(i)
        templist = []
        for j in range(-len(bi)+2, 0):
            if bi[j] == '1':
                templist.append(fromlist[j])
        print templist
        tolist.append(templist)
    return tolist
                
                
