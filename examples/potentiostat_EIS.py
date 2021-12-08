"""
	Python script to perform Potentiostat EIS with BIMMS.
	Authors: Florian Kolbl / Louis Regnacq
	(c) ETIS - University Cergy-Pontoise
		IMS - University of Bordeaux
		CNRS

	Requires:
		Python 3.6 or higher
		Analysis_Instrument - class handling Analog Discovery 2 (Digilent)

"""


import bimms as bm
import numpy as np
import matplotlib.pyplot as plt

fmin = 1000
fmax = 10e6
n_pts = 200
amp = 0.1
settling_time = 0.01
NPeriods = 32

output_file_name = "potentiostat_EIS.csv"

BS = bm.BIMMS()

freq, gain_mes, phase_mes = BS.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = amp, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'DC', apply_cal = True)

BS.close()

#dump data to csv
data = np.asarray([freq,gain_mes,phase_mes])
data = np.transpose(data)
np.savetxt(output_file_name, data, delimiter=",")

plt.figure(1)
plt.subplot(211)
plt.semilogx(freq,gain_mes)
plt.xlabel('Frequency ($Hz$)')
plt.ylabel('Impedance ($\Omega$)')
plt.grid()
plt.legend()
plt.subplot(212)
plt.semilogx(freq,phase_mes)
plt.grid()
plt.xlabel('Frequency ($Hz$)')
plt.ylabel('Phase ($°$)')

plt.show()

