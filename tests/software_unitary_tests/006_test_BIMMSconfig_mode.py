import bimms as bm
import time



test_cmode1 = bm.config_mode("first param","second param",2, default="first param")

print(test_cmode1=="first param")
test_cmode1(2)
print(not test_cmode1=="first param")
print(test_cmode1==2)
test_cmode1('a')


p = [i for i in range(10)]
test_cmode2 = bm.config_mode(default=1,*p)
print(test_cmode1)
print(test_cmode2)