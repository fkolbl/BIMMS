import bimms as bm
import numpy as np
import matplotlib.pyplot as plt

print('======== Current source test ========')
print('Connect a 1k resistor between STIM+ and STIM-')
input('- Press a Key when ready')

ignore_exception = False 
test_offset = True
test_single_freq = True
test_bode = True

BS = bm.BIMMS()
BS.config_mode("MANUAL")

BS.manual_config.waveform_gen("INTERNAL")
BS.manual_config.excitation_source("CURRENT")
BS.manual_config.I_source_gain("LOW")
BS.manual_config.wire_mode("2_WIRE")
BS.manual_config.excitation_signaling_mode("SE")
BS.manual_config.excitation_coupling("DC")
BS.manual_config.DC_feedback(False)
BS.manual_config.Enable_Isource(True)

BS.manual_config.CHx_to_Scopex("CH1")
BS.manual_config.CH1_coupling("DC")
BS.manual_config.CH2_coupling("DC")
BS.manual_config.TIA_coupling("DC")
BS.manual_config.connect_TIA(True)
BS.manual_config.TIA_to_CH2(False)
BS.manual_config.TIA_NEG("GND")
BS.manual_config.CH1_gain(1)
BS.manual_config.CH2_gain(1)

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
BS.manual_config.AWG_amp(amp_AWG)

#bode 
fmin = 1e3
fmax = 1e6
n_pts=101
settling_time=0.001
nperiods=8


