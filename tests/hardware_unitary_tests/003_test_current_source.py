import bimms as bm
import time
import numpy as np
import matplotlib.pyplot as plt

print('======== Current source test ========')
print('Connect a 1k resistor between STIM+ and STIM-')
input('- Press a Key when ready')

BS = bm.BIMMS()
BS.excitation_sources("INTERNAL")
BS.excitation_mode("G_EIS")
BS.wire_mode("2_WIRE")
BS.readout_coupling("DC")
BS.recording_mode("V")
BS.recording_signaling_mode("AUTO")

BS.G_EIS_gain = "LOW"
BS.IRO_gain = 1
BS.VRO_gain = 1
BS.DC_feedback = False


#MEASURE OFFSET CH1
acqu_duration = 1.0
max_offset = 1.0

print("Test offset current source ...")
BS.excitation_signaling_mode("SE")
BS.excitation_coupling("DC")
BS.set_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
print("Measured G_EIS DC-SE offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value on current source')

BS.excitation_coupling("AC")
BS.set_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
print("Measured G_EIS AC-SE offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')

BS.excitation_signaling_mode("DIFF")
BS.excitation_coupling("DC")
BS.set_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
print("Measured G_EIS DC-DIFF offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')

BS.excitation_coupling("AC")
BS.set_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
print("Measured G_EIS AC-DIFF offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')

BS.G_EIS_gain = "HIGH"
BS.excitation_coupling("DC")
BS.set_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
print("Measured G_EIS DC-DIFF (High-Gain) offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')

BS.G_EIS_gain = "HIGH"
BS.excitation_coupling("AC")
BS.set_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
print("Measured G_EIS AC-DIFF (High-Gain) offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')

BS.G_EIS_gain = "HIGH"
BS.excitation_coupling("AC")
BS.set_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
print("Measured G_EIS AC-DIFF (High-Gain, DC Feedback ON) offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')

BS.DC_feedback  = True
BS.excitation_signaling_mode = "SE"
BS.set_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
print("Measured G_EIS AC-SE (High-Gain, DC Feedback ON) offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on current source')
print("DONE!")

print("Test gain current source ...")
################
## Parameters ##
################
amp = 1
fmin = 100
fmax = 10e3
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

BS.DC_feedback  = False
BS.excitation_signaling_mode = "SE"
BS.G_EIS_gain = "LOW"
BS.excitation_coupling("DC")
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
print("Measured G_EIS DC-SE (LOW-Gain, DC Feedback OFF) GAIN: " +str(np.round(mean_gain,6)) +'A/V')
if (mean_current>max_current):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on current source')
if (mean_current<min_current):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on current source')


BS.G_EIS_gain = "HIGH"
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
print("Measured G_EIS DC-SE (HIGH-Gain, DC Feedback OFF) GAIN: " +str(np.round(mean_gain,6)) +'A/V')
if (mean_current>max_current):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on current source')
if (mean_current<min_current):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on current source')
print("DONE!")



BS.close()
print("Current source sucessfully pass all tests.")
