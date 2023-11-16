import bimms as bm
import numpy as np
import matplotlib.pyplot as plt

print('======== Current source test ========')
print('Connect a 1k resistor between STIM+ and STIM-')
input('- Press a Key when ready')

test_offset = False
test_single_freq = False
test_bode = True

BS = bm.BIMMS()
BS.config_mode("TEST")

BS.test_config.waveform_gen("INTERNAL")
BS.test_config.excitation_source("CURRENT")
BS.test_config.I_source_gain("LOW")
BS.test_config.wire_mode("2_WIRE")
BS.test_config.excitation_signaling_mode("SE")
BS.test_config.excitation_coupling("DC")
BS.test_config.DC_feedback(False)
BS.test_config.Enable_Isource(True)

BS.test_config.CHx_to_Scopex("CH1")
BS.test_config.CH1_coupling("DC")
BS.test_config.CH2_coupling("DC")
BS.test_config.TIA_coupling("DC")
BS.test_config.TIA_to_CH2(False)
BS.test_config.TIA_NEG("GND")
BS.test_config.CH1_gain(1)
BS.test_config.CH2_gain(1)

Rload = 1000

def v_2_uA (val):
	return(1e6*val/Rload)


#offset measure 
acqu_duration = 1.0
max_offset = 1.0
N_avg = 2

#single frequency measure
freq = 1e3
n_period = 5
amp_AWG = 0.1
BS.test_config.AWG_amp(amp_AWG)

#bode 
fmin = 1e3
fmax = 1e6
n_pts=101
settling_time=0.001
NPeriods=8