if (test_offset):
    print("===== Offset Current Source - LG-SE-DC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1_raw = v_2_uA(results['ch1_offset'])
    offset_ch1 = np.round(offset_ch1_raw,3)
    print("Offset: "+str(offset_ch1)+"µA")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCCS_SE_LG_DC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset Current Source - LG-SE-AC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1_raw = v_2_uA(results['ch1_offset'])
    offset_ch1 = np.round(offset_ch1_raw,3)
    print("Offset: "+str(offset_ch1)+"µA")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCCS_SE_LG_AC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset Current Source - LG-DIFF-DC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1_raw = v_2_uA(results['ch1_offset'])
    offset_ch1 = np.round(offset_ch1_raw,3)
    print("Offset: "+str(offset_ch1)+"µA")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCCS_DIFF_LG_DC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset Current Source - LG-DIFF-AC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1_raw = v_2_uA(results['ch1_offset'])
    offset_ch1 = np.round(offset_ch1_raw,3)
    print("Offset: "+str(offset_ch1)+"µA")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCCS_DIFF_LG_AC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset Current Source - HG-SE-DC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1_raw = v_2_uA(results['ch1_offset'])
    offset_ch1 = np.round(offset_ch1_raw,3)
    print("Offset: "+str(offset_ch1)+"µA")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCCS_SE_HG_DC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset Current Source - HG-SE-AC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1_raw = v_2_uA(results['ch1_offset'])
    offset_ch1 = np.round(offset_ch1_raw,3)
    print("Offset: "+str(offset_ch1)+"µA")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCCS_SE_HG_AC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset Current Source - HG-DIFF-DC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1 = np.round(results['ch1_offset']*1000,3)
    offset_ch1_raw = v_2_uA(results['ch1_offset'])
    offset_ch1 = np.round(offset_ch1_raw,3)
    print("Offset: "+str(offset_ch1)+"µA")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCCS_DIFF_HG_DC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")

    print("===== Offset Current Source - HG-DIFF-AC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.Offset(acqu_duration,N_avg)
    BS.attach_measure(m1)
    results = BS.measure()
    offset_ch1_raw = v_2_uA(results['ch1_offset'])
    offset_ch1 = np.round(offset_ch1_raw,3)
    print("Offset: "+str(offset_ch1)+"µA")
    if not (bm.in_range(offset_ch1_raw,bm.cst.max_VCCS_DIFF_HG_AC_offset)):
        if not (ignore_exception):
            raise Exception("Measured offset out of range")


if (test_single_freq):
    plt.figure()
    print("===== Single Frequency - LG-SE-DC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.TemporalSingleFrequency(freq = freq,nperiods = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = v_2_uA(results['chan1_raw'])
    t = results['t']
    plt.plot(t,ch1, label = "LG-SE-DC")

    print("===== Single Frequency - LG-SE-AC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.TemporalSingleFrequency(freq = freq,nperiods = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = v_2_uA(results['chan1_raw'])
    t = results['t']
    plt.plot(t,ch1, label = "LG-SE-AC")

    print("===== Single Frequency - LG-DIFF-DC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.TemporalSingleFrequency(freq = freq,nperiods = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = v_2_uA(results['chan1_raw'])
    t = results['t']
    plt.plot(t,ch1, label = "LG-DIFF-DC")

    print("===== Single Frequency - LG-DIFF-AC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.TemporalSingleFrequency(freq = freq,nperiods = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = v_2_uA(results['chan1_raw'])
    t = results['t']
    plt.plot(t,ch1, label = "LG-DIFF-DC")

    print("===== Single Frequency - HG-SE-DC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.TemporalSingleFrequency(freq = freq,nperiods = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = v_2_uA(results['chan1_raw'])
    t = results['t']
    plt.plot(t,ch1, label = "HG-SE-DC")

    print("===== Single Frequency - HG-SE-AC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.TemporalSingleFrequency(freq = freq,nperiods = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = v_2_uA(results['chan1_raw'])
    t = results['t']
    plt.plot(t,ch1, label = "HG-SE-AC")

    print("===== Single Frequency - HG-DIFF-DC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.TemporalSingleFrequency(freq = freq,nperiods = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = v_2_uA(results['chan1_raw'])
    t = results['t']
    plt.plot(t,ch1, label = "HG-DIFF-DC")

    print("===== Single Frequency - HG-DIFF-AC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.TemporalSingleFrequency(freq = freq,nperiods = n_period)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = v_2_uA(results['chan1_raw'])
    t = results['t']
    plt.plot(t,ch1, label = "HG-DIFF-AC")

    plt.legend(title = 'CH2 Gain:')
    plt.savefig('./hardware_unitary_tests/figures_hardware/003_current_source_temporal.png')        
    plt.close('all')


if (test_bode):
    plt.figure()
    print("===== Bode - LG-SE-DC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, nperiods=nperiods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "LG-SE-DC")
    mes_gain = v_2_uA(mag_ch1[0])
    print("Current Source Gain: "+ str(np.round((mes_gain),1))+ 'uA/V')
    if not (bm.in_range_min_max(mes_gain,bm.cst.VCVS_min_LG,bm.cst.VCVS_max_LG)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")

    print("===== Bode - LG-SE-AC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, nperiods=nperiods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "LG-SE-AC")
    mes_gain = v_2_uA(mag_ch1[0])
    print("Current Source Gain: "+ str(np.round((mes_gain),1))+ 'uA/V')
    if not (bm.in_range_min_max(mes_gain,bm.cst.VCVS_min_LG,bm.cst.VCVS_max_LG)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")

    print("===== Bode - LG-DIFF-DC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, nperiods=nperiods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "LG-DIFF-DC")
    mes_gain = v_2_uA(mag_ch1[0])
    print("Current Source Gain: "+ str(np.round((mes_gain),1))+ 'uA/V')
    if not (bm.in_range_min_max(mes_gain,bm.cst.VCVS_min_LG,bm.cst.VCVS_max_LG)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")

    print("===== Bode - LG-DIFF-AC Coupling =====")
    BS.manual_config.I_source_gain("LOW")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, nperiods=nperiods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "LG-DIFF-AC")
    mes_gain = v_2_uA(mag_ch1[0])
    print("Current Source Gain: "+ str(np.round((mes_gain),1))+ 'uA/V')
    if not (bm.in_range_min_max(mes_gain,bm.cst.VCVS_min_LG,bm.cst.VCVS_max_LG)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")

    print("===== Bode - HG-SE-DC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, nperiods=nperiods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "HG-SE-DC")
    mes_gain = v_2_uA(mag_ch1[0])
    print("Current Source Gain: "+ str(np.round((mes_gain),1))+ 'uA/V')
    if not (bm.in_range_min_max(mes_gain,bm.cst.VCVS_min_HG,bm.cst.VCVS_max_HG)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")


    print("===== Bode - HG-SE-AC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("SE")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, nperiods=nperiods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "HG-SE-AC")
    mes_gain = v_2_uA(mag_ch1[0])
    print("Current Source Gain: "+ str(np.round((mes_gain),1))+ 'uA/V')
    if not (bm.in_range_min_max(mes_gain,bm.cst.VCVS_min_HG,bm.cst.VCVS_max_HG)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")

    print("===== Bode - HG-DIFF-DC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("DC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, nperiods=nperiods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "HG-DIFF-DC")
    mes_gain = v_2_uA(mag_ch1[0])
    print("Current Source Gain: "+ str(np.round((mes_gain),1))+ 'uA/V')
    if not (bm.in_range_min_max(mes_gain,bm.cst.VCVS_min_HG,bm.cst.VCVS_max_HG)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")

    print("===== Bode - HG-DIFF-AC Coupling =====")
    BS.manual_config.I_source_gain("HIGH")
    BS.manual_config.excitation_coupling("AC")
    BS.manual_config.excitation_signaling_mode("DIFF")
    m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, nperiods=nperiods, ID=0)
    BS.attach_measure(m1)
    results = BS.measure()
    mag_ch1 = results['mag_ch1_raw']
    freq = results['freq']
    plt.semilogx(freq,mag_ch1, label = "HG-DIFF-AC")
    mes_gain = v_2_uA(mag_ch1[0])
    print("Current Source Gain: "+ str(np.round((mes_gain),1))+ 'uA/V')
    if not (bm.in_range_min_max(mes_gain,bm.cst.VCVS_min_HG,bm.cst.VCVS_max_HG)):
        if not (ignore_exception):
            raise Exception("Measured gain out of range")

    plt.legend()

    plt.savefig('./hardware_unitary_tests/figures_hardware/003_current_source_bode.png')        
    plt.close('all')