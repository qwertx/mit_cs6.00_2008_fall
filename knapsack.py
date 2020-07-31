def MaxVal(w, v, i, aW):
    print 'maxVal called with:', i, aW
    if i == 0:
        if w[i] <= aW:
            return v[i]
        else:
            return 0
    without_i = MaxVal(w, v, i-1, aW)
    if w[i] > aW:
        return without_i
    else:
        with_i = v[i] + MaxVal(w, v, i-1, aW-w[i])
    return max(with_i, without_i)

def fastMaxVal(w, v, i, aW, m):
    try:
        return m[(i, aW)]
    except KeyError:
        if i == 0:
            if w[i] <= aW:
                m[(i, aW)] = v[i]
                return v[i]
            else:
                m[(i, aW)] = 0
                return 0
        without_i = fastMaxVal(w, v, i-1, aW, m)
        if w[i] > aW:
            m[(i, aW)] = without_i
            return without_i
        else:
            with_i = v[i] + fastMaxVal(w, v, i-1, aW - w[i], m)
        res = max(with_i, without_i)
        m[(i, aW)] = res
    return res

def maxVal0(w, v, i, aW):
    m = {}
    return fastMaxVal(w, v, i, aW, m)
          
