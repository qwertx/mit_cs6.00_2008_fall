from string import *
from ps3b import *

def subStringMatchExactlyOneSub(target,key):
    #case01:last char is different from key
    key01 = key[0:len(key)-1]
    match = subStringMatchExactForPS3D(target,key01)
    #case02:first char is different from key
    key02 = key[1:len(key)]
    match_temp = subStringMatchExactForPS3D(target,key02)
    for n in range(0, len(match_temp)):
        match_temp[n] = match_temp[n] - 1
    match += match_temp
    #case03:char in the middle is different from key
    for incorrect in range(1, len(key)-1):
        firstMatch = key[0:incorrect]
        secondMatch = key[incorrect + 1:len(key)]
        match_a = subStringMatchExactForPS3D(target,firstMatch)
        match_b = subStringMatchExactForPS3D(target,secondMatch)
        for n in range(0, len(match_a)):
            for k in range(0, len(match_b)):
                if (match_a[n] + len(firstMatch) + 1 == match_b[k]):
                    match.append(match_a[n])
    #delete complete match
    match = list(set(match))
    match.sort()
    final_match = []
    for n in match:
        if target[n:len(key) + n] != key:
            final_match.append(n)
       
    #print final_match
    return final_match
        
    
