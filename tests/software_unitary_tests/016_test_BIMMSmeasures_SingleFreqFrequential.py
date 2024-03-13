import bimms as bm
import matplotlib.pyplot as plt
from time import perf_counter

BS = bm.BIMMS()
BS.config.excitation_sources("INTERNAL")
BS.config.excitation_mode("P_EIS")
BS.config.wire_mode("4_WIRE")
BS.config.recording_mode("BOTH")
BS.config.excitation_signaling_mode("SE")
BS.config.recording_signaling_mode("AUTO")
BS.config.excitation_coupling("DC")
BS.config.G_EIS_gain = "LOW"
BS.config.IRO_gain = 1
BS.config.VRO_gain = 1
BS.config.DC_feedback = False
BS.config.V_amplitude = 100 # mV


m1 = bm.FrequentialSingleFrequency(freq=10000,nperiods=100 ,settling_time=0.0001)
#m1 = bm.TemporalSingleFrequency(freq=1000,nperiods=10, ID=2)
N_meas = 10
for i in range(N_meas):
    BS.attach_measure(m1)

t0 = perf_counter()
results = BS.measure()

print("measurments done in", (perf_counter() - t0)/2*N_meas, "s/measure")
print(results[0].EIS())
del BS

