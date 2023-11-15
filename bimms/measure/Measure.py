
import numpy as np

from ..backend.BIMMS_Class import BIMMS_class, abstractmethod
from ..system.BIMMScalibration import BIMMScalibration
from ..utils import constants as BIMMScst


class Measure(BIMMS_class):
    """
    A generic class of measurement from wchich every measurment type should inherit
    """
    @abstractmethod
    def __init__(self, ID=0):
        super().__init__()
        self.ID = ID
        self.raw = False

    def set_parameters(self,**kawrgs):
        for key in kawrgs:
            if key in self.__dict__:
                self.__dict__[key] == kawrgs[dict]

    def get_parameters(self):
        return self.__dict__


    def measure(self, BS: BIMMScalibration):
        pass


class EIS(Measure):
    """
    
    """
    def __init__(self, fmin=1e3, fmax=1e7, n_pts=101, settling_time=0.001, NPeriods=8, ID=0):
        super().__init__(ID=ID)
        self.fmin = fmin
        self.fmax = fmax
        self.n_pts = n_pts
        self.settling_time = settling_time
        self.NPeriods = NPeriods

    def set_fmin(self, f):
        self.set_parameters(fmin=f)

    def set_fmax(self, f):
        self.set_parameters(fmax=f)

    def set_n_pts(self, N):
        self.set_parameters(n_pts=N)

    def set_settling_time(self, t):
        self.set_parameters(settling_time=t)

    def set_NPeriods(self, N):
        self.set_parameters(NPeriods=N)

    def measure(self, BS: BIMMScalibration):
        BS.ad2.configure_network_analyser()	#need to be checked
        freq, gain_mes, phase_mes, gain_ch1 = BS.ad2.bode_measurement(
            self.fmin,
            self.fmax,
            n_points=self.n_pts,
            dB=False,
            offset=BS.awg_offset,
            deg=True,
            amp=BS.awg_amp,
            settling_time=self.settling_time,
            Nperiods=self.NPeriods,
            verbose=BS.verbose,
        )

        if not self.raw:
            mag, phase = BS.bode2impendance(freq, gain_mes, phase_mes, gain_ch1)

        return freq, mag, phase

class TemporalSingleFrequency(Measure):
    def __init__(self,freq=1e3, phase=0, symmetry=50, Nperiod=8, delay=0, ID=0):
        super().__init__(ID=ID)
        self.freq = freq
        self.phase = phase
        self.symmetry = symmetry
        self.Nperiod = Nperiod
        self.delay = delay

    def set_freq(self, f):
        self.set_parameters(freq=f)

    def set_phase(self, phase):
        self.set_parameters(phase=phase)

    def set_symmetry(self, symmetry):
        self.set_parameters(symmetry=symmetry)

    def set_Nperiod(self, N):
        self.set_parameters(Nperiod=N)

    def set_delay(self, delay):
        self.set_parameters(delay=delay)


    def measure(self, BS: BIMMScalibration):
        # set the generators
        BS.AWG_sine(freq=self.freq, amp=BS.awg_amp,activate = False,offset = BS.awg_offset, phase=self.phase,
                            symmetry=self.symmetry)
        Fs_max = BS.AD2_input_Fs_max
        Npts = BS.AD2_input_buffer_size
        fs = self.freq*Npts/self.Nperiod

        while (fs>Fs_max):
            Npts-=1
            fs = self.freq*Npts/self.Nperiod
        # set the triger to triger source
        BS.Set_AWG_trigger(delay=self.delay)

        # set acquisition
        t = BS.set_acquistion(fs, Npts)

        # perform the generation/acquisition
        BS.AWG_enable(True)
        chan1, chan2 = BS.get_input_data()
        BS.AWG_enable(False)

        if not self.raw:
            chan1, chan2 = BS.Scope2calibration(chan1, chan2, t, self.freq)
        return(t,chan1,chan2)

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


