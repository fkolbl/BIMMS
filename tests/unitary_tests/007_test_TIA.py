import bimms as bm
import time
import numpy as np
import matplotlib.pyplot as plt

print('======== TIA test ========')
print('Plug a 1k resistor')
input('- Press a Key when ready')

BS = bm.BIMMS()
BS.set_STM32_idle()
BS.set_current_excitation(coupling = 'DC', differential_stim = False)
BS.set_recording_current(differential = False, coupling = 'DC', gain = 1)
BS.set_recording_voltage(coupling = 'DC', gain = 1)
BS.set_2_points_config()
BS.set_config()

max_offset = 1
print("Test offset TIA ...")
offset_DC = bm.Measure_Offset(BS = BS,channel = 2)
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value on TIA')


print("DONE!")


print("Test gain TIA ...")

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
load = 1000
tolerance = 10 #tolerance on measured resistor
gain_TIA = 1000

BS.set_voltage_excitation(coupling = 'DC', differential_stim = False)
BS.set_recording_current(differential = False, coupling = 'DC', gain = 1)
BS.set_recording_voltage(coupling = 'DC', gain = 1)
BS.set_2_points_config()
BS.set_config()
BS.interface.configure_network_analyser()
vrange = round(amp,2)
freq, gain_mes, phase_mes, gain_ch1 = BS.interface.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
mean_r = np.mean(gain_mes)*gain_TIA
error = 100*(np.abs(mean_r-load)/load)
if (np.abs(error)>tolerance):
	BS.close()
	raise ValueError('Excessive error on measured resistor. Check TIA')

BS.set_voltage_excitation(coupling = 'DC', differential_stim = True)
BS.set_recording_current(differential = True, coupling = 'DC', gain = 1)
BS.set_recording_voltage(coupling = 'DC', gain = 1)
BS.set_2_points_config()
BS.set_config()
BS.interface.configure_network_analyser()
vrange = round(amp,2)
freq, gain_mes, phase_mes, gain_ch1 = BS.interface.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
mean_r = np.mean(gain_mes)*gain_TIA
error = 100*(np.abs(mean_r-load)/load)
if (np.abs(error)>tolerance):
	BS.close()
	raise ValueError('Excessive error on measured resistor. Check TIA')

BS.close()

print("DONE!")
print("TIA sucessfully pass all tests.")
