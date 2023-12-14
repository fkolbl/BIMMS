import andi as ai
import bimms as bm
import time
from bimms import cst

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def toggle_bit(value, bit):
    return(value ^  (1<<(bit)))

ad2 = ai.Andi()

cst.LED_err
cst.LED_status

LED_status_p = 4
LED_err_p = 5

mask_output = 0
mask_output = (2**LED_status_p)+(2**LED_err_p)

ad2.digitalIO_set_as_output(mask_output)

#read IO
IO = ad2.digitalIO_read_outputs()

#Set LED_err_p for 1s
print("Error LED on")
IO = set_bit(IO,LED_err_p)
ad2.digitalIO_output(IO)
time.sleep(1)
print("Error LED OFF")
IO = ad2.digitalIO_read_outputs()
IO = clear_bit(IO,LED_err_p)
ad2.digitalIO_output(IO)

#Set LED_status_p for 1s
print("Status LED on")
IO = ad2.digitalIO_read_outputs()
IO = set_bit(IO,LED_status_p)
ad2.digitalIO_output(IO)
time.sleep(1)
print("Status LED OFF")
IO = ad2.digitalIO_read_outputs()
IO = clear_bit(IO,LED_status_p)
ad2.digitalIO_output(IO)

#Set LED_err_p for 1s and then LED_status_p
print("Error LED ON")
IO = ad2.digitalIO_read_outputs()
IO = set_bit(IO,LED_err_p)
ad2.digitalIO_output(IO)
time.sleep(1)
print("Status LED ON")
IO = ad2.digitalIO_read_outputs()
IO = set_bit(IO,LED_status_p)
ad2.digitalIO_output(IO)
time.sleep(1)
for k in range (6):
    print("Error LED Toggled")
    IO = ad2.digitalIO_read_outputs()
    IO = toggle_bit(IO,LED_err_p)
    ad2.digitalIO_output(IO)
    time.sleep(0.5)

ad2.close()


