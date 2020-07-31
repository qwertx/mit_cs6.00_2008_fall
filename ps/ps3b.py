from string import *

def subStringMatchExact(target,key):
    match = ()
    n = 0
    while(n <= len(target)):
        value = find(target, key, n)
        if value != -1:
            n = value + len(key)
            match2 = (value,)
            match += match2
        else:
            break
    #print match
    return match

def subStringMatchExactForPS3D(target,key):
    match = []
    n = 0
    while(n <= len(target)):
        value = find(target, key, n)
        if value != -1:
            n = value + len(key)
            match.append(value)
        else:
            break
    #print match
    return match
