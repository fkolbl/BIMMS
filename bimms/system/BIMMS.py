"""
    Python library to use BIMMS measurement setup
    Authors: Florian Kolbl / Louis Regnacq
    (c) ETIS - University Cergy-Pontoise
        IMS - University of Bordeaux
        CNRS

    Requires:
        Python 3.6 or higher
        Analysis_Instrument - class handling Analog Discovery 2 (Digilent)

    Dev notes:
        - LR: in BIMMS_constants, IO15 change with IO7 because hardware issue.  
        - LR: TIA relay modified too

"""
import sys
import os
import faulthandler
import numpy as np
import os
import json
from scipy.signal import butter, lfilter
from time import sleep

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .BIMMSconfig import BIMMSconfig
from .BIMMScalibration import BIMMScalibration
from ..measure.Measure import Measure

### for debug
faulthandler.enable()
### verbosity of the verbosity
verbose = True

##############################
## CLASS FOR BIMMS HANDLING ##
##############################
class BIMMS(BIMMSconfig):
    def __init__(self, bimms_id=None, serialnumber=None):
        super().__init__(bimms_id=bimms_id, serialnumber=serialnumber)
        self.measures = []
        self.results

    def attach_calibrator(self, calibrator):
        pass

    def attach_measure(self, m : Measure):
        self.measures += m


    def callibrate(self):
        pass



    def check_measures_config():
        pass

    def measure(self):
        self.check_config()
        self.set_config()
        for m in self.measures:
            m.measure(self)


    #########################
    ## Measurement Methods ##
    #########################
    def impedance_spectroscopy(
        self,
        fmin=1e2,
        fmax=1e7,
        n_pts=501,
        amp=1,
        offset=0,
        settling_time=0.1,
        NPeriods=32,
        Vrange_CH1=1.0,
        Vrange_CH2=1.0,
        offset_CH1=0.0,
        offset_CH2=0.0,
    ):
        """
        docstring for the impedance spectrocopy
        """
        # perform bode measurement
        if 2 * Vrange_CH1 > 5.0:
            Vrange_CH1 = 50.0
        else:
            Vrange_CH1 = 5.0

        if 2 * Vrange_CH2 > 5.0:
            Vrange_CH2 = 50.0
        else:
            Vrange_CH2 = 5.0

        freq, gain_mes, phase_mes, gain_ch1 = self.ad2.bode_measurement(
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
        return freq, gain_mes, phase_mes

    def galvanostat_EIS(
        self,
        fmin=1e2,
        fmax=1e7,
        n_pts=501,
        I_amp=1,
        I_offset=0,
        settling_time=0.1,
        NPeriods=32,
        voltage_gain=1,
        current_gain=1,
        V_range=1.0,
        V_offset=0.0,
        differential=True,
        High_gain=True,
        two_wires=True,
        coupling="DC",
        DC_feedback=False,
        apply_cal=True,
    ):
        self.set_galvanostat_EIS_config(
            differential=differential,
            two_wires=two_wires,
            High_gain=High_gain,
            coupling=coupling,
            DC_feedback=DC_feedback,
            voltage_gain=voltage_gain,
            current_gain=current_gain,
        )

        if High_gain:
            amp = I_amp / self.Gain_High_current
            offset = I_offset / self.Gain_High_current
        else:
            amp = I_amp / self.Gain_Low_current
            offset = I_offset / self.Gain_Low_current

        self.ad2.configure_network_analyser()
        Vrange_CH1 = V_range * 1.5
        offset_CH1 = V_offset * 1.5
        Vrange_CH2 = 1.0
        offset_CH2 = I_offset * 1.5

        freq, gain_mes, phase_mes = self.impedance_spectroscopy(
            fmin=fmin,
            fmax=fmax,
            n_pts=n_pts,
            amp=amp,
            offset=offset,
            settling_time=settling_time,
            NPeriods=NPeriods,
            Vrange_CH1=Vrange_CH1,
            Vrange_CH2=1.0,
            offset_CH1=offset_CH1,
            offset_CH2=0.0,
        )

        mag = gain_mes * self.Gain_TIA
        phase = phase_mes - 180

        if apply_cal:
            freq, mag, phase = self.apply_OSLCal(
                freq,
                mag,
                phase,
                excitation_mode="galvanostat",
                differential=differential,
                coupling=coupling,
                high_current_gain=High_gain,
            )

        return freq, mag, phase

    def potentiostat_EIS(
        self,
        fmin=1e2,
        fmax=1e7,
        n_pts=501,
        V_amp=1,
        V_offset=0,
        settling_time=0.1,
        NPeriods=32,
        voltage_gain=1,
        current_gain=1,
        differential=True,
        two_wires=True,
        coupling="DC",
        apply_cal=True,
    ):
        self.set_potentiostat_EIS_config(
            differential=differential,
            two_wires=two_wires,
            coupling=coupling,
            voltage_gain=voltage_gain,
            current_gain=current_gain,
        )

        if differential:
            amp = V_amp / self.Gain_Voltage_DIFF
            offset = V_offset / self.Gain_Voltage_DIFF
        else:
            amp = V_amp / self.Gain_Voltage_SE
            offset = V_offset / self.Gain_Voltage_SE

        self.ad2.configure_network_analyser()
        Vrange_CH1 = V_amp * 1.5
        offset_CH1 = V_offset * 1.5

        freq, gain_mes, phase_mes = self.impedance_spectroscopy(
            fmin=fmin,
            fmax=fmax,
            n_pts=n_pts,
            amp=amp,
            offset=offset,
            settling_time=settling_time,
            NPeriods=NPeriods,
            Vrange_CH1=Vrange_CH1,
            Vrange_CH2=1.0,
            offset_CH1=offset_CH1,
            offset_CH2=0.0,
        )

        mag = gain_mes * self.Gain_TIA
        phase = phase_mes - 180

        if apply_cal:
            freq, mag, phase = self.apply_OSLCal(
                freq,
                mag,
                phase,
                excitation_mode="potentiostat",
                differential=differential,
                coupling=coupling,
            )

        return freq, mag, phase

    def cyclic_voltametry(
        self,
        period,
        V_amp,
        n_delay,
        n_avg,
        filter=True,
        mode="two_points",
        coupling="DC",
        differential=True,
    ):
        N_pts = int(8192)
        fs = (1 / (period + 0.12 * period)) * N_pts
        self.set_cyclic_voltametry_config(
            mode=mode, coupling=coupling, differential=differential
        )
        if 2 * V_amp >= 5.0:
            vrange1 = 50.0
        else:
            vrange1 = 5.0
        vrange2 = 1

        if differential:
            V_awg = V_amp / self.Gain_Voltage_DIFF
        else:
            V_awg = V_amp / self.Gain_Voltage_SE

        trig_th = 0
        self.ad2.in_set_channel(channel=0, Vrange=vrange1, Voffset=0.0)
        self.ad2.in_set_channel(channel=1, Vrange=vrange2, Voffset=0.0)
        self.ad2.set_Chan_trigger(
            0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left"
        )  # Improvement: use internal trigger instead
        self.ad2.triangle(channel=0, freq=1 / period, amp=V_awg, offset=0.0)
        if n_delay:
            print("Wait for settling...")
            sleep(n_delay * period)
        print("Measuring...")
        t = self.ad2.set_acq(freq=fs, samples=N_pts)
        voltage, current = self.ad2.acq()
        if n_avg > 0:
            current_array = []
            voltage_array = []
            for i in range(n_avg):
                print("Average: " + str(i + 1))
                self.ad2.set_Chan_trigger(
                    0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left"
                )  # Improvement: use internal trigger instead
                t = self.ad2.set_acq(freq=fs, samples=N_pts)
                voltage, current = self.ad2.acq()
                voltage_array.append(voltage)
                current_array.append(current)
            voltage_array = np.array(voltage_array)
            current_array = np.array(current_array)
            voltage = np.mean(voltage_array, axis=0)
            current = np.mean(current_array, axis=0)
        else:
            self.ad2.set_Chan_trigger(
                0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left"
            )  # Improvement: use internal trigger instead
            t = self.ad2.set_acq(freq=fs, samples=N_pts)
            voltage, current = self.ad2.acq()
        if filter:
            cutoff = 10 * (1 / period)
            order = 2
            nyq = 0.5 * fs
            normal_cutoff = cutoff / nyq
            b, a = butter(order, normal_cutoff, btype="low", analog=False)
            current = lfilter(b, a, current)
            voltage = lfilter(b, a, voltage)
        t = t - 0.05 * period
        idx = np.where(t <= 0)
        t = np.delete(t, idx)
        voltage = np.delete(voltage, idx)
        current = np.delete(current, idx)
        print("Done!")

        return (t, voltage, -current / self.Gain_TIA)

    def cyclic_amperometry(
        self,
        period,
        I_amp,
        V_range,
        n_delay,
        n_avg,
        filter=True,
        mode="two_points",
        coupling="DC",
        differential=True,
        High_gain=True,
        DC_feedback=False,
    ):
        N_pts = int(8192)
        fs = (1 / (period + 0.12 * period)) * N_pts
        self.set_cyclic_amperometry_config(
            mode=mode,
            coupling=coupling,
            differential=differential,
            High_gain=High_gain,
            DC_feedback=DC_feedback,
        )

        if 2 * V_range >= 5.0:
            vrange1 = 50.0
        else:
            vrange1 = 5.0
        vrange2 = 1

        if High_gain:
            amp = I_amp / self.Gain_High_current
        else:
            amp = I_amp / self.Gain_Low_current

        trig_th = 0

        self.ad2.in_set_channel(channel=0, Vrange=vrange1, Voffset=0)
        self.ad2.in_set_channel(channel=1, Vrange=vrange2, Voffset=0)
        self.ad2.triangle(channel=0, freq=1 / period, amp=amp, offset=0)
        if n_delay:
            print("Wait for settling...")
            sleep(n_delay * period)
        print("Measuring...")
        t = self.ad2.set_acq(freq=fs, samples=N_pts)
        voltage, current = self.ad2.acq()
        if n_avg > 0:
            current_array = []
            voltage_array = []
            for i in range(n_avg):
                print("Average: " + str(i + 1))
                self.ad2.set_Chan_trigger(
                    0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left"
                )  # Improvement: use internal trigger instead
                t = self.ad2.set_acq(freq=fs, samples=N_pts)
                voltage, current = self.ad2.acq()
                voltage_array.append(voltage)
                current_array.append(current)
            voltage_array = np.array(voltage_array)
            current_array = np.array(current_array)
            voltage = np.mean(voltage_array, axis=0)
            current = np.mean(current_array, axis=0)
        else:
            self.ad2.set_Chan_trigger(
                0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left"
            )  # Improvement: use internal trigger instead
            t = self.ad2.set_acq(freq=fs, samples=N_pts)
            voltage, current = self.ad2.acq()
        if filter:
            cutoff = 10 * (1 / period)
            order = 2
            nyq = 0.5 * fs
            normal_cutoff = cutoff / nyq
            b, a = butter(order, normal_cutoff, btype="low", analog=False)
            current = lfilter(b, a, current)
            voltage = lfilter(b, a, voltage)
        t = t - 0.05 * period
        idx = np.where(t <= 0)
        t = np.delete(t, idx)
        voltage = np.delete(voltage, idx)
        current = np.delete(current, idx)
        print("Done!")

        return (t, voltage, -current / self.Gain_TIA)

    def AW_Potentiostat(self, something):
        pass

    def AW_Galvanostat(self, something):
        pass
