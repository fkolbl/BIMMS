import bimms as bm
import matplotlib.pyplot as plt
from time import sleep

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
BS.config.V_amplitude = 100 # mV

m1 = bm.TemporalSingleFrequency(freq = 10000,Nperiod=10,phase = 90)
BS.attach_measure(m1)
results = BS.measure()
del BS

t = results['t']
ch1  = results['chan1_raw']
ch2 = results['chan2_raw']

plt.figure()
plt.plot(t,ch1)
plt.plot(t,ch2)
plt.savefig('./figures_software/008_singleFreqAcquisition.png')

