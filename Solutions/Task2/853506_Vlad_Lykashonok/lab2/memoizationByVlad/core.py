def memoize(f):
    memory = {}
    def wrapper(*args, **kwargs):
        if args not in memory:            
            memory[args] = f(*args, **kwargs)
        return memory[args]
    return wrapper

@memoize
def fibonacci(n):
    if n < 0: raise ValueError('wrong input')
    elif n <= 1: return n
    else: return fibonacci(n-1)+fibonacci(n-2)

@memoize
def factorial(n):
    if n < 0: raise ValueError('wrong input')
    elif n < 2: return 1
    else: return n * factorial(n-1)