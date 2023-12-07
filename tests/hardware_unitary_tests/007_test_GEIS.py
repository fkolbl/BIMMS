import bimms as bm
import numpy as np
import matplotlib.pyplot as plt
import time

BS = bm.BIMMS()
print('======== GEIS test ========')
print('Connect a 1k resistor between STIM+ and STIM-')
input('- Press a Key when ready')

g_list = [1,2,4,5,10]

BS.config.excitation_mode("G_EIS")
BS.config.wire_mode("2_WIRE")
BS.config.recording_signaling_mode("AUTO")
BS.config.readout_coupling("DC")
BS.config.G_EIS_gain("HIGH")
BS.config.IRO_gain(1)
BS.config.VRO_gain(1)
BS.config.I_amplitude = 25 #25uA excitation
BS.config.config_settling(1)

plt.figure()

#SE-DC
BS.config.excitation_signaling_mode("SE")
BS.config.excitation_coupling("DC")
m1 = bm.EIS(fmin=1000,fmax=1e7,n_pts=101,settling_time=0.01,NPeriods=8)
BS.attach_measure(m1)
results = BS.measure()
plt.semilogx(results['freq'],results['mag_Z'], label = "SE_DC") 

#SE-AC
BS.config.excitation_signaling_mode("SE")
BS.config.excitation_coupling("AC")
m1 = bm.EIS(fmin=1000,fmax=1e7,n_pts=101,settling_time=0.01,NPeriods=8)
BS.attach_measure(m1)
results = BS.measure()
plt.semilogx(results['freq'],results['mag_Z'], label = "SE_AC") 

#DIFF-DC
BS.config.excitation_signaling_mode("DIFF")
BS.config.excitation_coupling("DC")
m1 = bm.EIS(fmin=1000,fmax=1e7,n_pts=101,settling_time=0.01,NPeriods=8)
BS.attach_measure(m1)
results = BS.measure()
plt.semilogx(results['freq'],results['mag_Z'], label = "DIFF_DC") 

#DIFF-AC
BS.config.excitation_signaling_mode("DIFF")
BS.config.excitation_coupling("AC")
m1 = bm.EIS(fmin=1000,fmax=1e7,n_pts=101,settling_time=0.01,NPeriods=8)
BS.attach_measure(m1)
results = BS.measure()
plt.semilogx(results['freq'],results['mag_Z'], label = "DIFF_AC") 

plt.legend()
plt.savefig('./figures_hardware/007_GEIS_1k_config.png')
plt.close('all')


#GAIN IRO
plt.figure()
for gain in g_list:
    BS.config.IRO_gain(gain)
    m1 = bm.EIS(fmin=1000,fmax=1e7,n_pts=101,settling_time=0.01,NPeriods=8)
    BS.attach_measure(m1)
    results = BS.measure()
    plt.semilogx(results['freq'],results['mag_Z'], label = "gain_IRO: "+str(gain)) 
plt.savefig('./figures_hardware/007_GEIS_1k_GAIN_IRO.png')
plt.close('all')

#GAIN VRO
plt.figure()
BS.config.IRO_gain(1)
for gain in g_list:
    BS.config.VRO_gain(gain)
    m1 = bm.EIS(fmin=1000,fmax=1e7,n_pts=101,settling_time=0.01,NPeriods=8)
    BS.attach_measure(m1)
    results = BS.measure()
    plt.semilogx(results['freq'],results['mag_Z'], label = "gain_VRO: "+str(gain)) 
plt.savefig('./figures_hardware/007_GEIS_1k_GAIN_VRO.png')
plt.close('all')

#BOTH GAIN
plt.figure()
for gain in g_list:
    BS.config.VRO_gain(gain)
    BS.config.IRO_gain(gain)
    m1 = bm.EIS(fmin=1000,fmax=1e7,n_pts=101,settling_time=0.01,NPeriods=8)
    BS.attach_measure(m1)
    results = BS.measure()
    plt.semilogx(results['freq'],results['mag_Z'], label = "IRO_VRO_gain: "+str(gain)) 
plt.savefig('./figures_hardware/007_GEIS_1k_GAIN_VRO_IRO.png')
plt.close('all')
del BS



