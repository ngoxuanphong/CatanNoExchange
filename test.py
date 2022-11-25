import numpy as np
import random
a = np.array([0,2, 3, 5, 2])
# for i in range(5):

#     a[i]
for i in range(100):
    res = np.random.choice([0,1,2,3,4], p = a/sum(a))
    print(res)