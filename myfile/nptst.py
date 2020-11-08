import numpy as np
import matplotlib.pyplot as plt

#a = np.zeros((8,8))
a = np.arange(64).reshape(8,8)
b,c = np.split(a,2)
d,e = np.split(a,2, axis =1 )
k = np.concatenate((b,c))
k1 = np.concatenate((c,b))
k2 = np.concatenate((e,d),axis = 1)
print(k)
print(k1)
print(e)
print(k2)
fo = np.loadtxt("points_circle.dat")
trans = np.array([2.1,1.1])
fn = fo * trans
print(fo)
print(type(fo))
x, y = np.split(fo, 2, axis = 1)
x1, y1 = np.split(fn, 2, axis = 1)
print(x)

plt.plot(x, y, 'ro')
plt.plot(x1, y1, 'go')
plt.show()
