import BIMMS as bm
import time
import BIMMS_constants as cst

bimms = bm.BIMMS()

state = bimms.get_state()
if (state == cst.STM32_stopped):
	print("STM32 MCU sucessfully initialized")
else:
	bimms.close()
	raise ValueError('Failed to initialize STM32 MCU. Make sure that the AD2 board is properly connected to BIMMS')
	quit()

bimms.set_state(cst.STM32_idle)
time.sleep(0.2)
state = bimms.get_state()
if (state == cst.STM32_idle):
	print("STM32 MCU sucessfully set to IDLE mode")
else:
	bimms.close()
	raise ValueError('Failed to set STM32 MCU to IDLE mode')
	quit()

bimms.set_state(cst.STM32_locked)
time.sleep(0.2)
state = bimms.get_state()
if (state == cst.STM32_locked):
	print("STM32 MCU sucessfully set to LOCKED mode")
else:
	bimms.close()
	raise ValueError('Failed to set STM32 MCU to LOCKED mode')
	quit()


bimms.close()