if (test_offset):
	print("===== Offset Current Source - LG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.Offset(acqu_duration,N_avg)
	BS.attach_measure(m1)
	results = BS.measure()
	offset_ch1 = np.round(results['ch1_offset']*1000,3)
	print("Offset: "+str(v_2_uA(offset_ch1))+"µA")

	print("===== Offset Current Source - LG-SE-AC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.Offset(acqu_duration,N_avg)
	BS.attach_measure(m1)
	results = BS.measure()
	offset_ch1 = np.round(results['ch1_offset']*1000,3)
	print("Offset: "+str(v_2_uA(offset_ch1))+"µA")

	print("===== Offset Current Source - LG-DIFF-DC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.Offset(acqu_duration,N_avg)
	BS.attach_measure(m1)
	results = BS.measure()
	offset_ch1 = np.round(results['ch1_offset']*1000,3)
	print("Offset: "+str(v_2_uA(offset_ch1))+"µA")

	print("===== Offset Current Source - LG-DIFF-AC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.Offset(acqu_duration,N_avg)
	BS.attach_measure(m1)
	results = BS.measure()
	offset_ch1 = np.round(results['ch1_offset']*1000,3)
	print("Offset: "+str(v_2_uA(offset_ch1))+"µA")

	print("===== Offset Current Source - HG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.Offset(acqu_duration,N_avg)
	BS.attach_measure(m1)
	results = BS.measure()
	offset_ch1 = np.round(results['ch1_offset']*1000,3)
	print("Offset: "+str(v_2_uA(offset_ch1))+"µA")

	print("===== Offset Current Source - HG-SE-AC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.Offset(acqu_duration,N_avg)
	BS.attach_measure(m1)
	results = BS.measure()
	offset_ch1 = np.round(results['ch1_offset']*1000,3)
	print("Offset: "+str(v_2_uA(offset_ch1))+"µA")

	print("===== Offset Current Source - HG-DIFF-DC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.Offset(acqu_duration,N_avg)
	BS.attach_measure(m1)
	results = BS.measure()
	offset_ch1 = np.round(results['ch1_offset']*1000,3)
	print("Offset: "+str(v_2_uA(offset_ch1))+"µA")

	print("===== Offset Current Source - HG-DIFF-AC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.Offset(acqu_duration,N_avg)
	BS.attach_measure(m1)
	results = BS.measure()
	offset_ch1 = np.round(results['ch1_offset']*1000,3)
	print("Offset: "+str(v_2_uA(offset_ch1))+"µA")


if (test_single_freq):
	plt.figure()
	print("===== Single Frequency - LG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
	BS.attach_measure(m1)
	results = BS.measure()
	ch1 = v_2_uA(results['chan1'])
	t = results['t']
	plt.plot(t,ch1, label = "LG-SE-DC")

	print("===== Single Frequency - LG-SE-AC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
	BS.attach_measure(m1)
	results = BS.measure()
	ch1 = v_2_uA(results['chan1'])
	t = results['t']
	plt.plot(t,ch1, label = "LG-SE-AC")

	print("===== Single Frequency - LG-DIFF-DC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
	BS.attach_measure(m1)
	results = BS.measure()
	ch1 = v_2_uA(results['chan1'])
	t = results['t']
	plt.plot(t,ch1, label = "LG-DIFF-DC")

	print("===== Single Frequency - LG-DIFF-AC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
	BS.attach_measure(m1)
	results = BS.measure()
	ch1 = v_2_uA(results['chan1'])
	t = results['t']
	plt.plot(t,ch1, label = "LG-DIFF-DC")

	print("===== Single Frequency - HG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
	BS.attach_measure(m1)
	results = BS.measure()
	ch1 = v_2_uA(results['chan1'])
	t = results['t']
	plt.plot(t,ch1, label = "HG-SE-DC")

	print("===== Single Frequency - HG-SE-AC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
	BS.attach_measure(m1)
	results = BS.measure()
	ch1 = v_2_uA(results['chan1'])
	t = results['t']
	plt.plot(t,ch1, label = "HG-SE-AC")

	print("===== Single Frequency - HG-DIFF-DC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
	BS.attach_measure(m1)
	results = BS.measure()
	ch1 = v_2_uA(results['chan1'])
	t = results['t']
	plt.plot(t,ch1, label = "HG-DIFF-DC")

	print("===== Single Frequency - HG-DIFF-AC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
	BS.attach_measure(m1)
	results = BS.measure()
	ch1 = v_2_uA(results['chan1'])
	t = results['t']
	plt.plot(t,ch1, label = "HG-DIFF-AC")


if (test_bode):
	plt.figure()
	print("===== Bode - LG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
	BS.attach_measure(m1)
	results = BS.measure()
	mag_ch1 = results['mag_ch1']
	freq = results['freq']
	plt.semilogx(freq,mag_ch1, label = "SE-DC")
	mes_gain = mag_ch1[0]
	print("Current Source Gain: "+ str(np.round(v_2_uA(mes_gain),3))+ 'uA/V')

	print("===== Bode - LG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
	BS.attach_measure(m1)
	results = BS.measure()
	mag_ch1 = results['mag_ch1']
	freq = results['freq']
	plt.semilogx(freq,mag_ch1, label = "SE-DC")
	mes_gain = mag_ch1[0]
	print("Current Source Gain: "+ str(np.round(v_2_uA(mes_gain),3))+ 'uA/V')

	print("===== Bode - LG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
	BS.attach_measure(m1)
	results = BS.measure()
	mag_ch1 = results['mag_ch1']
	freq = results['freq']
	plt.semilogx(freq,mag_ch1, label = "SE-DC")
	mes_gain = mag_ch1[0]
	print("Current Source Gain: "+ str(np.round(v_2_uA(mes_gain),3))+ 'uA/V')

	print("===== Bode - LG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("LOW")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
	BS.attach_measure(m1)
	results = BS.measure()
	mag_ch1 = results['mag_ch1']
	freq = results['freq']
	plt.semilogx(freq,mag_ch1, label = "SE-DC")
	mes_gain = mag_ch1[0]
	print("Current Source Gain: "+ str(np.round(v_2_uA(mes_gain),3))+ 'uA/V')

	print("===== Bode - HG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
	BS.attach_measure(m1)
	results = BS.measure()
	mag_ch1 = results['mag_ch1']
	freq = results['freq']
	plt.semilogx(freq,mag_ch1, label = "SE-DC")
	mes_gain = mag_ch1[0]
	print("Current Source Gain: "+ str(np.round(v_2_uA(mes_gain),3))+ 'uA/V')

	print("===== Bode - HG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("SE")
	m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
	BS.attach_measure(m1)
	results = BS.measure()
	mag_ch1 = results['mag_ch1']
	freq = results['freq']
	plt.semilogx(freq,mag_ch1, label = "SE-DC")
	mes_gain = mag_ch1[0]
	print("Current Source Gain: "+ str(np.round(v_2_uA(mes_gain),3))+ 'uA/V')

	print("===== Bode - HG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("DC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
	BS.attach_measure(m1)
	results = BS.measure()
	mag_ch1 = results['mag_ch1']
	freq = results['freq']
	plt.semilogx(freq,mag_ch1, label = "SE-DC")
	mes_gain = mag_ch1[0]
	print("Current Source Gain: "+ str(np.round(v_2_uA(mes_gain),3))+ 'uA/V')

	print("===== Bode - HG-SE-DC Coupling =====")
	BS.test_config.I_source_gain("HIGH")
	BS.test_config.excitation_coupling("AC")
	BS.test_config.excitation_signaling_mode("DIFF")
	m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
	BS.attach_measure(m1)
	results = BS.measure()
	mag_ch1 = results['mag_ch1']
	freq = results['freq']
	plt.semilogx(freq,mag_ch1, label = "SE-DC")
	mes_gain = mag_ch1[0]
	print("Current Source Gain: "+ str(np.round(v_2_uA(mes_gain),3))+ 'uA/V')



	plt.show()