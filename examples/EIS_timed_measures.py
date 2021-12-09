import bimms as bm
import numpy as np
import matplotlib.pyplot as plt
import time as t

fmin = 100            #Start Frequency (Hz)
fmax = 10e6            #Stop Frequency (Hz)
n_pts = 200           #Number of frequency points
amp = 0.1              #amplitude (V)
settling_time = 0.01   #Settling time between points
NPeriods = 32          #Number of period per frequency points

N_measures = 10        #Total number of measure
t_interval = 30        #interval between two measure (s)

two_wires = True       #Connection to the DUT mode: True  = 2wires, False = 4wires

output_file_name = "EIS_timed_measures.csv"

BS = bm.BIMMS()

data = []
impedance_l = []
phase_l = []

for i in range (N_measures):
	freq, impedance, phase_mes = BS.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = amp, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = False, two_wires = two_wires, coupling = 'DC', apply_cal = True)
	data.append(impedance)
	data.append(phase_mes)
	impedance_l.append(impedance)
	phase_l.append(phase_mes)
	print("Waiting...")
	t.sleep(t_interval)

BS.close()


#dump data to csv
data.insert(0,freq)
data = np.transpose(data)
np.savetxt(output_file_name, data , delimiter=",")
plt.figure(1)
plt.subplot(211)
alpha = np.linspace(0.2,1,N_measures)
for i in range(N_measures):
	plt.semilogx(freq,impedance_l[i],color = 'darkgoldenrod',alpha = alpha[i])
plt.xlabel('Frequency ($Hz$)')
plt.ylabel('Impedance ($\Omega$)')
plt.grid()
plt.subplot(212)
for i in range(N_measures):
	plt.semilogx(freq,phase_l[i],color = 'darkgoldenrod',alpha = alpha[i])
plt.grid()
plt.xlabel('Frequency ($Hz$)')
plt.ylabel('Phase ($°$)')

plt.show()


