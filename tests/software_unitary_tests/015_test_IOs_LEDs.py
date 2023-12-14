import andi as ai
import bimms as bm
import time
from bimms import cst

BS = bm.BIMMS()

#Set LED_err_p for 1s
print("Error LED on")
BS.set_IO(cst.LED_err,1)
time.sleep(1)
print("Error LED OFF")
BS.set_IO(cst.LED_err,0)

#Set LED_status_p for 1s
print("Status LED on")
BS.set_IO(cst.LED_status,1)
time.sleep(1)
print("Status LED OFF")
BS.set_IO(cst.LED_status,0)

#Set LED_err_p for 1s and then LED_status_p
print("Error LED ON")
BS.set_IO(cst.LED_err,1)
time.sleep(1)
print("Status LED ON")
BS.set_IO(cst.LED_status,1)
time.sleep(1)
for k in range (6):
    print("Error LED Toggled")
    BS.toggle_IO(cst.LED_err)
    time.sleep(0.5)

del BS


