def fastFib(n, memo):
    if not n in memo:
        memo[n] = fastFib(n-1, memo) + fastFib(n-2, memo)
    return memo[n]

def fib1(n):
    memo = {0:0, 1:1}
    return fastFib(n, memo)
