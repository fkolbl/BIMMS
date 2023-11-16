
import numpy as np

from ..backend.BIMMS_Class import BIMMS_class, abstractmethod
from ..system.BIMMScalibration import BIMMScalibration
from ..utils import constants as BIMMScst
import matplotlib.pyplot as plt

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
            mag, phase = BS.bode2impendance(gain_mes, phase_mes, freq, gain_ch1)

        results = {'freq':freq, 'mag':mag, 'phase':phase}
        return results

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

        results = {'t':t, 'chan1':chan1, 'chan2':chan2}
        return results

class Offset(Measure):
    def __init__(self,acq_duration = 1, Navg = 0, ID=0):
        super().__init__(ID=ID)
        self.acq_duration = acq_duration
        self.Navg = Navg

    def set_acq_duration(self, acq_duration):
        self.set_parameters(acq_duration=acq_duration)

    def set_Navg(self, Navg):
        self.set_parameters(Navg=Navg)
                            
    def measure(self, BS: BIMMScalibration):
                            
        BS.AWG_sine(freq=1e3, amp=0,activate = True)  #Dummy sine waveform
        BS.Set_AUTO_trigger()
                            
        Npts = BS.AD2_input_buffer_size
        fs = Npts/self.acq_duration
        t = BS.set_acquistion(fs=fs, size=Npts)
        ch1_offset = []
        ch2_offset = []
        if (BS.verbose):
            print("Measuring Offset...")
        for n in range (self.Navg):
            ch1,ch2 = BS.get_input_data()
            ch1_offset.append(np.mean(ch1))
            ch2_offset.append(np.mean(ch2))
        
        if (BS.verbose):
            print("Done!")
        if (self.Navg>1):
            ch1_offset = np.mean(ch1_offset)
            ch2_offset = np.mean(ch2_offset)
        else:
            ch1_offset = ch1_offset[0]
            ch2_offset = ch2_offset[0]          
        
        if not self.raw:
            ch1_offset, ch2_offset = BS.Scope2calibration(ch1_offset, ch2_offset, [0])

        results = {
            'ch1_offset':ch1_offset, 'ch2_offset':ch2_offset}
        return results


class Bode(Measure):
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

        gain_ch2 = gain_ch1/gain_mes
        results = {'freq':freq, 'mag_ch1':gain_ch1,'mag_ch2':gain_ch2, 'phase':phase_mes}
