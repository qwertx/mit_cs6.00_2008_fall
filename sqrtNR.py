def squareRootBi(x, epsilon):
    """Return y s.t. y*y is within epsilon of x"""
    assert epsilon > 0,'epsilon must be positive, not' + str(epsilon)
    low = 0
    high = max(x, 1.0)
    guess = (low + high) / 2.0
    ctr = 1
    while abs(guess**2 - x) > epsilon and ctr <= 100:
        if guess**2 < x:
            low = guess
        else:
            high = guess
        guess = (low + high)/2.0
        ctr += 1
    assert ctr <= 100, 'Iteration count exceeded'
    print 'Bi method. Num. iterrations:', ctr, 'Estimate:', guess
    return guess

def squareRootNR(x, epsilon):
    """Return y s.t. y*y is within epsilon of x"""
    assert epsilon > 0,'epsilon must be positive, not' + str(epsilon)
    x = float(x)
    guess = x/2.0
    diff = guess**2 - x
    ctr = 1
    while abs(diff) > epsilon and ctr <= 100:
        guess = guess - diff/(2.0*guess)
        diff = guess**2 - x
        ctr += 1
    assert ctr <= 100, 'Iteration count exceeded'
    print 'Bi method. Num. iterrations:', ctr, 'Estimate:', guess
    return guess
