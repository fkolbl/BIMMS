import bimms as bm
import time
import numpy as np



test_cmode1 = bm.config_mode("first param","second param",2, default="first param")
p = [i for i in range(10)]
test_cmode2 = bm.config_mode(*p, default=1)

test_list = bm.config_mode_list()
test_list.add_mode("test_cmode1", test_cmode1)
test_list.add_mode("test_cmode2", test_cmode2)

print(test_list.test_cmode1=="first param")
test_list.test_cmode1(2)
print(not test_list.test_cmode1=="first param")
print(test_list.test_cmode1==2)
test_list.test_cmode1('a')

print(test_list.test_cmode1)
print(test_list.test_cmode2)

test_list_dict = test_list.save()

print(test_list_dict)
