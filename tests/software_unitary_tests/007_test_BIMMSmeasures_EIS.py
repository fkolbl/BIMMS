import bimms as bm
import matplotlib.pyplot as plt

BS = bm.BIMMS()
BS.excitation_sources("INTERNAL")
BS.excitation_mode("P_EIS")
BS.wire_mode("2_WIRE")
BS.recording_mode("BOTH")
BS.excitation_signaling_mode("DIFF")
BS.recording_signaling_mode("AUTO")
BS.excitation_coupling("DC")
BS.G_EIS_gain = "LOW"
BS.IRO_gain = 1
BS.VRO_gain = 1
BS.DC_feedback = False

freq, mag, phase = bm.EIS(BS,fmin=1000,fmax=1e7,n_pts=101,amp=0.1,offset=0,settling_time=0.01,NPeriods=8,apply_cal=False)

plt.figure()
plt.semilogx(freq,mag)
plt.show()

