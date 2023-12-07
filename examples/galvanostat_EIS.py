import bimms as bm
import numpy as np
import matplotlib.pyplot as plt
import time

BS = bm.BIMMS()

Gain_IRO = 20
Gain_VRO = 20
fmin = 1000
fmax = 1e7
n_pts = 101
settling_time = 0.01
NPeriods = 8
I_stim = 100 #100uA excitation

BS.config.excitation_mode("G_EIS")
BS.config.wire_mode("2_WIRE")
BS.config.excitation_signaling_mode("SE")
BS.config.excitation_coupling("DC")
BS.config.G_EIS_gain("HIGH")

BS.config.IRO_gain(Gain_IRO)
BS.config.VRO_gain(Gain_VRO)
BS.config.I_amplitude = I_stim #


m1 = bm.EIS(fmin=fmin,fmax=fmax,n_pts=n_pts,settling_time=settling_time,NPeriods=NPeriods)
BS.attach_measure(m1)
results = BS.measure()
del BS

plt.figure()
plt.semilogx(results['freq'],results['mag_Z']) 


plt.figure()
plt.semilogx(results['freq'],results['phase_Z']) 
plt.show()
