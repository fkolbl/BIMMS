import bimms as bm
import numpy as np
import matplotlib.pyplot as plt

BS = bm.BIMMS()

Gain_IRO = 20
Gain_VRO = 20
fmin = 1000
fmax = 1e7
n_pts = 101
settling_time = 0.01
nperiods = 8
V_stim = 100 #100mV excitation

BS.config.excitation_mode("P_EIS")
BS.config.wire_mode("2_WIRE")
BS.config.excitation_signaling_mode("SE")
BS.config.excitation_coupling("DC")

BS.config.IRO_gain(Gain_IRO)
BS.config.VRO_gain(Gain_VRO)
BS.config.V_amplitude = V_stim #100mV excitation


m1 = bm.EIS(fmin=fmin,fmax=fmax,n_pts=n_pts,settling_time=settling_time,nperiods=nperiods)
BS.attach_measure(m1)
results = BS.measure()
del BS

plt.figure()
plt.semilogx(results['freq'],results['mag_Z']) 


plt.figure()
plt.semilogx(results['freq'],results['phase_Z']) 
plt.show()


