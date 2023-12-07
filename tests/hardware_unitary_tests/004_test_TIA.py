import bimms as bm
import numpy as np
import matplotlib.pyplot as plt

print('======== TIA test ========')
print('Connect a 1k resistor between STIM+ and STIM-')
input('- Press a Key when ready')

r_l = 1000

ignore_exception = False
test_offset = False
test_single_freq = False
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

BS.test_config.CHx_to_Scopex("BOTH")
BS.test_config.CH1_coupling("DC")
BS.test_config.CH2_coupling("DC")
BS.test_config.TIA_coupling("DC")
BS.test_config.connect_TIA(True)
BS.test_config.TIA_to_CH2(True)
BS.test_config.TIA_NEG("GND")
BS.test_config.CH1_gain(1)
BS.test_config.CH2_gain(1)

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
    print("===== Offset TIA - SE-DC Coupling =====")
    BS.test_config.TIA_coupling("DC")
    BS.test_config.TIA_NEG("GND")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_TIA_raw = results['ch2_offset']
    offset_TIA = np.round(offset_TIA_raw*1000,3)
    print("Offset: "+str(offset_TIA)+"mV")
    if not (bm.in_range(offset_TIA_raw,bm.cst.max_TIA_SE_DC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset TIA - SE-AC Coupling =====")
    BS.test_config.TIA_coupling("AC")
    BS.test_config.TIA_NEG("GND")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_TIA_raw = results['ch2_offset']
    offset_TIA = np.round(offset_TIA_raw*1000,3)
    print("Offset: "+str(offset_TIA)+"mV")
    if not (bm.in_range(offset_TIA_raw,bm.cst.max_TIA_SE_AC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset TIA - DIFF-DC Coupling =====")
    BS.test_config.TIA_coupling("DC")
    BS.test_config.excitation_signaling_mode("DIFF")
    BS.test_config.TIA_NEG("Vneg")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_TIA_raw = results['ch2_offset']
    offset_TIA = np.round(offset_TIA_raw*1000,3)
    print("Offset: "+str(offset_TIA)+"mV")
    if not (bm.in_range(offset_TIA_raw,bm.cst.max_TIA_DIFF_DC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset TIA - DIFF-AC Coupling =====")
    BS.test_config.TIA_coupling("AC")
    BS.test_config.excitation_signaling_mode("DIFF")
    BS.test_config.TIA_NEG("Vneg")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_TIA_raw = results['ch2_offset']
    offset_TIA = np.round(offset_TIA_raw*1000,3)
    print("Offset: "+str(offset_TIA)+"mV")
    if not (bm.in_range(offset_TIA_raw,bm.cst.max_TIA_DIFF_AC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

if (test_single_freq):
    plt.figure()
    print("===== Single Frequency - SE-DC Coupling =====")
    BS.test_config.excitation_signaling_mode("SE")
    BS.test_config.TIA_coupling("DC")
    BS.test_config.TIA_NEG("GND")
    m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch2 = (results['chan2_raw'])
    t = results['t']
    plt.plot(t,ch2, label = "SE-DC")

    print("===== Single Frequency - SE-AC Coupling =====")
    BS.test_config.excitation_signaling_mode("SE")
    BS.test_config.TIA_coupling("AC")
    BS.test_config.TIA_NEG("GND")
    m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch2 = (results['chan2_raw'])
    t = results['t']
    plt.plot(t,ch2, label = "SE-AC")

    print("===== Single Frequency - DIFF-DC Coupling =====")
    BS.test_config.excitation_signaling_mode("DIFF")
    BS.test_config.TIA_coupling("DC")
    BS.test_config.TIA_NEG("Vneg")
    m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch2 = (results['chan2_raw'])
    t = results['t']
    plt.plot(t,ch2, label = "DIFF-DC")

    print("===== Single Frequency - DIFF-AC Coupling =====")
    BS.test_config.excitation_signaling_mode("DIFF")
    BS.test_config.TIA_coupling("AC")
    BS.test_config.TIA_NEG("Vneg")
    m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch2 = (results['chan2_raw'])
    t = results['t']
    plt.plot(t,ch2, label = "DIFF-AC")        
    plt.savefig('./hardware_unitary_tests/figures_hardware/004_TIA_temporal.png')
    plt.close('all')


if (test_bode):
    plt.figure()
    print("===== Bode - SE-DC Coupling =====")
    BS.test_config.excitation_signaling_mode("SE")
    BS.test_config.TIA_coupling("DC")
    BS.test_config.TIA_NEG("GND")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch2 = results['mag_ch2_raw']
    mag_current = results['mag_ch1_raw']/r_l
    G_TIA = mag_ch2/mag_current
    freq = results['freq']
    plt.semilogx(freq,G_TIA, label = "SE-DC")
    mes_gain = G_TIA[0]
    print("TIA Gain: "+ str(np.round((mes_gain),1))+ 'V/A')
    if not (bm.in_tol(mes_gain,bm.cst.TIA_gain_default,bm.cst.TIA_gain_tol)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")

    print("===== Bode - SE-AC Coupling =====")
    BS.test_config.excitation_signaling_mode("SE")
    BS.test_config.TIA_coupling("AC")
    BS.test_config.TIA_NEG("GND")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch2 = results['mag_ch2_raw']
    mag_current = results['mag_ch1_raw']/r_l
    G_TIA = mag_ch2/mag_current
    freq = results['freq']
    plt.semilogx(freq,G_TIA, label = "SE-AC")
    mes_gain = G_TIA[0]
    print("TIA Gain: "+ str(np.round((mes_gain),1))+ 'V/A')
    if not (bm.in_tol(mes_gain,bm.cst.TIA_gain_default,bm.cst.TIA_gain_tol)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")

    print("===== Bode - DIFF-DC Coupling =====")
    BS.test_config.excitation_signaling_mode("DIFF")
    BS.test_config.TIA_coupling("DC")
    BS.test_config.TIA_NEG("Vneg")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch2 = results['mag_ch2_raw']
    freq = results['freq']
    mag_current = results['mag_ch1_raw']/r_l
    G_TIA = mag_ch2/mag_current
    freq = results['freq']
    plt.semilogx(freq,G_TIA, label = "DIFF-DC")
    mes_gain = G_TIA[0]
    print("TIA Gain: "+ str(np.round((mes_gain),1))+ 'V/A')
    if not (bm.in_tol(mes_gain,bm.cst.TIA_gain_default,bm.cst.TIA_gain_tol)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")

    print("===== Bode - SE-AC Coupling =====")
    BS.test_config.excitation_signaling_mode("DIFF")
    BS.test_config.TIA_coupling("AC")
    BS.test_config.TIA_NEG("Vneg")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch2 = results['mag_ch2_raw']
    mag_current = results['mag_ch1_raw']/r_l
    G_TIA = mag_ch2/mag_current
    freq = results['freq']
    plt.semilogx(freq,G_TIA, label = "DIFF-AC")   
    mes_gain = G_TIA[0]
    print("TIA Gain: "+ str(np.round((mes_gain),1))+ 'V/A') 
    if not (bm.in_tol(mes_gain,bm.cst.TIA_gain_default,bm.cst.TIA_gain_tol)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")


    plt.savefig('./hardware_unitary_tests/figures_hardware/004_TIA_bode.png')
    plt.close('all')
