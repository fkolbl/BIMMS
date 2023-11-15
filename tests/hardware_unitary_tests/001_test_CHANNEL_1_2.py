import bimms as bm
import numpy as np

test_ch1 = True
test_ch2 = True

BS = bm.BIMMS()

if (test_ch1):
	print('======== Channel 1 Test ========')
	print('- Connect CH1 + to AWG1')
	print('- Connect CH1 - to GND')
	input('- Press a Key when ready')

	#MEASURE OFFSET CH1
	gain_IA = 1
	acqu_duration = 1.0
	max_offset = 1.0

	print("Test offset Channel 1...")

	offset_DC = bm.Measure_Offset(BS = BS,channel = 1)
	print("Measured DC offset: " +str(np.round(offset_DC,6)) +'V')
	if (np.abs(offset_DC)>max_offset):
		BS.close()
		raise ValueError('Excessive DC offset value in measured on Channel 1')
	offset_AC = bm.Measure_Offset(BS = BS,channel = 1,coupling = 'AC')
	print("Measured AC offset: " +str(np.round(offset_AC,6)) +'V')
	if (np.abs(offset_DC)>max_offset):
		BS.close()
		raise ValueError('Excessive AC offset value in measured on Channel 1')

	print("Test gain Channel 1...")
	gain_array_IA = np.array([1,2,4,5,10,20,25,50,100])
	tol_gain = 1 #1% tolerance on measured gain to pass
	amp_AWG_max = 1
	max_IA_output = 1
	fmin = 100
	fmax = 100e3
	offset = 0
	n_pts = 20
	settling_time = 0.01
	NPeriods = 8
	BS.set_STM32_idle()
	BS.set_recording_channel_1(coupling = 'DC', gain = gain_IA)
	BS.set_config()
	BS.ad2.configure_network_analyser()
	for idx in range (len(gain_array_IA)):
		gain_IA = gain_array_IA [idx]
		print('Gain IA: ',gain_IA,'V/V')
		amp_awg = max_IA_output/gain_IA
		print('AWG Amplitude: ',amp_awg,'V')
		BS.set_gain_IA(channel=1, gain=gain_IA)
		vrange = round(amp_awg * gain_IA * 1.5,2)
		freq, gain_mes, phase_mes, gain_ch1 = BS.ad2.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp_awg,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
		mean_gain = np.mean(gain_ch1)
		error = 100*np.abs(mean_gain-gain_IA)/gain_IA
		print("Measured GAIN: " +str(np.round(mean_gain,6)) +'V/V')
		if (error>tol_gain):
			BS.close()
			raise ValueError('ERROR: Failed to measure expected gain on Channel 1')
	print("Channel 1 sucessfully all pass tests.")


if test_ch2:
	print('======== Channel 2 Test ========')
	print('- Disconnect CH1 + to AWG1')
	print('- Disconnect CH1 - to GND')
	print('- Connect Channel 2 + to AWG1')
	print('- Connect Channel 2 - to GND')
	input('- Press a Key when ready')

	#MEASURE OFFSET CH2
	gain_IA = 1
	acqu_duration = 1.0
	max_offset = 1.0

	print("Test offset Channel 2...")
	offset_DC = bm.Measure_Offset(BS = BS,channel = 2)
	print("Measured DC offset: " +str(np.round(offset_DC,6)) +'V')
	if (np.abs(offset_DC)>max_offset):
		BS.close()
		raise ValueError('Excessive DC offset value in measured on Channel 2')

	offset_AC = bm.Measure_Offset(BS = BS,channel = 2,coupling = 'AC')
	print("Measured AC offset: " +str(np.round(offset_AC,6)) +'V')
	if (np.abs(offset_DC)>max_offset):
		BS.close()
		raise ValueError('Excessive AC offset value in measured on Channel 2')

	print("Test gain Channel 2...")
	gain_array_IA = np.array([1,2,4,5,10,20,25,50,100])
	tol_gain = 1 #1% tolerance on measured gain to pass
	amp_AWG_max = 1
	max_IA_output = 1
	fmin = 100
	fmax = 100e3
	offset = 0
	n_pts = 20
	settling_time = 0.01
	NPeriods = 8
	BS.set_STM32_idle()
	BS.set_recording_channel_2(coupling = 'DC', gain = gain_IA)
	BS.set_config()
	BS.ad2.configure_network_analyser()
	for idx in range (len(gain_array_IA)):
		gain_IA = gain_array_IA [idx]
		print('Gain IA: ',gain_IA,'V/V')
		amp_awg = max_IA_output/gain_IA
		print('AWG Amplitude: ',amp_awg,'V')
		BS.set_gain_IA(channel=2, gain=gain_IA)
		vrange = round(amp_awg * gain_IA * 1.5,2)
		freq, gain_mes, phase_mes, gain_ch1 = BS.ad2.bode_measurement(fmin, fmax, n_points = n_pts, dB = False,offset=offset, deg = True, amp = amp_awg,settling_time=settling_time, Nperiods = NPeriods, Vrange_CH1 = vrange)
		gain_ch2 = gain_ch1/gain_mes
		mean_gain = np.mean(gain_ch2)
		error = 100*np.abs(mean_gain-gain_IA)/gain_IA
		print("Measured GAIN: " +str(np.round(mean_gain,6)) +'V/V')
		if (error>tol_gain):
			BS.close()
			raise ValueError('ERROR: Failed to measure expected gain on Channel 2')
	print("Channel 2 sucessfully all pass tests.")


BS.close()