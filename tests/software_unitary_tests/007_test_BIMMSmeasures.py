import bimms as bm
import matplotlib.pyplot as plt

BS = bm.BIMMS()
BS.config.excitation_sources("INTERNAL")
BS.config.excitation_mode("P_EIS")
BS.config.wire_mode("2_WIRE")
BS.config.recording_mode("BOTH")
BS.config.excitation_signaling_mode("DIFF")
BS.config.recording_signaling_mode("AUTO")
BS.config.excitation_coupling("DC")
BS.config.G_EIS_gain = "LOW"
BS.config.IRO_gain = 1
BS.config.VRO_gain = 1
BS.config.DC_feedback = False
BS.set_config()

freq, mag, phase = bm.EIS(BS,fmin=1000,fmax=1e7,n_pts=101,amp=0.1,offset=0,settling_time=0.01,NPeriods=8,apply_cal=False)

plt.figure()
plt.semilogx(freq,mag)
plt.show()

