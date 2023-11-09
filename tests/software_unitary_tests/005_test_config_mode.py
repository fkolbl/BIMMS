import bimms as bm
import time
import numpy as np



test_cmode1 = bm.config_mode("first param","second param",2, default="first param")

print(test_cmode1=="first param")
test_cmode1(2)
print(not test_cmode1=="first param")
print(test_cmode1==2)
test_cmode1('a')


p = [i for i in range(10)]
test_cmode2 = bm.config_mode(*p, default=1)
print(test_cmode1)
print(test_cmode2)
