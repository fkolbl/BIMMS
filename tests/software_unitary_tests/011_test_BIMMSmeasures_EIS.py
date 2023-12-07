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
BS.config.IRO_gain = 10
BS.config.VRO_gain = 10
BS.config.DC_feedback = False
BS.config.I_amplitude = 100 # uA
BS.config.V_amplitude = 250 # mV

for i in range(3):
    BS.attach_measure(bm.EIS(fmin=1e3,fmax=1e6,n_pts=101,settling_time=0.01,NPeriods=8, ID=i))

results = BS.measure()
del BS

plt.figure()
for i in range(3):
    plt.semilogx(results[i]['freq'],results[i]['mag_Z'])
plt.savefig('./software_unitary_tests/figures_software/011_multipleEIS_mag.png')

plt.figure()
for i in range(3):
    plt.semilogx(results[i]['freq'],results[i]['phase_Z'])
plt.savefig('./software_unitary_tests/figures_software/011_multipleEIS_phase.png')

