import time

n = 100000

def inner(i):
    return i+1

def outer_1(n):
    x = 0
    for i in range(n):
        x = inner(x)
def outer_2(n):
    x = 0
    for i in range(n):
        x = x+1

t0 = time.process_time()
b = outer_1(n)

t1 = time.process_time()
c = outer_2(n)
t2 = time.process_time()
print('nested call', t1-t0, 's')
print('call', t2-t1, 's')
