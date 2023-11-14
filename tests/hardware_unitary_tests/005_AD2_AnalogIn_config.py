import bimms as bm
import numpy as np
import matplotlib.pyplot as plt

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

#Decimate mode:
BS.interface.in_avering_decimate_mode(0)
BS.interface.in_avering_decimate_mode(1)
t,dat0,dat1 = bm.TemporalSingleFrequency(BS,Freq = 10000,Nperiod=10,Phase = 90)


plt.plot(t,dat1)

#Decimate mode:
BS.interface.in_avering_sampling_mode(0)
BS.interface.in_avering_sampling_mode(1)
t,dat0,dat1 = bm.TemporalSingleFrequency(BS,Freq = 10000,Nperiod=10,Phase = 90)

plt.plot(t,dat1)
plt.show()


