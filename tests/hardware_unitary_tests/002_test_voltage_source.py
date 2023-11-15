import bimms as bm
import numpy as np

print('======== Voltage source test ========')
print('Unplug any connected wire/load')
input('- Press a Key when ready')

BS = bm.BIMMS()
BS.config.excitation_sources("INTERNAL")
BS.config.excitation_mode("P_EIS")
BS.config.wire_mode("2_WIRE")
BS.config.readout_coupling("DC")
BS.config.recording_mode("V")
BS.config.recording_signaling_mode("AUTO")

#MEASURE OFFSET CH1
gain_IA = 1
acqu_duration = 1.0
max_offset = 1.0

BS.config.excitation_signaling_mode("SE")
BS.config.excitation_coupling("DC")
BS.set_config()
print("Test offset voltage source ...")
offset_DC = bm.Measure_Offset(BS = BS,channel = 1,Vrange = 1)
print("Measured DC-SE offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on voltage source')


BS.config.excitation_signaling_mode("SE")
BS.config.excitation_coupling("AC")
BS.set_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1,Vrange = 1)
print("Measured AC-SE offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on voltage source')

BS.config.excitation_signaling_mode("DIFF")
BS.config.excitation_coupling("DC")
BS.set_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1,Vrange = 1)
print("Measured DC-DIFF offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on voltage source')


BS.config.excitation_signaling_mode("DIFF")
BS.config.excitation_coupling("AC")
BS.set_config()
offset_DC = bm.Measure_Offset(BS = BS,channel = 1,Vrange = 1)
print("Measured AC-DIFF offset: " +str(np.round(offset_DC,6)) +'V')
if (np.abs(offset_DC)>max_offset):
	BS.close()
	raise ValueError('Excessive offset value in measured on voltage source')

print("DONE!")

print("Test gain voltage source ...")
################
## Parameters ##
################
amp = 1
fmin = 100
fmax = 100e3
offset = 0
n_pts = 20
settling_time = 0.01
NPeriods = 16
tolerance = 5 #5% tolerance on measured gain
gain_SE = 1.1
gain_DIFF = 2.2
gain_IA = 1
####################################################

BS.config.excitation_sources("INTERNAL")
BS.config.excitation_mode("P_EIS")
BS.config.wire_mode("2_WIRE")
BS.config.readout_coupling("DC")
BS.config.recording_mode("V")
BS.config.recording_signaling_mode("AUTO")
BS.config.excitation_signaling_mode("SE")
BS.config.excitation_coupling("DC")
BS.set_config()

BS.ad2.configure_network_analyser()
vrange = round(amp  * gain_SE*1.5,2)
freq, gain_mes, phase_mes, gain_ch1 = BS.ad2.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
mean_gain = np.mean(gain_ch1)
error = 100*np.abs(mean_gain-gain_SE)/gain_SE
print("Measured SE GAIN: " +str(np.round(mean_gain,6)) +'V/V')
if (error>tolerance):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on voltage source')

BS.config.excitation_signaling_mode("DIFF")
BS.set_config()
BS.ad2.configure_network_analyser()
vrange = round(amp  * gain_DIFF*1.5,2)
freq, gain_mes, phase_mes, gain_ch1 = BS.ad2.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
mean_gain = np.mean(gain_ch1)
error = 100*np.abs(mean_gain-gain_DIFF)/gain_SE
print("Measured Diff GAIN: " +str(np.round(mean_gain,6)) +'V/V')
if (error>tolerance):
	BS.close()
	raise ValueError('ERROR: Failed to measure expected gain on voltage source')

BS.close()

print("DONE!")
print("Voltage source sucessfully pass all tests.")