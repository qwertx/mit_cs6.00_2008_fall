from string import *

def countSubStringMatch(target, key):
    n = 0
    count = 0
    while(n <= len(target)):
        value = find(target, key, n)
        if value != -1:
            n = value + len(key)
            count += 1
        else:
            break
    if count == 0:
        print "There is no match."
    else:
        print "The number of instances of the key\
 in the target string is: %d" % count

def countSubStringMatchRecursive(target, key, default = 0):
    if (find(target, key) == -1):
        print "The number of instances of the key\
 in the target string is: %d" % default
    else:
        default += 1
        return countSubStringMatchRecursive(target[(find(target, key)+len(key)):len(target) + 1], key, default)        
        
