import numpy as np
import matplotlib.pyplot as plt


#a = np.random.random(1000)
a = np.random.normal(10,5,10000)

print(a)

print(np.mean(a))
print(np.std(a))
plt.hist(a,bins = 50)
plt.show()
