import bimms as bm
import matplotlib.pyplot as plt
from time import sleep

BS = bm.BIMMS()
BS.excitation_sources("INTERNAL")
BS.excitation_mode("P_EIS")
BS.wire_mode("2_WIRE")
BS.recording_mode("BOTH")
BS.excitation_signaling_mode("SE")
BS.recording_signaling_mode("AUTO")
BS.excitation_coupling("DC")
BS.G_EIS_gain = "LOW"
BS.IRO_gain = 1
BS.VRO_gain = 1
BS.DC_feedback = False
BS.set_config()


t,dat0,dat1 = bm.TemporalSingleFrequency(BS,Freq = 10000,Nperiod=10,Phase = 90)

plt.figure()
plt.plot(t,dat0)
plt.plot(t,dat1)
plt.show()

