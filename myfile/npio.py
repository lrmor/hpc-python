import numpy as np


fi = np.loadtxt("xy-coordinates.dat")

print(fi)
print(type(fi))
fo = fi + np.array([0,2.5])
print(fo)

np.savetxt("xytrans.dat",fo, fmt = '%.5f')
