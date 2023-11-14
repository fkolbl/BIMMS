import bimms as bm
import numpy as np

print('======== TIA test ========')
print('Connect a 1k resistor between STIM+ and STIM-')
input('- Press a Key when ready')

BS = bm.BIMMS()
BS.excitation_sources("INTERNAL")
BS.excitation_mode("P_EIS")
BS.wire_mode("2_WIRE")
BS.recording_mode("I")
BS.excitation_signaling_mode("SE")
BS.recording_signaling_mode("AUTO")
BS.excitation_coupling("DC")
BS.G_EIS_gain = "LOW"
BS.IRO_gain = 1
BS.VRO_gain = 1
BS.DC_feedback = False
BS.set_config()


print("Test offset TIA ...")

max_offset = 1
BS.readout_coupling("DC")
BS.excitation_signaling_mode("SE")
offset_DC = bm.Measure_Offset(BS = BS,channel = 2)
print("Measured TIA DC-SE offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value on TIA')

BS.readout_coupling("AC")
BS.excitation_signaling_mode("SE")
max_offset = 1
offset_DC = bm.Measure_Offset(BS = BS,channel = 2)
print("Measured TIA AC-SE offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value on TIA')

BS.readout_coupling("DC")
BS.excitation_signaling_mode("DIFF")
max_offset = 1
offset_DC = bm.Measure_Offset(BS = BS,channel = 2)
print("Measured TIA DC-DIFF offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value on TIA')

BS.readout_coupling("AC")
BS.excitation_signaling_mode("DIFF")
max_offset = 1
offset_DC = bm.Measure_Offset(BS = BS,channel = 2)
print("Measured TIA AC-DIFF offset: " +str(np.round(offset_DC,6)) +'V')
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
gain_TIA = 100

BS.readout_coupling("DC")
BS.excitation_signaling_mode("SE")
BS.recording_mode("BOTH")

BS.set_config()
BS.interface.configure_network_analyser()
vrange = round(amp,2)
freq, gain_mes, phase_mes, gain_ch1 = BS.interface.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
mean_r = np.mean(gain_mes)*gain_TIA
error = 100*(np.abs(mean_r-load)/load)
print("Measured R (TIA DC-SE): " +str(np.round(mean_r,6)) +'Ohms')
if (np.abs(error)>tolerance):
	BS.close()
	raise ValueError('Excessive error on measured resistor. Check TIA')

BS.excitation_signaling_mode("DIFF")
BS.set_config()
BS.interface.configure_network_analyser()
vrange = round(amp,2)
freq, gain_mes, phase_mes, gain_ch1 = BS.interface.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
mean_r = np.mean(gain_mes)*gain_TIA
error = 100*(np.abs(mean_r-load)/load)
print("Measured R (TIA DC-DIFF): " +str(np.round(mean_r,6)) +'Ohms')
if (np.abs(error)>tolerance):
	BS.close()
	raise ValueError('Excessive error on measured resistor. Check TIA')

BS.close()

print("DONE!")
print("TIA sucessfully pass all tests.")
