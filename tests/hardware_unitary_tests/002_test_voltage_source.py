import bimms as bm
import time
import numpy as np
import matplotlib.pyplot as plt

print('======== Voltage source test ========')
print('Unplug any connected wire/load')
input('- Press a Key when ready')

BS = bm.BIMMS()

#MEASURE OFFSET CH1
gain_IA = 1
acqu_duration = 1.0
max_offset = 1.0


print("Test offset voltage source ...")
BS.set_voltage_excitation(coupling = 'DC', differential_stim = False)
BS.set_2_points_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on voltage source')
BS.set_voltage_excitation(coupling = 'AC', differential_stim = False)
BS.set_2_points_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on voltage source')
BS.set_voltage_excitation(coupling = 'DC', differential_stim = True)
BS.set_2_points_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on voltage source')
BS.set_voltage_excitation(coupling = 'AC', differential_stim = True)
BS.set_2_points_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on voltage source')

print("DONE!")

print("Test gain voltage source ...")

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
tolerance = 5 #5% tolerance on measured gain
gain_SE = 1.1
gain_DIFF = 2.2
####################################################

BS.set_voltage_excitation(coupling = 'DC', differential_stim = False)
BS.set_recording_voltage(coupling = 'DC', gain = gain_IA)
BS.set_2_points_config()
BS.set_config()
BS.interface.configure_network_analyser()
vrange = round(amp  * gain_SE*1.5,2)
freq, gain_mes, phase_mes, gain_ch1 = BS.interface.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
mean_gain = np.mean(gain_ch1)
error = 100*np.abs(mean_gain-gain_SE)/gain_SE
if (error>tolerance):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on voltage source')

BS.set_voltage_excitation(coupling = 'DC', differential_stim = True)
BS.set_recording_voltage(coupling = 'DC', gain = gain_IA)
BS.set_2_points_config()
BS.set_config()
BS.interface.configure_network_analyser()
vrange = round(amp  * gain_DIFF*1.5,2)
freq, gain_mes, phase_mes, gain_ch1 = BS.interface.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
mean_gain = np.mean(gain_ch1)
error = 100*np.abs(mean_gain-gain_DIFF)/gain_SE
if (error>tolerance):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on voltage source')

BS.close()

print("DONE!")
print("Voltage source sucessfully pass all tests.")