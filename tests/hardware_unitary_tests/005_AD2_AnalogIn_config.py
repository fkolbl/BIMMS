import bimms as bm
import numpy as np
import matplotlib.pyplot as plt

BS = bm.BIMMS()
BS.config_mode("MANUAL")

BS.manual_config.waveform_gen("INTERNAL")
BS.manual_config.excitation_source("VOLTAGE")
BS.manual_config.I_source_gain("HIGH")
BS.manual_config.wire_mode("2_WIRE")
BS.manual_config.excitation_signaling_mode("SE")
BS.manual_config.excitation_coupling("DC")
BS.manual_config.DC_feedback(False)
BS.manual_config.Enable_Isource(True)

BS.manual_config.CHx_to_Scopex("CH1")
BS.manual_config.CH1_coupling("DC")
BS.manual_config.CH2_coupling("DC")
BS.manual_config.TIA_coupling("DC")
BS.manual_config.connect_TIA(False)
BS.manual_config.TIA_to_CH2(False)
BS.manual_config.TIA_NEG("GND")
BS.manual_config.CH1_gain(1)
BS.manual_config.CH2_gain(1)

amp_AWG = 0.005
BS.manual_config.AWG_amp(amp_AWG)

freq = 1e3
n_period = 8

#Decimate mode:
BS.AD2_set_input_range(-1,2.0)
BS.AD2_input_decimate_filter()

m1 = bm.TemporalSingleFrequency(freq = freq,nperiods = n_period)
BS.attach_measure(m1)
results = BS.measure()
ch1 = (results['chan1_raw'])
t = results['t']
plt.plot(t,ch1,label = "DECIMATE MODE")

#average mode:
BS.AD2_input_average_filter()
m1 = bm.TemporalSingleFrequency(freq = freq,nperiods = n_period)
BS.attach_measure(m1)
results = BS.measure()
ch1 = (results['chan1_raw'])
t = results['t']
plt.plot(t,ch1,label = "AVERAGING MODE")
plt.savefig('./hardware_unitary_tests/figures_hardware/005_AD2_input_mode.png')
plt.close('all')

#input attenuation
range_list = BS.AD2_get_input_ranges()
range_list.sort(reverse=True)
plt.figure()
for range in range_list:
    BS.AD2_set_input_range(-1,range)
    BS.attach_measure(m1)
    results = BS.measure()
    ch1 = (results['chan1_raw'])
    t = results['t']
    plt.plot(t,ch1,label = str(range) +'V')

plt.legend(title = 'Range:')
plt.savefig('./hardware_unitary_tests/figures_hardware/005_AD2_range.png')
plt.close('all')


