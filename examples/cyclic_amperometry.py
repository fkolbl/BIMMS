"""
	Python script to perform Cyclic Amperometry with BIMMS.
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


scan_rate = 100e-3		# Scan rate in mA
I_amp= 0.25				# Maximum amplitude in mA
V_range = 10.0          # Voltage measurement range
n_avg = 0               # Averaging 
n_delay= 1              # Number of cycle delay before measuring
output_file_name = "cyclic_amperometry.csv"


period_triangle = I_amp/scan_rate

BS = bm.BIMMS()
t,voltage,current = BS.cyclic_amperometry(period_triangle,I_amp,V_range,n_delay,n_avg,filter=True, mode = 'two_points', coupling = 'DC', differential = True,High_gain = True, DC_feedback = False)
BS.close()


#dump data to csv
data = np.asarray([t,voltage,current])
data = np.transpose(data)
np.savetxt(output_file_name, data, delimiter=",")


plt.figure(1)
plt.subplot(211)
plt.plot(t,voltage)
plt.grid()
plt.xlabel('Time (s)')
plt.ylabel('Recorded Voltage (V)')
plt.subplot(212)
plt.plot(t,current*1000)
plt.grid()
plt.xlabel('Time (s)')
plt.ylabel('Recorded Current (mA)')

plt.figure(2)
plt.plot(voltage,current*1000)
plt.grid()
plt.ylabel('Recorded Current (mA)')
plt.xlabel('Recorded Voltage (V)')
plt.show()



