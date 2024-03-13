import bimms as bm
import matplotlib.pyplot as plt
from time import sleep
import numpy as np



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


f1 = 1e3
f2 = 10e3
n_T = 4
Npts = BS.AD2_input_buffer_size

t = np.linspace(0, n_T/min(f1, f2), Npts)
S = np.sin(2*np.pi*f1*t)
S += np.sin(2*np.pi*f2*t)
S = S / S.max()

fs = 1/(t[1]-t[0])

print(fs, BS.AD2_input_Fs_max)


m1 = bm.TemporalSingleFrequency()
m1.set_signal(sig=S, fs=fs)
BS.attach_measure(m1)
results = BS.measure()
del BS

t = results['t_raw']
ch1  = results['chan1_raw']
ch2 = results['chan2_raw']

plt.figure()
plt.plot(t,ch1)
plt.plot(t,ch2)
plt.plot(S)
plt.savefig('./software_unitary_tests/figures_software/008_singleFreqAcquisition.png')

results.fft()
f = results['f']
ch1f  = results['chan1_f']/results["n_sample"]
ch2f = results['chan2_f']/results["n_sample"]
plt.figure()
plt.plot(f,ch1f)
plt.plot(f,ch2f)

plt.xlim((1,11000))
plt.show()