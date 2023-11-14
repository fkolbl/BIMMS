
import numpy as np
from ..utils import constants as BIMMScst

#Need update
def Measure_Offset(BS,channel = 1, gain_IA = 1, acq_duration = 1, Nsample = 8192,coupling = 'DC', Vrange = 1, Voffset = 0):
	sampling_freq = Nsample/acq_duration
	BS.set_STM32_idle()
	if (channel == 1):
		BS.set_recording_channel_1(coupling = coupling, gain = gain_IA)
		BS.interface.in_set_channel(channel=0, Vrange=Vrange, Voffset=Voffset)
	else:
		BS.set_recording_channel_2(coupling = coupling, gain = gain_IA)
		BS.interface.in_set_channel(channel = 1, Vrange=Vrange, Voffset=Voffset)
	BS.set_config()
	BS.interface.set_Auto_chan_trigger(0, timeout=0.1, type="Rising", ref="center")
	t = BS.interface.set_acq(freq=sampling_freq, samples=Nsample)
	dat0, dat1 = BS.interface.acq()
	if(channel == 1):
		offset = np.mean(dat0)
	else :
		offset = np.mean(dat1)
	return(offset)

def TemporalAcquistion(BS):
	pass

def EIS(BS,fmin=1e2,fmax=1e7,n_pts=501,offset=0,settling_time=0.1,NPeriods=32,apply_cal=True):

	BS.set_config()

	GAIN = 1	
	amp_stim= 0.1								#need to be changed with calibrated or uncalibrated gain
	Gain_TIA = 100								#need to be changed with calibrated or uncalibrated gain
	amp_AWG =  amp_stim*GAIN 					#need to be changed with calibrated or uncalibrated gain
	BS.interface.configure_network_analyser()	#need to be checked
	offset_AWG = offset*GAIN

	#TO CHECK!!
	verbose = True
	offset_CH1 = 0
	offset_CH2 = 0
	Vrange_CH1 = 1
	Vrange_CH2 = 1


	if 2 * Vrange_CH1 > 5.0:
		Vrange_CH1 = 50.0
	else:
		Vrange_CH1 = 5.0

	if 2 * Vrange_CH2 > 5.0:
		Vrange_CH2 = 50.0
	else:
		Vrange_CH2 = 5.0

	freq, gain_mes, phase_mes, gain_ch1 = BS.interface.bode_measurement(
		fmin,
		fmax,
		n_points=n_pts,
		dB=False,
		offset=offset,
		deg=True,
		amp=amp,
		settling_time=settling_time,
		Nperiods=NPeriods,
		Vrange_CH1=Vrange_CH1,
		Vrange_CH2=Vrange_CH2,
		offset_CH1=offset_CH1,
		offset_CH2=offset_CH2,
		verbose=verbose,
	)

	mag = gain_mes * Gain_TIA	
	phase = phase_mes - 180
	if apply_cal:
		print("Calibration not Implemented")

	return freq, mag, phase


def SingleFrequency(BS,xxx):
	pass


def TemporalSingleFrequency(BS,amp,Freq,Phase = 0,Symmetry = 50,Nperiod=1,Delay = 0):

	GAIN = 1	
	amp_stim= amp								#need to be changed with calibrated or uncalibrated gain
	Gain_TIA = 100								#need to be changed with calibrated or uncalibrated gain
	amp_AWG =  amp_stim*GAIN 					#need to be changed with calibrated or uncalibrated gain
	AWG_offset = 0.02 								#in calibration

	AD2_VRO_range = 5.0							#in calibration
	AD2_VRO_offset = 0.0
	AD2_IRO_range = 5.0
	AD2_IRO_offset = 0.0

	
	# set the generators
	BS.interface.sine(channel=BIMMScst.AD2_AWG_ch, freq=Freq, amp=amp_AWG,activate = False,offset = AWG_offset, phase = Phase,
				   		symmetry = Symmetry)

    #set acquisition parameters
	#BS.interface.in_set_channel(channel=BIMMScst.AD2_VRO_ch, Vrange=AD2_VRO_range, Voffset=AD2_VRO_offset)							 #to update with AD2config 
	#BS.interface.in_set_channel(channel=BIMMScst.AD2_IRO_ch, Vrange=AD2_IRO_range, Voffset=AD2_IRO_offset)							 #to update with AD2config 

	#max Fs
	Fs_max = BS.interface.in_frequency_info()[-1]
	Input_Npts_max = BS.interface.in_buffer_size_info()[-1]
	Npts = Input_Npts_max
	fs = Freq*Input_Npts_max/Nperiod

	n_pts = ()

	while (fs>Fs_max):
		Npts-=1
		fs = Freq*Input_Npts_max/Nperiod

	BS.interface.set_AWG_trigger(BIMMScst.AD2_AWG_ch,type="Rising",ref="left border", position=Delay)
	t = BS.interface.set_acq(freq=fs, samples=Npts)
	fs_set  =  BS.interface.in_sampling_freq_get()

	BS.interface.out_channel_on(BIMMScst.AD2_AWG_ch)
	dat0, dat1 = BS.interface.acq()
	BS.interface.out_channel_off(BIMMScst.AD2_AWG_ch)
	return(t,dat0,dat1)
	#pass


