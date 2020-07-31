from ps3b import *

def constrainedMatchPair(target,firstMatch,secondMatch):
    if firstMatch == '':
        match = subStringMatchExact(target,secondMatch)
    elif secondMatch == '':
        match = subStringMatchExact(target,firstMatch)
    else:
        match = ()
        match_a = subStringMatchExact(target,firstMatch)
        match_b = subStringMatchExact(target,secondMatch)
        for n in range(0, len(match_a)):
            for k in range(0, len(match_b)):
                if (match_a[n] + len(firstMatch) + 1 == match_b[k]):
                    match2 = (match_a[n],)
                    match += match2
    print match
                
