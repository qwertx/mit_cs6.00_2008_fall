def selSort(L):
    for i in range(len(L) - 1):
        print L
        minIndx = i
        minVal = L[i]
        j = i + 1
        while j < len(L):
            if minVal > L[j]:
                minIndx = j
                minVal = L[j]
            j = j + 1
        temp = L[i]
        L[i] = L[minIndx]
        L[minIndx] = temp
    print '\n',L

def testSelSort():
    test1 = [1,6,3,4,5,2]
    raw_input('run selective test 1')
    selSort(test1)
    test2 = [6,1,2,3,4,5]
    raw_input('run selective test 2')
    selSort(test2)
    test3 = [6,5,4,3,2,1]
    raw_input('run selective test 3')
    selSort(test3)
    test4 = [1,2,3,4,5,6]
    raw_input('run selective test 4')
    selSort(test4)

##def bubbleSort(L):
##    for j in range(len(L)):
##        print L
##        for i in range(len(L) - 1):
##            if L[i] > L[i+1]:
##                temp = L[i]
##                L[i] = L[i+1]
##                L[i+1] = temp

def bubbleSort(L):
    swapped = True
    while swapped:
        swapped = False
        print L
        for i in range(len(L) - 1):
            if L[i] > L[i+1]:
                temp = L[i]
                L[i] = L[i+1]
                L[i+1] = temp
                swapped = True

def testBubbleSort():
    test1 = [1,6,3,4,5,2]
    raw_input('run bubble test 1')
    bubbleSort(test1)
    test2 = [6,1,2,3,4,5]
    raw_input('run bubble test 2')
    bubbleSort(test2)
    test3 = [6,5,4,3,2,1]
    raw_input('run bubble test 3')
    bubbleSort(test3)
    test4 = [1,2,3,4,5,6]
    raw_input('run bubble test 4')
    bubbleSort(test4)
