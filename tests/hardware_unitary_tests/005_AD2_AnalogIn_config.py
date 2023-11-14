import bimms as bm
import numpy as np
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
BS.set_config()

#Decimate mode:
BS.interface.in_channel_range_set(-1,2.0)
BS.interface.in_decimate_filter_mode(-1)
t,dat0,dat1 = bm.TemporalSingleFrequency(BS,amp = 0.005,Freq = 10000,Nperiod=10,Phase = 90)


plt.plot(t,dat0,label = "DECIMATE MODE")

#average mode:
BS.interface.in_average_filter_mode(-1)
t,dat0,dat1 = bm.TemporalSingleFrequency(BS,amp = 0.005,Freq = 10000,Nperiod=10,Phase = 90)

plt.plot(t,dat0,label = "AVERAGING MODE")
plt.legend()

#input attenuation
range_list = BS.interface.in_channel_range_info(-1)
range_list.sort(reverse=True)
plt.figure()
for range in range_list:
    BS.interface.in_channel_range_set(-1,range)
    t,dat0,dat1 = bm.TemporalSingleFrequency(BS,amp = 0.005,Freq = 10000,Nperiod=10,Phase = 90)
    plt.plot(t,dat0,label = str(range) +'V')

plt.legend(title = 'Range:')
plt.show()


#TODO CONF AD2:
#SET in_channel_range_set --> 2.0,5.0 or 5.0 --> 2.0 by default; check if saturation?
#BS.interface.in_average_filter_mode(-1)
#AD2 attenation = 1.0
#AD2 offsets = 0.0 
#Triggers --> AWG by default --> external TODO
#Conf modes (bode,)
