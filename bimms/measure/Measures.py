
import numpy as np
from ..utils import constants as BIMMScst

#Need update
def Measure_Offset(BS,channel = 1, gain_IA = 1, acq_duration = 1, Nsample = 8192,coupling = 'DC', Vrange = 1, Voffset = 0):
    sampling_freq = Nsample/acq_duration
    BS.set_STM32_idle()
    if (channel == 1):
        BS.set_recording_channel_1(coupling = coupling, gain = gain_IA)
        BS.ad2.in_set_channel(channel=0, Vrange=Vrange, Voffset=Voffset)
    else:
        BS.set_recording_channel_2(coupling = coupling, gain = gain_IA)
        BS.ad2.in_set_channel(channel = 1, Vrange=Vrange, Voffset=Voffset)
    BS.set_config()
    BS.ad2.set_Auto_chan_trigger(0, timeout=0.1, type="Rising", ref="center")
    t = BS.ad2.set_acq(freq=sampling_freq, samples=Nsample)
    dat0, dat1 = BS.ad2.acq()
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
    BS.ad2.configure_network_analyser()	#need to be checked
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

	freq, gain_mes, phase_mes, gain_ch1 = BS.ad2.bode_measurement(
		fmin,
		fmax,
		n_points=n_pts,
		dB=False,
		offset=offset,
		deg=True,
		amp=0.1,
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
	BS.AWG_sine(freq=Freq, amp=amp_AWG,activate = False,offset = AWG_offset, phase = Phase,
				   		symmetry = Symmetry)

    Fs_max = BS.AD2_input_Fs_max
    Npts = BS.AD2_input_buffer_size
    fs = Freq*Npts/Nperiod

    while (fs>Fs_max):
        Npts-=1
        fs = Freq*Npts/Nperiod

    BS.Set_AWG_trigger(delay=Delay)
    t = BS.set_acquistion(fs, Npts)

	BS.AWG_enable(True)
	chan1, chan2 = BS.get_input_data()
	
	BS.AWG_enable(False)

    #Here --> convert chan1, chan2 with calibration data

    return(t,chan1,chan2)
    #pass


