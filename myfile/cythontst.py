from  cyt_module import subtract
import time

t0 = time.process_time()
a = subtract(3.6, 2)

t1 = time.process_time()
print(a)
print('time spend', t1-t0)
