import bimms as bm
import matplotlib.pyplot as plt

BS = bm.BIMMS()
BS.config.excitation_sources("INTERNAL")
BS.config.excitation_mode("P_EIS")
BS.config.wire_mode("2_WIRE")
BS.config.recording_mode("BOTH")
BS.config.excitation_signaling_mode("SE")
BS.config.recording_signaling_mode("AUTO")
BS.config.excitation_coupling("DC")
BS.config.G_EIS_gain = "LOW"
BS.config.IRO_gain = 1
BS.config.VRO_gain = 1
BS.config.DC_feedback = False
BS.config.V_amplitude = 50 # mV


m1 = bm.EIS(fmin=1000,fmax=1e7,n_pts=101,settling_time=0.01,NPeriods=8)
BS.attach_measure(m1)
results = BS.measure()
del BS

plt.figure()
plt.semilogx(results['freq'],results['mag'])
plt.show()
