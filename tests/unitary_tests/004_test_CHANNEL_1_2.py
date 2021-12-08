import bimms as bm
import time
import numpy as np
import matplotlib.pyplot as plt

print('======== Channel 1 Test ========')
print('- Connect CH1 + to AWG1')
print('- Connect CH1 - to GND')
input('- Press a Key when ready')

#MEASURE OFFSET CH1
gain_IA = 1
acqu_duration = 1.0
max_offset = 1.0

print("Test offset Channel 1...")
BS = bm.BIMMS()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on Channel 1')


offset_AC = bm.Measure_Offset(BS = BS,channel = 1,coupling = 'AC')
if (np.abs(offset_AC)<np.abs(offset_DC)):
	print("WARNING: DC coupled offset should be lower than AC coupled offset")

print("DONE!")

BS.close()

print("Test gain Channel 1...")
gain_array_IA = np.array([1,2,4,5,10,20,25,50,100])
tol_gain = 5 #5% tolerance on measured gain to pass
amp_AWG_max = 1
max_IA_output = 1
fmin = 100
fmax = 100e3
offset = 0
n_pts = 20
settling_time = 0.01
NPeriods = 8
for idx in range (len(gain_array_IA)):
	gain_IA = gain_array_IA [idx]
	print('Gain IA: ',gain_IA,'V/V')
	amp_awg = max_IA_output/gain_IA
	print('AWG Amplitude: ',amp_awg,'V')
	BS = bm.BIMMS()
	BS.set_STM32_idle()
	BS.set_recording_voltage(coupling = 'DC', gain = gain_IA)
	BS.set_config()
	BS.interface.configure_network_analyser()
	vrange = round(amp_awg * gain_IA * 1.5,2)
	freq, gain_mes, phase_mes, gain_ch1 = BS.interface.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp_awg,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
	mean_gain = np.mean(gain_ch1)
	error = 100*np.abs(mean_gain-gain_IA)/gain_IA
	if (error>tol_gain):
		BS.close()
		raise ValueError('ERROR: Failed to measure expected gain on Channel 1')
	BS.close()

print("Channel 1 sucessfully all pass tests.")



print('======== Channel 2 Test ========')
print('- Connect Channel 2 + to AWG1')
print('- Connect Channel 2 - to GND')
input('- Press a Key when ready')

print("NOT IMPLEMENTED YET")
pass 			#TO DO LATER


