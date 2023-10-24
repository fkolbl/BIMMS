import bimms as bm
import time
import numpy as np
import matplotlib.pyplot as plt

print('======== Current source test ========')
print('Plug a 1k resistor')
input('- Press a Key when ready')

BS = bm.BIMMS()
BS.set_STM32_idle()



#MEASURE OFFSET CH1
gain_IA = 1
acqu_duration = 1.0
max_offset = 1.0

print("Test offset current source ...")
BS.set_current_excitation(coupling = 'DC', differential_stim = False)
BS.set_2_points_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value on current source')
BS.set_current_excitation(coupling = 'AC', differential_stim = False)
BS.set_2_points_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')
BS.set_current_excitation(coupling = 'DC', differential_stim = True)
BS.set_2_points_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')
BS.set_current_excitation(coupling = 'AC', differential_stim = True)
BS.set_2_points_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')

BS.set_current_excitation(coupling = 'DC', differential_stim = True, High_gain = True)
BS.set_2_points_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')

BS.set_current_excitation(coupling = 'AC', differential_stim = True,DC_feedback = True)
BS.set_2_points_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')

print("DONE!")


print("Test gain current source ...")

################
## Parameters ##
################
amp = 1
fmin = 1000
fmax = 100e3
offset = 0
n_pts = 20
settling_time = 0.01
NPeriods = 16
high_gain_min = 50000
high_gain_max = 1000
low_gain_min = 94000
low_gain_max = 47000
load = 1000
tolerance = 10 #10% tolerance on measured gain

BS.set_current_excitation(coupling = 'DC', differential_stim = True,DC_feedback = False,High_gain = False)
BS.set_recording_voltage(coupling = 'DC', gain = 1)
BS.set_2_points_config()
BS.set_config()
BS.interface.configure_network_analyser()
vrange = round(amp,2)
freq, gain_mes, phase_mes, gain_ch1 = BS.interface.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
mean_gain = np.mean(gain_ch1)
mean_current = mean_gain/load
max_current = amp * 2.2/low_gain_max
max_current = max_current*(1+tolerance/100)		#include tolerance
min_current = amp * 2.2/low_gain_min
min_current = min_current*(1-tolerance/100)		#include tolerance
if (mean_current>max_current):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on current source')
if (mean_current<min_current):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on current source')


BS.set_current_excitation(coupling = 'DC', differential_stim = True,DC_feedback = False,High_gain = True)
BS.set_recording_voltage(coupling = 'DC', gain = 1)
BS.set_2_points_config()
BS.set_config()
BS.interface.configure_network_analyser()
vrange = round(amp,2)
freq, gain_mes, phase_mes, gain_ch1 = BS.interface.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
mean_gain = np.mean(gain_ch1)
mean_current = mean_gain/load
max_current = amp * 2.2/high_gain_max
max_current = max_current*(1+tolerance/100)		#include tolerance
min_current = amp * 2.2/high_gain_min
min_current = min_current*(1-tolerance/100)		#include tolerance
if (mean_current>max_current):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on current source')
if (mean_current<min_current):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on current source')
BS.close()

print("DONE!")
print("Current source sucessfully pass all tests.")
