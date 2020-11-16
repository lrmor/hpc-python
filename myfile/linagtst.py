import numpy as np

a = np.random.randint(1, 15, (2,2))
b = np.random.randint(1, 15, (2,2))


#print(a)
#print(a.T)
syma = a + a.T
symb = b + b.T
c = np.dot(syma, symb)
d = np.linalg.eigvals(c)
print(syma)
print(syma)
print('dot\n',c)
print(d)
