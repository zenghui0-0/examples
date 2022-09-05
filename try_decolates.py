import time
from functools import wraps

def exeTime(func):
    start = time.time()
    @wraps(func)
    def execFunc(*args):
        start = time.time()
        res = func(*args)
        end = time.time()
        print(end - start)
        return res
    return execFunc

@exeTime
def A(a, b):
    time.sleep(1)
    return a + b

@exeTime
def B():
    time.sleep(5)

print(A(1, 2))
B()