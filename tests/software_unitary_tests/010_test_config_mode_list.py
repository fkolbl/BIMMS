import bimms as bm
import time
import numpy as np



p = [i for i in range(10)]

test_list = bm.config_mode_list()
test_list.add_mode("cmode1", bm.config_mode("first param","second param",2, default="first param"))
test_list.add_mode("cmode2",  bm.config_mode(*p, default=1))
test_list.add_mode("cmode3", bm.config_range(-10.3,10, default=1))

print(test_list.cmode1=="first param")

test_list.cmode1(2)
print(not test_list.cmode1=="first param")
print(test_list.cmode1==2)

test_list.cmode1('a')

print(test_list.cmode1)
print(test_list.cmode2)

print(test_list)
test_list.reset()
print(test_list)

test_list_dict = test_list.save()
test_list2 = bm.config_mode_list()
test_list2.load((test_list_dict))
print(test_list2==test_list)
test_list.cmode3(0.23)
print(not test_list2==test_list)