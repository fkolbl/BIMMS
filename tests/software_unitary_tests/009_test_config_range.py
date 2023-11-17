import bimms as bm
import time
import numpy as np



test_cmode1 = bm.config_range(-10,2, default=1)

print(test_cmode1)

test_cmode2 = bm.config_range(-10.3,10, default=1)
test_cmode2(27)
test_cmode2(3.4)
print(test_cmode2)

test_cmode2.reset()
print(test_cmode2)