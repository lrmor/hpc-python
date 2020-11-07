import numpy as np

import math
import datetime 

dx = 0.01
x_ser = np.arange(0,math.pi/2.0,0.1)
y_ser = np.arange(0,math.pi/2.0,dx)

print(x_ser)

#x_lower = x_ser-0.1
#x_upper = x_ser+0.1
#print(x_lower)
#print(x_upper)
tm1 = datetime.datetime.now()
fx1 = np.sin(x_ser)
dfdx = (fx1[2:]-fx1[:-2])/2/0.1
tm2 = datetime.datetime.now()
fx2 = np.cos(x_ser)
dfdx2 = (fx2[2:]-fx2[:-2])/2/0.1
tm3 = datetime.datetime.now()
mx_ser = (y_ser[1:]+y_ser[:-1])/2.0
fy = np.sum(np.sin(mx_ser)*dx)
tm4 = datetime.datetime.now()


print(mx_ser)
print(dfdx)
print(dfdx2)
print(fy)
print(tm2-tm1,"s")
print(tm3-tm2,"s")
print(tm4-tm3,"s")
