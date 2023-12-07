import bimms as bm
import numpy as np
import matplotlib.pyplot as plt

#bode 
fmin = 1e3
fmax = 1e6
n_pts=101
settling_time=0.001
NPeriods=8

r_l = 1000

BS = bm.BIMMS()

BS.config.excitation_mode("P_EIS")
BS.config.wire_mode("2_WIRE")
BS.config.IRO_gain(10)
BS.config.VRO_gain(5)
BS.config.V_amplitude = 50 #50mV excitation
BS.config.excitation_signaling_mode("SE")
BS.config.excitation_coupling("DC")
BS.config.recording_signaling_mode("SE")
BS.config.readout_coupling("DC")


m1 = bm.Bode(fmin=fmin, fmax=fmax, n_pts=n_pts, settling_time=settling_time, NPeriods=NPeriods, ID=0)
BS.attach_measure(m1)
results = BS.measure()
ch1_raw = results['mag_ch1_raw']
ch2_raw = results['mag_ch2_raw']
IRO = results['I_readout']
VRO = results['V_readout']
freq = results['freq']
plt.figure()
plt.loglog(freq,ch1_raw, label = "CH1_raw")   
plt.loglog(freq,VRO, label = "V_readout") 
plt.legend()
plt.savefig('./figures_software/013_bode_IV_V_readout.png')
plt.close("all")

plt.figure()
plt.loglog(freq,ch2_raw, label = "CH2_raw")   
plt.loglog(freq,IRO, label = "I_readout") 
plt.legend()
plt.savefig('./figures_software/013_bode_IV_I_readout.png')
plt.close("all")
