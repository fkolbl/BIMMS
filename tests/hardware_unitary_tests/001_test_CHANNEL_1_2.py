import bimms as bm
import numpy as np
import matplotlib.pyplot as plt

test_ch1 = True
test_ch2 = True

test_offset = True
test_single_freq = True
test_bode = True

BS = bm.BIMMS()

BS.config_mode("TEST")

BS.test_config.waveform_gen("INTERNAL")
BS.test_config.excitation_source("NONE")
BS.test_config.I_source_gain("HIGH")
BS.test_config.wire_mode("4_WIRE")
BS.test_config.excitation_signaling_mode("SE")
BS.test_config.excitation_coupling("DC")
BS.test_config.DC_feedback(False)
BS.test_config.Enable_Isource(True)

BS.test_config.CHx_to_Scopex("NONE")
BS.test_config.CH1_coupling("DC")
BS.test_config.CH2_coupling("DC")
BS.test_config.TIA_coupling("DC")
BS.test_config.TIA_to_CH2(False)
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
amp_AWG = 0.02

#bode 
fmin = 1e3
fmax = 1e6
n_pts=101
settling_time=0.001
NPeriods=8

BS.test_config.AWG_amp(amp_AWG)

if (test_ch1):
    print('======== Channel 1 Test ========')
    print('- Connect CH1 + to AWG1')
    print('- Connect CH1 - to GND')
    input('- Press a Key when ready')

    BS.test_config.CHx_to_Scopex("CH1")

    if (test_offset):
        #MEASURE OFFSET CH1 - DC
        print("===== Offset CH1 - DC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH1_gain(gain)
            m1 = bm.Offset(acqu_duration,N_avg)
            BS.attach_measure(m1)
            print("CH1 Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            offset_ch1 = np.round(results['ch1_offset']*1000,3)
            print("Offset: "+str(offset_ch1)+"mV")

        #MEASURE OFFSET CH1 - AC
        print("===== Offset CH1 - AC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH1_gain(gain)
            BS.test_config.CH1_coupling("AC")
            m1 = bm.Offset(acqu_duration,N_avg)
            BS.attach_measure(m1)
            print("CH1 Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            offset_ch1 = np.round(results['ch1_offset']*1000,3)
            print("Offset: "+str(offset_ch1)+"mV")

    if (test_single_freq):
        plt.figure()
        print("===== Single Frequency CH1 - DC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH1_gain(gain)
            BS.test_config.CH1_coupling("DC")
            m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
            BS.attach_measure(m1)
            print("CH1 Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            ch1 = results['chan1']
            t = results['t']
            plt.plot(t,ch1, label = str(gain))
        plt.legend(title = 'CH1 Gain:')
    
        plt.figure()
        print("===== Single Frequency CH1 - AC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH1_gain(gain)
            BS.test_config.CH1_coupling("AC")
            m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
            BS.attach_measure(m1)
            print("CH1 Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            ch1 = results['chan1']
            t = results['t']
            plt.plot(t,ch1, label = str(gain))
        plt.legend(title = 'CH1 Gain:')


    if (test_bode):
        plt.figure()
        print("===== Bode CH1 - DC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH1_gain(gain)
            BS.test_config.CH1_coupling("DC")
            m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
            BS.attach_measure(m1)
            print("CH1 Set Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            mag_ch1 = results['mag_ch1']
            freq = results['freq']
            plt.loglog(freq,mag_ch1, label = str(gain))
            mes_gain = mag_ch1[0]
            print("CH1 Measured Gain: "+ str(np.round(mes_gain,3))+ 'V/V')
        plt.legend(title = 'CH1 Gain:')

        plt.figure()
        print("===== Bode CH1 - AC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH1_gain(gain)
            BS.test_config.CH1_coupling("AC")
            m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
            BS.attach_measure(m1)
            print("CH1 Set Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            mag_ch1 = results['mag_ch1']
            freq = results['freq']
            plt.loglog(freq,mag_ch1, label = str(gain))
            mes_gain = mag_ch1[0]
            print("CH1 Measured Gain: "+ str(np.round(mes_gain,3))+ 'V/V')
        plt.legend(title = 'CH1 Gain:')

if (test_ch2):
    print('======== Channel 2 Test ========')
    print('- Connect CH2 + to AWG1')
    print('- Connect CH2 - to GND')
    input('- Press a Key when ready')

    BS.test_config.CHx_to_Scopex("CH2")

    if (test_offset):
        #MEASURE OFFSET CH1 - DC
        print("===== Offset CH2 - DC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH2_gain(gain)
            m1 = bm.Offset(acqu_duration,N_avg)
            BS.attach_measure(m1)
            print("CH2 Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            offset_ch2 = np.round(results['ch2_offset']*1000,3)
            print("Offset: "+str(offset_ch2)+"mV")

        #MEASURE OFFSET CH1 - AC
        print("===== Offset CH2 - AC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH2_gain(gain)
            BS.test_config.CH2_coupling("AC")
            m1 = bm.Offset(acqu_duration,N_avg)
            BS.attach_measure(m1)
            print("CH2 Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            offset_ch2 = np.round(results['ch2_offset']*1000,3)
            print("Offset: "+str(offset_ch2)+"mV")
    

    if (test_single_freq):
        BS.test_config.AWG_amp(amp_AWG)
        plt.figure()
        print("===== Single Frequency CH2 - DC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH2_gain(gain)
            BS.test_config.CH2_coupling("DC")
            m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
            BS.attach_measure(m1)
            print("CH2 Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            ch2 = results['chan2']
            t = results['t']
            plt.plot(t,ch2, label = str(gain))
        plt.legend(title = 'CH2 Gain:')
    
        plt.figure()
        print("===== Single Frequency CH2 - AC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH2_gain(gain)
            BS.test_config.CH2_coupling("AC")
            m1 = bm.TemporalSingleFrequency(freq = freq,Nperiod = n_period)
            BS.attach_measure(m1)
            print("CH2 Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            ch2 = results['chan2']
            t = results['t']
            plt.plot(t,ch2, label = str(gain))
        plt.legend(title = 'CH2 Gain:')
    

    if (test_bode):
        BS.test_config.AWG_amp(amp_AWG)
        plt.figure()
        print("===== Bode CH2 - DC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH2_gain(gain)
            BS.test_config.CH2_coupling("DC")
            m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
            BS.attach_measure(m1)
            print("CH2 Set Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            mag_ch2 = results['mag_ch2']
            freq = results['freq']
            plt.loglog(freq,mag_ch2, label = str(gain))
            mes_gain = mag_ch2[0]
            print("CH2 Measured Gain: "+ str(np.round(mes_gain,3))+ 'V/V')
        plt.legend(title = 'CH2 Gain:')

    if (test_bode):
        BS.test_config.AWG_amp(amp_AWG)
        plt.figure()
        print("===== Bode CH2 - AC Coupling =====")
        for gain in bm.BIMMScst.gain_array:
            BS.test_config.CH2_gain(gain)
            BS.test_config.CH2_coupling("AC")
            m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
            BS.attach_measure(m1)
            print("CH2 Set Gain: "+ str(gain)+ 'V/V')
            results = BS.measure()
            mag_ch2 = results['mag_ch2']
            freq = results['freq']
            plt.loglog(freq,mag_ch2, label = str(gain))
            mes_gain = mag_ch2[0]
            print("CH2 Measured Gain: "+ str(np.round(mes_gain,3))+ 'V/V')
        plt.legend(title = 'CH2 Gain:')






plt.show()