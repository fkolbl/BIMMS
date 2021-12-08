"""
	Python script to calibrate BIMMS gains and store them in a dedicated json file.
	Authors: Florian Kolbl / Louis Regnacq
	(c) ETIS - University Cergy-Pontoise
		IMS - University of Bordeaux
		CNRS

	Requires:
		Python 3.6 or higher
		Analysis_Instrument - class handling Analog Discovery 2 (Digilent)


"""


import bimms as BM
import time
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import json
from scipy.signal import savgol_filter


################
## Parameters ##
################
load = 994 				#Default Resistor value 
frequency = 1000
amp = 0.2
amp_to_current = 1
settling_time = 0.01
NPeriods = 64
gain_SE = 1.1
gain_DIFF = 2.2
gain_TIA = 1000
gain_current_source_low = 1/50000
gain_current_source_high = 1/1000
N_mes = 10
v_range_ch1 = 1.0
v_range_ch2 = 1.0
####################################################
serial_key = "BIMMS_SERIAL"
cal_folder = './CalibrationData/'

bm = BM.BIMMS()
bm.set_STM32_idle()
serial = bm.ID

#Read existing calibration file 


print('======== DC Calibration for BIMMS ========')
print('- Connect R = 1000 Ohm to the board')
print('- Precisely measured value should be specified in the script ')
input('- Press a Key when ready')


print('======== Measuring Voltage source Gain ========')

bm.set_voltage_excitation(coupling = 'DC', differential_stim = False)
bm.set_recording_voltage(coupling = 'DC', gain = 1)
bm.set_recording_current(differential = False, coupling = 'DC', gain = 1)
bm.set_2_points_config()
bm.set_config()
gain_voltage_SE_array = []
gain_TIA_array = []
for k in range (N_mes):
	gain1, phase1, gain2 = bm.interface.single_frequency_gain_phase(frequency= frequency,settling_time=settling_time,
			amp = amp, offset = 0.0, Nperiods = NPeriods,Vrange_CH1 = v_range_ch1,Vrange_CH2 = v_range_ch2, 
			offset_CH1 = 0.0,offset_CH2 = 0.0)
	gain_voltage_SE_array.append(gain2)
	gain_TIA_array.append(gain1)


gain_voltage_SE = np.mean(gain_voltage_SE_array)
gain_TIA = load/np.mean(gain_TIA_array)
print("Measured Voltage source gain (Single Ended): " + str(round(gain_voltage_SE,3)) + " V/V")
print("Measured TIA gain: " + str(round(gain_TIA,3)) + " V/A")

bm.set_voltage_excitation(coupling = 'DC', differential_stim = True)
bm.set_recording_voltage(coupling = 'DC', gain = 1)
bm.set_recording_current(differential = True, coupling = 'DC', gain = 1)
bm.set_2_points_config()
bm.set_config()
gain_voltage_DIFF_array = []
for k in range (N_mes):
	gain1, phase1, gain2 = bm.interface.single_frequency_gain_phase(frequency= frequency,settling_time=settling_time,
			amp = amp, offset = 0.0, Nperiods = NPeriods,Vrange_CH1 = v_range_ch1,Vrange_CH2 = v_range_ch2, 
			offset_CH1 = 0.0,offset_CH2 = 0.0)
	gain_voltage_DIFF_array.append(gain2)

gain_voltage_DIFF = np.mean(gain_voltage_DIFF_array)
print("Measured Voltage source gain (Differential): " + str(round(gain_voltage_DIFF,3)) + " V/V")

print('======== Measuring Current Source Gain ========')
bm.set_current_excitation(coupling = 'DC', differential_stim = True, High_gain = False)
bm.set_recording_voltage(coupling = 'DC', gain = 1)
bm.set_recording_current(differential = True, coupling = 'DC', gain = 1)
bm.set_2_points_config()
bm.set_config()
low_gain_current_array = []
for k in range (N_mes):
	gain1, phase1, gain2 = bm.interface.single_frequency_gain_phase(frequency= frequency,settling_time=settling_time,
			amp = amp_to_current, offset = 0.0, Nperiods = NPeriods,Vrange_CH1 = v_range_ch1,Vrange_CH2 = v_range_ch2, 
			offset_CH1 = 0.0,offset_CH2 = 0.0)
	low_gain_current_array.append(gain2)

low_gain_current = np.mean(low_gain_current_array)
print("Measured current source gain (Low Gain): " + str(round(low_gain_current,3)) + " mA/V")


bm.set_current_excitation(coupling = 'DC', differential_stim = True, High_gain = True)
bm.set_recording_voltage(coupling = 'DC', gain = 1)
bm.set_recording_current(differential = True, coupling = 'DC', gain = 1)
bm.set_2_points_config()
bm.set_config()
high_gain_current_array = []
for k in range (N_mes):
	gain1, phase1, gain2 = bm.interface.single_frequency_gain_phase(frequency= frequency,settling_time=settling_time,
			amp = amp_to_current, offset = 0.0, Nperiods = NPeriods,Vrange_CH1 = v_range_ch1,Vrange_CH2 = v_range_ch2, 
			offset_CH1 = 0.0,offset_CH2 = 0.0)
	high_gain_current_array.append(gain2)

high_gain_current = np.mean(high_gain_current_array)
print("Measured current source gain (High Gain): " + str(round(high_gain_current,3)) + " mA/V")

bm.Update_DCCal('gain_voltage_SE',gain_voltage_SE)

bm.Update_DCCal('gain_voltage_DIFF',gain_voltage_DIFF)
bm.Update_DCCal('low_gain_current',low_gain_current)
bm.Update_DCCal('high_gain_current',high_gain_current)
bm.Update_DCCal('gain_TIA',gain_TIA)

bm.close()



