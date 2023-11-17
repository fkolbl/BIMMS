import bimms as bm
import numpy as np

p1 = {'1':1, '2':2, 't':3}
p2 = np.zeros((3,2))

val = np.ones((3,2))

res1 = bm.Results_test()

res1['parameter1'] = p1
res1['parameter2'] = p2
res1['values'] = val

print(res1.parameter1 == p1)
print(res1['parameter1']==p1)

res2 = bm.load_any(res1.save())
res2['parameter3'] = 3

print(res2)
print(res1)