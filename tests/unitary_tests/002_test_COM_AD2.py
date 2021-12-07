import Analysis_Instrument as ai
import time

try:
	test = ai.Andi()
	print('device successfully opened')
	time.sleep(1)
	test.close()
	print('device closed')
except :
	raise ValueError('Failed to connect to AD2. Check USB connection and/or close Waveform.')

