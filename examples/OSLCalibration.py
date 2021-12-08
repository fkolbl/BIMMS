"""
	Python script to calibrate BIMMS with a Open-Short-Load method and store results in the dedicated json file.
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
#import BIMMS_PostProcess as PP


################
## Parameters ##
################
resistor = 994
fmin = 10000
fmax = 10e6
n_pts = 400
offset = 0
settling_time = 0.01
NPeriods = 64
v_amp = 0.1
v_amp_AC = 0.01
i_amp_high = 0.2
i_amp_low = 0.01
####################################################


#Set to 1 to perform the calibration of a specific BIMMS configuration 
cal_potentiostat_SE_DC = 1 
cal_potentiostat_SE_AC = 0 
cal_potentiostat_DIFF_DC = 0  
cal_potentiostat_DIFF_AC = 0 

cal_galvanostat_SE_DC_high_gain = 0
cal_galvanostat_SE_DC_low_gain = 0
cal_galvanostat_SE_AC_high_gain = 0
cal_galvanostat_SE_AC_low_gain = 0
cal_galvanostat_DIFF_DC_high_gain = 0
cal_galvanostat_DIFF_DC_low_gain = 0
cal_galvanostat_DIFF_AC_high_gain = 0
cal_galvanostat_DIFF_AC_low_gain = 0

#Set to 1 to plot the calibration result of a specific BIMMS configration
plot_cal_potentiostat_SE_DC = 1
plot_cal_potentiostat_SE_AC = 1
plot_cal_potentiostat_DIFF_DC = 1
plot_cal_potentiostat_DIFF_AC = 1

plot_galvanostat_SE_DC_high_gain = 1
plot_galvanostat_SE_DC_low_gain = 1
plot_galvanostat_SE_AC_high_gain = 1
plot_galvanostat_SE_AC_low_gain = 1
plot_galvanostat_DIFF_DC_high_gain = 1
plot_galvanostat_DIFF_DC_low_gain = 1
plot_galvanostat_DIFF_AC_high_gain = 1
plot_galvanostat_DIFF_AC_low_gain = 1


serial_key = "BIMMS_SERIAL"
cal_folder = './CalibrationData/'

bm = BM.BIMMS()
bm.set_STM32_idle()
serial = bm.ID

print('======== Load Calibration ========')
print('- Connect the load')
input('- Press a Key when ready')
if (cal_potentiostat_SE_DC):
	print('Potentiostat EIS - Single Ended - DC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = False, two_wires = True, coupling = 'DC', apply_cal = False)
	cal_load_SE_DC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_load_SE_DC.FilterData(51,3,51,3)
	cal_load_SE_DC.GetPoly(8,8,8,8)


if (cal_potentiostat_SE_AC):
	print('Potentiostat EIS - Single Ended - AC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp_AC, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = False, two_wires = True, coupling = 'AC', apply_cal = False)
	cal_load_SE_AC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_load_SE_AC.FilterData(51,3,51,3)
	cal_load_SE_AC.GetPoly(8,8,8,8)

if (cal_potentiostat_DIFF_DC):
	print('Potentiostat EIS - Differential - DC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = True, two_wires = True, coupling = 'DC', apply_cal = False)
	cal_load_DIFF_DC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_load_DIFF_DC.FilterData(51,3,51,3)
	cal_load_DIFF_DC.GetPoly(8,8,8,8)

if (cal_potentiostat_DIFF_AC):
	print('Potentiostat EIS - Differential - AC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp_AC, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = True, two_wires = True, coupling = 'AC', apply_cal = False)
	cal_load_DIFF_AC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_load_DIFF_AC.FilterData(51,3,51,3)
	cal_load_DIFF_AC.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_DC_high_gain):
	print('Galvanostat EIS - Single Ended - DC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = True)
	cal_galva_load_SE_DC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_load_SE_DC_HG.FilterData(51,3,51,3)
	cal_galva_load_SE_DC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_AC_high_gain):
	print('Galvanostat EIS - Single Ended - AC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = True,DC_feedback = True)
	cal_galva_load_SE_AC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_load_SE_AC_HG.FilterData(51,3,51,3)
	cal_galva_load_SE_AC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_DC_low_gain):
	print('Galvanostat EIS - Single Ended - DC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = False)
	cal_galva_load_SE_DC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_load_SE_DC_LG.FilterData(51,3,51,3)
	cal_galva_load_SE_DC_LG.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_AC_low_gain):
	print('Galvanostat EIS - Single Ended - AC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = False,DC_feedback = True)
	cal_galva_load_SE_AC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_load_SE_AC_LG.FilterData(51,3,51,3)
	cal_galva_load_SE_AC_LG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_DC_high_gain):
	print('Galvanostat EIS - Differential - DC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = True)
	cal_galva_load_DIFF_DC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_load_DIFF_DC_HG.FilterData(51,3,51,3)
	cal_galva_load_DIFF_DC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_AC_high_gain):
	print('Galvanostat EIS - Differential - AC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = True,DC_feedback = True)
	cal_galva_load_DIFF_AC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_load_DIFF_AC_HG.FilterData(51,3,51,3)
	cal_galva_load_DIFF_AC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_DC_low_gain):
	print('Galvanostat EIS - Differential - DC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = False)
	cal_galva_load_DIFF_DC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_load_DIFF_DC_LG.FilterData(51,3,51,3)
	cal_galva_load_DIFF_DC_LG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_AC_low_gain):
	print('Galvanostat EIS - Differential - AC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = False,DC_feedback = True)
	cal_galva_load_DIFF_AC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_load_DIFF_AC_LG.FilterData(51,3,51,3)
	cal_galva_load_DIFF_AC_LG.GetPoly(8,8,8,8)


print('======== Open Calibration ========')
print('- Remove the load')
input('- Press a Key when ready')

if (cal_potentiostat_SE_DC):
	print('Potentiostat EIS - Single Ended - DC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = False, two_wires = True, coupling = 'DC', apply_cal = False)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_open_SE_DC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_open_SE_DC.FilterData(51,3,51,3)
	cal_open_SE_DC.GetPoly(8,8,8,8)

if (cal_potentiostat_SE_AC):
	print('Potentiostat EIS - Single Ended - AC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp_AC, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = False, two_wires = True, coupling = 'AC', apply_cal = False)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_open_SE_AC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_open_SE_AC.FilterData(51,3,51,3)
	cal_open_SE_AC.GetPoly(8,8,8,8)

if (cal_potentiostat_DIFF_DC):
	print('Potentiostat EIS - Differential - DC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = True, two_wires = True, coupling = 'DC', apply_cal = False)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_open_DIFF_DC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_open_DIFF_DC.FilterData(51,3,51,3)
	cal_open_DIFF_DC.GetPoly(8,8,8,8)

if (cal_potentiostat_DIFF_AC):
	print('Potentiostat EIS - Differential - AC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp_AC, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = True, two_wires = True, coupling = 'AC', apply_cal = False)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_open_DIFF_AC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_open_DIFF_AC.FilterData(51,3,51,3)
	cal_open_DIFF_AC.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_DC_high_gain):
	print('Galvanostat EIS - Single Ended - DC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = True,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_open_SE_DC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_open_SE_DC_HG.FilterData(51,3,51,3)
	cal_galva_open_SE_DC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_AC_high_gain):
	print('Galvanostat EIS - Single Ended - AC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = True,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_open_SE_AC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_open_SE_AC_HG.FilterData(51,3,51,3)
	cal_galva_open_SE_AC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_DC_low_gain):
	print('Galvanostat EIS - Single Ended - DC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = False,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_open_SE_DC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_open_SE_DC_LG.FilterData(51,3,51,3)
	cal_galva_open_SE_DC_LG.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_AC_low_gain):
	print('Galvanostat EIS - Single Ended - AC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = False,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_open_SE_AC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_open_SE_AC_LG.FilterData(51,3,51,3)
	cal_galva_open_SE_AC_LG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_DC_high_gain):
	print('Galvanostat EIS - Differential - DC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = True,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_open_DIFF_DC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_open_DIFF_DC_HG.FilterData(51,3,51,3)
	cal_galva_open_DIFF_DC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_AC_high_gain):
	print('Galvanostat EIS - Differential - AC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = True,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_open_DIFF_AC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_open_DIFF_AC_HG.FilterData(51,3,51,3)
	cal_galva_open_DIFF_AC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_DC_low_gain):
	print('Galvanostat EIS - Differential - DC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = False,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_open_DIFF_DC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_open_DIFF_DC_LG.FilterData(51,3,51,3)
	cal_galva_open_DIFF_DC_LG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_AC_low_gain):
	print('Galvanostat EIS - Differential - AC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = False,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_open_DIFF_AC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_open_DIFF_AC_LG.FilterData(51,3,51,3)
	cal_galva_open_DIFF_AC_LG.GetPoly(8,8,8,8)

print('======== Short Calibration ========')
print('- Short the load')
input('- Press a Key when ready')

if (cal_potentiostat_SE_DC):
	print('Potentiostat EIS - Single Ended- DC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = False, two_wires = True, coupling = 'DC', apply_cal = False)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_short_SE_DC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_short_SE_DC.FilterData(51,3,51,3)
	cal_short_SE_DC.GetPoly(8,8,8,8)

if (cal_potentiostat_SE_AC):
	print('Potentiostat EIS - Single Ended- AC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp_AC, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = False, two_wires = True, coupling = 'AC', apply_cal = False)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_short_SE_AC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_short_SE_AC.FilterData(51,3,51,3)
	cal_short_SE_AC.GetPoly(8,8,8,8)

if (cal_potentiostat_DIFF_DC):
	print('Potentiostat EIS - Differential - DC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = True, two_wires = True, coupling = 'DC', apply_cal = False)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_short_DIFF_DC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_short_DIFF_DC.FilterData(51,3,51,3)
	cal_short_DIFF_DC.GetPoly(8,8,8,8)

if (cal_potentiostat_DIFF_AC):
	print('Potentiostat EIS - Differential - AC Coupled')
	freq, gain_mes, phase_mes = bm.potentiostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, V_amp = v_amp_AC, V_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
		differential = True, two_wires = True, coupling = 'AC', apply_cal = False)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_short_DIFF_AC = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_short_DIFF_AC.FilterData(51,3,51,3)
	cal_short_DIFF_AC.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_DC_high_gain):
	print('Galvanostat EIS - Single Ended - DC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_short_SE_DC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_short_SE_DC_HG.FilterData(51,3,51,3)
	cal_galva_short_SE_DC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_AC_high_gain):
	print('Galvanostat EIS - Single Ended - AC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = True,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_short_SE_AC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_short_SE_AC_HG.FilterData(51,3,51,3)
	cal_galva_short_SE_AC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_DC_low_gain):
	print('Galvanostat EIS - Single Ended - DC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = False)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_short_SE_DC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_short_SE_DC_LG.FilterData(51,3,51,3)
	cal_galva_short_SE_DC_LG.GetPoly(8,8,8,8)

if(cal_galvanostat_SE_AC_low_gain):
	print('Galvanostat EIS - Single Ended - AC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = False, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = False,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_short_SE_AC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_short_SE_AC_LG.FilterData(51,3,51,3)
	cal_galva_short_SE_AC_LG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_DC_high_gain):
	print('Galvanostat EIS - Differential - DC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_short_DIFF_DC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_short_DIFF_DC_HG.FilterData(51,3,51,3)
	cal_galva_short_DIFF_DC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_AC_high_gain):
	print('Galvanostat EIS - Differential - AC Coupled - High Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_high, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = True,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_short_DIFF_AC_HG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_short_DIFF_AC_HG.FilterData(51,3,51,3)
	cal_galva_short_DIFF_AC_HG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_DC_low_gain):
	print('Galvanostat EIS - Differential - DC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'DC', apply_cal = False,High_gain = False)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_short_DIFF_DC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_short_DIFF_DC_LG.FilterData(51,3,51,3)
	cal_galva_short_DIFF_DC_LG.GetPoly(8,8,8,8)

if(cal_galvanostat_DIFF_AC_low_gain):
	print('Galvanostat EIS - Differential - AC Coupled - Low Gain')
	freq, gain_mes, phase_mes = bm.galvanostat_EIS(fmin = fmin, fmax = fmax, n_pts = n_pts, I_amp = i_amp_low, I_offset = 0, settling_time = settling_time, NPeriods = NPeriods,
	differential = True, two_wires = True, coupling = 'AC', apply_cal = False,High_gain = False,DC_feedback = True)
	phase_mes = BM.unwrap_phase(phase_mes)
	cal_galva_short_DIFF_AC_LG = BM.MeasObj(gain_mes,phase_mes,freq)
	cal_galva_short_DIFF_AC_LG.FilterData(51,3,51,3)
	cal_galva_short_DIFF_AC_LG.GetPoly(8,8,8,8)


#Update calibration file
if (cal_potentiostat_SE_DC):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_open_SE_DC,data_short = cal_short_SE_DC,data_load = cal_load_SE_DC,
			excitation_mode = 'potentiostat',differential = False, coupling = 'DC')

if (cal_potentiostat_SE_AC):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_open_SE_AC,data_short = cal_short_SE_AC,data_load = cal_load_SE_AC,
			excitation_mode = 'potentiostat',differential = False, coupling = 'AC')


if (cal_potentiostat_DIFF_DC):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_open_DIFF_DC,data_short = cal_short_DIFF_DC,data_load = cal_load_DIFF_DC,
			excitation_mode = 'potentiostat',differential = True, coupling = 'DC')

if (cal_potentiostat_DIFF_AC):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_open_DIFF_AC,data_short = cal_short_DIFF_AC,data_load = cal_load_DIFF_AC,
			excitation_mode = 'potentiostat',differential = True, coupling = 'AC')

if(cal_galvanostat_SE_DC_high_gain):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_galva_open_SE_DC_HG,data_short = cal_galva_short_SE_DC_HG,data_load = cal_galva_load_SE_DC_HG,
		excitation_mode = 'galvanostat',differential = False, coupling = 'DC',high_current_gain = True)

if(cal_galvanostat_SE_AC_high_gain):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_galva_open_SE_AC_HG,data_short = cal_galva_short_SE_AC_HG,data_load = cal_galva_load_SE_AC_HG,
		excitation_mode = 'galvanostat',differential = False, coupling = 'AC',high_current_gain = True)

if(cal_galvanostat_SE_DC_low_gain):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_galva_open_SE_DC_LG,data_short = cal_galva_short_SE_DC_LG,data_load = cal_galva_load_SE_DC_LG,
		excitation_mode = 'galvanostat',differential = False, coupling = 'DC',high_current_gain = False)

if(cal_galvanostat_SE_AC_low_gain):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_galva_open_SE_AC_LG,data_short = cal_galva_short_SE_AC_LG,data_load = cal_galva_load_SE_AC_LG,
		excitation_mode = 'galvanostat',differential = False, coupling = 'AC',high_current_gain = False)

if(cal_galvanostat_DIFF_DC_high_gain):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_galva_open_DIFF_DC_HG,data_short = cal_galva_short_DIFF_DC_HG,data_load = cal_galva_load_DIFF_DC_HG,
		excitation_mode = 'galvanostat',differential = True, coupling = 'DC',high_current_gain = True)

if(cal_galvanostat_DIFF_AC_high_gain):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_galva_open_DIFF_AC_HG,data_short = cal_galva_short_DIFF_AC_HG,data_load = cal_galva_load_DIFF_AC_HG,
		excitation_mode = 'galvanostat',differential = True, coupling = 'AC',high_current_gain = True)

if(cal_galvanostat_DIFF_DC_low_gain):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_galva_open_DIFF_DC_LG,data_short = cal_galva_short_DIFF_DC_LG,data_load = cal_galva_load_DIFF_DC_LG,
		excitation_mode = 'galvanostat',differential = True, coupling = 'DC',high_current_gain = False)

if(cal_galvanostat_DIFF_AC_low_gain):
	bm.Update_OSLCal(Z_load = resistor,data_open=cal_galva_open_DIFF_AC_LG,data_short = cal_galva_short_DIFF_AC_LG,data_load = cal_galva_load_DIFF_AC_LG,
		excitation_mode = 'galvanostat',differential = True, coupling = 'AC',high_current_gain = False)

print("Open-Short-Load Calibration complete!")

bm.close()

n_plot = 0

def plot_cal(freq,cal_short,cal_load,cal_open,nplot,title):
	plt.figure(n_plot)
	plt.subplot(311)
	plt.semilogx(freq,cal_load.mag,label = 'Un-filtered')
	plt.semilogx(freq,cal_load.mag_filtered,label = 'Filtered')
	plt.semilogx(freq,cal_load.PlotMagPoly(freq),label = 'Fit')
	plt.grid()
	plt.xlabel('Frequency ($Hz$)')
	plt.ylabel('Impedance ($\Omega$)')
	plt.legend(title = 'Reference Load - ' + str(title))
	plt.subplot(312)
	plt.semilogx(freq,cal_load.phase,label = 'Un-filtered')
	plt.semilogx(freq,cal_load.phase_filtered,label = 'Filtered')
	plt.semilogx(freq,cal_load.PlotPhasePoly(freq),label = 'Fit')
	plt.grid()
	plt.xlabel('Frequency ($Hz$)')
	plt.ylabel('Phase (°)')
	plt.legend(title = 'Reference Load - ' + str(title))
	plt.subplot(313)
	plt.semilogx(freq,cal_load.getMagErrorFit(),label = 'Magnitude')
	plt.semilogx(freq,cal_load.getPhaseErrorFit(),label = 'Phase')
	plt.grid()
	plt.xlabel('Frequency ($Hz$)')
	plt.ylabel('Fit Error (%)')
	plt.legend(title = 'Fit Error - ' + str(title))

	plt.figure(n_plot+1)
	plt.subplot(311)
	plt.semilogx(freq,cal_short.mag,label = 'Un-filtered')
	plt.semilogx(freq,cal_short.mag_filtered,label = 'Filtered')
	plt.semilogx(freq,cal_short.PlotMagPoly(freq),label = 'Fit')
	plt.grid()
	plt.xlabel('Frequency ($Hz$)')
	plt.ylabel('Impedance ($\Omega$)')
	plt.legend(title = 'Short - ' + str(title))
	plt.subplot(312)
	plt.semilogx(freq,cal_short.phase,label = 'Un-filtered')
	plt.semilogx(freq,cal_short.phase_filtered,label = 'Filtered')
	plt.semilogx(freq,cal_short.PlotPhasePoly(freq),label = 'Fit')
	plt.grid()
	plt.xlabel('Frequency ($Hz$)')
	plt.ylabel('Phase (°)')
	plt.legend(title = 'Short - ' + str(title))
	plt.subplot(313)
	plt.semilogx(freq,cal_short.getMagErrorFit(),label = 'Magnitude')
	plt.semilogx(freq,cal_short.getPhaseErrorFit(),label = 'Phase')
	plt.grid()
	plt.xlabel('Frequency ($Hz$)')
	plt.ylabel('Fit Error (%)')
	plt.legend(title = 'Fit Error - ' + str(title))

	#Plot Calibration Data on Open load in Voltage - Single Ended  - DC
	plt.figure(n_plot+2)
	plt.subplot(311)
	plt.loglog(freq,cal_open.mag,label = 'Un-filtered')
	plt.loglog(freq,cal_open.mag_filtered,label = 'Filtered')
	plt.loglog(freq,cal_open.PlotMagPoly(freq),label = 'Fit')
	plt.grid()
	plt.xlabel('Frequency ($Hz$)')
	plt.ylabel('Impedance ($\Omega$)')
	plt.legend(title = 'Open - ' + str(title))
	plt.subplot(312)
	plt.semilogx(freq,cal_open.phase,label = 'Un-filtered')
	plt.semilogx(freq,cal_open.phase_filtered,label = 'Filtered')
	plt.semilogx(freq,cal_open.PlotPhasePoly(freq),label = 'Fit')
	plt.grid()
	plt.xlabel('Frequency ($Hz$)')
	plt.ylabel('Phase (°)')
	plt.legend(title = 'Open - ' + str(title))
	plt.subplot(313)
	plt.semilogx(freq,cal_open.getMagErrorFit(),label = 'Magnitude')
	plt.semilogx(freq,cal_open.getPhaseErrorFit(),label = 'Phase')
	plt.grid()
	plt.xlabel('Frequency ($Hz$)')
	plt.ylabel('Fit Error (%)')
	plt.legend(title = 'Fit Error - ' + str(title))
	return(n_plot+3)


if (plot_cal_potentiostat_SE_DC and cal_potentiostat_SE_DC):
	n_plot  = plot_cal(freq,cal_short_SE_DC,cal_load_SE_DC,cal_open_SE_DC,n_plot,title = 'Potentiostat EIS - Single Ended - DC Coupled')

if (plot_cal_potentiostat_SE_AC and cal_potentiostat_SE_AC):
	n_plot  = plot_cal(freq,cal_short_SE_AC,cal_load_SE_AC,cal_open_SE_AC,n_plot,title = 'Potentiostat EIS - Single Ended - AC Coupled')

if (plot_cal_potentiostat_DIFF_DC and cal_potentiostat_DIFF_DC):
	n_plot  = plot_cal(freq,cal_short_DIFF_DC,cal_load_DIFF_DC,cal_open_DIFF_DC,n_plot,title = 'Potentiostat EIS - Differential - DC Coupled')

if (plot_cal_potentiostat_DIFF_AC and cal_potentiostat_DIFF_AC):
	n_plot  = plot_cal(freq,cal_short_DIFF_AC,cal_load_DIFF_AC,cal_open_DIFF_AC,n_plot,title = 'Potentiostat EIS - Differential - AC Coupled')

if (plot_galvanostat_SE_DC_high_gain and cal_galvanostat_SE_DC_high_gain):
	n_plot  = plot_cal(freq,cal_galva_short_SE_DC_HG,cal_galva_load_SE_DC_HG,cal_galva_open_SE_DC_HG,n_plot,title = 'Galvanostat EIS - Single Ended - DC Coupled - High Gain')

if (plot_galvanostat_SE_DC_low_gain and cal_galvanostat_SE_DC_low_gain):
	n_plot  = plot_cal(freq,cal_galva_short_SE_DC_LG,cal_galva_load_SE_DC_LG,cal_galva_open_SE_DC_LG,n_plot,title = 'Galvanostat EIS - Single Ended - DC Coupled - Low Gain')

if (plot_galvanostat_SE_AC_high_gain and cal_galvanostat_SE_AC_high_gain):
	n_plot  = plot_cal(freq,cal_galva_short_SE_AC_HG,cal_galva_load_SE_AC_HG,cal_galva_open_SE_AC_HG,n_plot,title = 'Galvanostat EIS - Single Ended - AC Coupled - High Gain')

if (plot_galvanostat_SE_AC_low_gain and cal_galvanostat_SE_AC_low_gain):
	n_plot  = plot_cal(freq,cal_galva_short_SE_AC_LG,cal_galva_load_SE_AC_LG,cal_galva_open_SE_AC_LG,n_plot,title = 'Galvanostat EIS - Single Ended - AC Coupled - Low Gain')

if (plot_galvanostat_DIFF_DC_high_gain and cal_galvanostat_DIFF_DC_high_gain):
	n_plot  = plot_cal(freq,cal_galva_short_DIFF_DC_HG,cal_galva_load_DIFF_DC_HG,cal_galva_open_DIFF_DC_HG,n_plot,title = 'Galvanostat EIS - Differential - DC Coupled - High Gain')

if (plot_galvanostat_DIFF_DC_low_gain and cal_galvanostat_DIFF_DC_low_gain):
	n_plot  = plot_cal(freq,cal_galva_short_DIFF_DC_LG,cal_galva_load_DIFF_DC_LG,cal_galva_open_DIFF_DC_LG,n_plot,title = 'Galvanostat EIS - Differential - DC Coupled - Low Gain')

if (plot_galvanostat_DIFF_AC_high_gain and cal_galvanostat_DIFF_AC_high_gain):
	n_plot  = plot_cal(freq,cal_galva_short_DIFF_AC_HG,cal_galva_load_DIFF_AC_HG,cal_galva_open_DIFF_AC_HG,n_plot,title = 'Galvanostat EIS - Differential - AC Coupled - High Gain')

if (plot_galvanostat_DIFF_AC_low_gain and cal_galvanostat_DIFF_AC_low_gain):
	n_plot  = plot_cal(freq,cal_galva_short_DIFF_AC_LG,cal_galva_load_DIFF_AC_LG,cal_galva_open_DIFF_AC_LG,n_plot,title = 'Galvanostat EIS - Differential - AC Coupled - Low Gain')




plt.show()









