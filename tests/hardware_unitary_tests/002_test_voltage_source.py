import bimms as bm
import numpy as np
import matplotlib.pyplot as plt

print('======== Voltage source test ========')
print('Unplug any connected wire/load')
input('- Press a Key when ready')

ignore_exception = False
test_offset = True
test_single_freq = True
test_bode = True

BS = bm.BIMMS()
BS.config_mode("TEST")


BS.test_config.waveform_gen("INTERNAL")
BS.test_config.excitation_source("VOLTAGE")
BS.test_config.I_source_gain("HIGH")
BS.test_config.wire_mode("2_WIRE")
BS.test_config.excitation_signaling_mode("SE")
BS.test_config.excitation_coupling("DC")
BS.test_config.DC_feedback(False)
BS.test_config.Enable_Isource(True)

BS.test_config.CHx_to_Scopex("CH1")
BS.test_config.CH1_coupling("DC")
BS.test_config.CH2_coupling("DC")
BS.test_config.TIA_coupling("DC")
BS.test_config.connect_TIA(False)
BS.test_config.TIA_to_CH2(False)
BS.test_config.TIA_NEG("GND")
BS.test_config.CH1_gain(1)
BS.test_config.CH2_gain(1)



#offset measure 
acqu_duration = 1.0
max_offset = 1.0
N_avg = 2

#single frequency measure
freq_AWG = 1e3
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
    print("===== Offset Voltage Source - SE-DC Coupling =====")
    BS.test_config.excitation_coupling("DC")
    BS.test_config.excitation_signaling_mode("SE")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1_raw = results['ch1_offset']
    offset_ch1 = np.round(offset_ch1_raw*1000,3)
    print("Offset: "+str(offset_ch1)+"mV")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCVS_SE_DC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset Voltage Source - SE-AC Coupling =====")
    BS.test_config.excitation_coupling("AC")
    BS.test_config.excitation_signaling_mode("SE")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1_raw = results['ch1_offset']
    offset_ch1 = np.round(offset_ch1_raw*1000,3)
    print("Offset: "+str(offset_ch1)+"mV")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCVS_SE_AC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset Voltage Source - DIFF-DC Coupling =====")
    BS.test_config.excitation_coupling("DC")
    BS.test_config.excitation_signaling_mode("DIFF")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1_raw = results['ch1_offset']
    offset_ch1 = np.round(offset_ch1_raw*1000,3)
    print("Offset: "+str(offset_ch1)+"mV")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCVS_DIFF_DC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset Voltage Source - DIFF-AC Coupling =====")
    BS.test_config.excitation_coupling("AC")
    BS.test_config.excitation_signaling_mode("DIFF")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1_raw = results['ch1_offset']
    offset_ch1 = np.round(offset_ch1_raw*1000,3)
    print("Offset: "+str(offset_ch1)+"mV")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCVS_DIFF_AC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")


if (test_single_freq):
    plt.figure()
    print("===== Single Frequency - SE-DC Coupling =====")
    BS.test_config.excitation_coupling("DC")
    BS.test_config.excitation_signaling_mode("SE")
    m1 = bm.TemporalSingleFrequency(freq = freq_AWG,Nperiod = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = results['chan1_raw']
    t = results['t']
    plt.plot(t,ch1, label = "SE-DC")

    print("===== Single Frequency - SE-AC Coupling =====")
    BS.test_config.excitation_coupling("AC")
    BS.test_config.excitation_signaling_mode("SE")
    m1 = bm.TemporalSingleFrequency(freq = freq_AWG,Nperiod = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = results['chan1_raw']
    t = results['t']
    plt.plot(t,ch1, label = "SE-AC")

    print("===== Single Frequency - DIFF-DC Coupling =====")
    BS.test_config.excitation_coupling("DC")
    BS.test_config.excitation_signaling_mode("DIFF")
    m1 = bm.TemporalSingleFrequency(freq = freq_AWG,Nperiod = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = results['chan1_raw']
    t = results['t']
    plt.plot(t,ch1, label = "DIFF-DC")

    print("===== Single Frequency - DIFF-AC Coupling =====")
    BS.test_config.excitation_coupling("AC")
    BS.test_config.excitation_signaling_mode("DIFF")
    m1 = bm.TemporalSingleFrequency(freq = freq_AWG,Nperiod = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = results['chan1_raw']
    t = results['t']
    plt.plot(t,ch1, label = "DIFF-AC")
    plt.legend()
    plt.savefig('./hardware_unitary_tests/figures_hardware/002_VCVS_temporal.png')
    plt.close('all')

if (test_bode):
    plt.figure()
    print("===== Bode - SE-DC Coupling =====")
    BS.test_config.excitation_coupling("DC")
    BS.test_config.excitation_signaling_mode("SE")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "SE-DC")
    mes_gain = mag_ch1[0]
    print("Voltage Source Gain: "+ str(np.round(mes_gain,3))+ 'V/V')
    if not (bm.in_tol(mes_gain,bm.cst.Vsource_SE_G_default,bm.cst.VCVS_SE_DC_gain_tol)):
        if not (ignore_exception):
            raise Exception("Measured VCVS gain out of tol")

    print("===== Bode - SE-AC Coupling =====")
    BS.test_config.excitation_coupling("AC")
    BS.test_config.excitation_signaling_mode("SE")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "SE-AC")
    mes_gain = mag_ch1[0]
    print("Voltage Source Gain: "+ str(np.round(mes_gain,3))+ 'V/V')
    if not (bm.in_tol(mes_gain,bm.cst.Vsource_SE_G_default,bm.cst.VCVS_SE_AC_gain_tol)):
        if not (ignore_exception):
            raise Exception("Measured VCVS gain out of tol")

    print("===== Bode - DIFF-DC Coupling =====")
    BS.test_config.excitation_coupling("DC")
    BS.test_config.excitation_signaling_mode("DIFF")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "DIFF-DC")
    mes_gain = mag_ch1[0]
    print("Voltage Source Gain: "+ str(np.round(mes_gain,3))+ 'V/V')
    if not (bm.in_tol(mes_gain,bm.cst.Vsource_DIFF_G_default,bm.cst.VCVS_DIFF_DC_gain_tol)):
        if not (ignore_exception):
            raise Exception("Measured VCVS gain out of tol")

    print("===== Bode - DIFF-AC Coupling =====")
    BS.test_config.excitation_coupling("AC")
    BS.test_config.excitation_signaling_mode("DIFF")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "DIFF-AC")
    mes_gain = mag_ch1[0]
    print("Voltage Source Gain: "+ str(np.round(mes_gain,3))+ 'V/V')
    if not (bm.in_tol(mes_gain,bm.cst.Vsource_DIFF_G_default,bm.cst.VCVS_DIFF_AC_gain_tol)):
        if not (ignore_exception):
            raise Exception("Measured VCVS gain out of tol")


    plt.legend()
    plt.savefig('./hardware_unitary_tests/figures_hardware/002_VCVS_bode.png')
    plt.close('all')

