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
import andi as ai
import faulthandler
import numpy as np
import os
import json
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, butter, lfilter, freqz
from time import sleep

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


from .BIMMSconfig import BIMMSconfig
from ..utils import constants as cst

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

        # Try to load DC calibration file
        if self.Load_DCCal():
            self.DCCalibration = True
            if verbose:
                print("DC Calibration data successfully loaded.")
        else:
            self.DCCalibration = False
            if verbose:
                print("WARNING: DC Calibration does not exist.")
                print("Estimated current, voltage and impedance will be innacurate.")
                print("Consider running DC calibration script.")

        if self.Load_OSLCal() == 12:
            self.OSH_all_cal = 1
            if verbose:
                print("All Open-Short-Load calibration data loaded.")
            self.OSLCalibration = True
        elif self.Load_OSLCal() > 0:
            self.OSLCalibration = True
            if verbose:
                print("WARNING: Some Open-Short-Load Calibration data are missing.")
        else:
            if verbose:
                print("WARNING: Open-Short-Load Calibration does not exist.")
                print("Estimated impedance will be innacurate.")
                print("Consider running Open-Short-Load calibration script.")
            self.OSLCalibration = False


    def Load_DCCal(self):
        if not os.path.exists(self.cal_folder):
            if verbose:
                return 0
        else:
            file_name = self.cal_folder + "DCCal_BIMMS_" + str(self.ID) + ".json"
            try:
                json_file = open(file_name)
                self.DCCalFile = json.load(json_file)
                json_file.close()
                if self.DCCalFile["BIMMS_SERIAL"] != self.ID:
                    return 0
            except:
                return 0
        if self.DCCalFile:
            if "gain_TIA" in self.DCCalFile:
                self.Gain_TIA = self.DCCalFile["gain_TIA"]
            if "gain_voltage_SE" in self.DCCalFile:
                self.Gain_Voltage_SE = self.DCCalFile["gain_voltage_SE"]
            if "gain_voltage_DIFF" in self.DCCalFile:
                self.Gain_Voltage_DIFF = self.DCCalFile["gain_voltage_DIFF"]
            if "low_gain_current" in self.DCCalFile:
                self.Gain_Low_current = self.DCCalFile["low_gain_current"]
            if "high_gain_current" in self.DCCalFile:
                self.Gain_High_current = self.DCCalFile["high_gain_current"]
        return 1

    def Load_OSLCal(self):
        if not os.path.exists(self.cal_folder):
            return 0
        else:
            file_name = (
                "./" + self.cal_folder + "/OSLCal_BIMMS_" + str(self.ID) + ".json"
            )
            try:
                json_file = open(file_name)
                self.OSLCalFile = json.load(json_file)
                if self.OSLCalFile["BIMMS_SERIAL"] != self.ID:
                    return 0
            except:
                return 0

        n_cal_data = 0
        if self.OSLCalFile["potentiostat"]["SE"]["DC"] != {}:
            n_cal_data = n_cal_data + 1
        if self.OSLCalFile["potentiostat"]["SE"]["AC"] != {}:
            n_cal_data = n_cal_data + 1
        if self.OSLCalFile["potentiostat"]["differential"]["DC"] != {}:
            n_cal_data = n_cal_data + 1
        if self.OSLCalFile["potentiostat"]["differential"]["AC"] != {}:
            n_cal_data = n_cal_data + 1
        if self.OSLCalFile["galvanostat"]["SE"]["High_gain"]["DC"] != {}:
            n_cal_data = n_cal_data + 1
        if self.OSLCalFile["galvanostat"]["SE"]["High_gain"]["AC"] != {}:
            n_cal_data = n_cal_data + 1
        if self.OSLCalFile["galvanostat"]["SE"]["Low_gain"]["DC"] != {}:
            n_cal_data = n_cal_data + 1
        if self.OSLCalFile["galvanostat"]["SE"]["Low_gain"]["AC"] != {}:
            n_cal_data = n_cal_data + 1
        if self.OSLCalFile["galvanostat"]["differential"]["High_gain"]["DC"] != {}:
            n_cal_data = n_cal_data + 1
        if self.OSLCalFile["galvanostat"]["differential"]["High_gain"]["AC"] != {}:
            n_cal_data = n_cal_data + 1
        if self.OSLCalFile["galvanostat"]["differential"]["Low_gain"]["DC"] != {}:
            n_cal_data = n_cal_data + 1
        if self.OSLCalFile["galvanostat"]["differential"]["Low_gain"]["AC"] != {}:
            n_cal_data = n_cal_data + 1
        return n_cal_data

    def Update_DCCal(self, measured_gain, value):
        if self.DCCalibration == 0:  # Create Cal file if does not exist
            if verbose:
                print(
                    "Creating new DC Calibration file for BIMMS " + str(self.ID) + "."
                )
            if not os.path.exists(self.cal_folder):
                os.makedirs(self.cal_folder)
            self.DCCalFile = {}
            self.DCCalFile["BIMMS_SERIAL"] = self.ID

        self.DCCalFile[measured_gain] = value

        outfile_name = "./" + self.cal_folder + "/DCCal_BIMMS_" + str(self.ID) + ".json"
        outfile = open(outfile_name, "w")
        json.dump(self.DCCalFile, outfile)
        outfile.close()
        self.DCCalibration = True
        self.Load_DCCal()

    def Create_OSLCal(self):
        if not os.path.exists(self.cal_folder):
            os.makedirs(self.cal_folder)
        self.OSLCalFile = {}
        self.OSLCalFile["BIMMS_SERIAL"] = self.ID
        self.OSLCalFile["potentiostat"] = {}
        self.OSLCalFile["potentiostat"]["SE"] = {}
        self.OSLCalFile["potentiostat"]["differential"] = {}
        self.OSLCalFile["potentiostat"]["SE"]["AC"] = {}
        self.OSLCalFile["potentiostat"]["SE"]["DC"] = {}
        self.OSLCalFile["potentiostat"]["differential"]["AC"] = {}
        self.OSLCalFile["potentiostat"]["differential"]["DC"] = {}

        self.OSLCalFile["galvanostat"] = {}
        self.OSLCalFile["galvanostat"]["SE"] = {}
        self.OSLCalFile["galvanostat"]["differential"] = {}
        self.OSLCalFile["galvanostat"]["SE"]["Low_gain"] = {}
        self.OSLCalFile["galvanostat"]["SE"]["High_gain"] = {}

        self.OSLCalFile["galvanostat"]["differential"]["Low_gain"] = {}
        self.OSLCalFile["galvanostat"]["differential"]["High_gain"] = {}

        self.OSLCalFile["galvanostat"]["differential"]["High_gain"]["DC"] = {}
        self.OSLCalFile["galvanostat"]["differential"]["High_gain"]["AC"] = {}
        self.OSLCalFile["galvanostat"]["differential"]["Low_gain"]["DC"] = {}
        self.OSLCalFile["galvanostat"]["differential"]["Low_gain"]["AC"] = {}

        self.OSLCalFile["galvanostat"]["SE"]["High_gain"]["DC"] = {}
        self.OSLCalFile["galvanostat"]["SE"]["High_gain"]["AC"] = {}
        self.OSLCalFile["galvanostat"]["SE"]["Low_gain"]["DC"] = {}
        self.OSLCalFile["galvanostat"]["SE"]["Low_gain"]["AC"] = {}

        outfile_name = (
            "./" + self.cal_folder + "/OSLCal_BIMMS_" + str(self.ID) + ".json"
        )
        outfile = open(outfile_name, "w")
        json.dump(self.OSLCalFile, outfile)
        outfile.close()
        self.OSLCalibration = True
        self.Load_OSLCal()

    def Update_OSLCal(
        self,
        Z_load,
        data_open,
        data_short,
        data_load,
        excitation_mode="potentiostat",
        differential=True,
        high_current_gain=True,
        coupling="DC",
    ):
        if self.OSLCalibration == False:  # Create Cal file if does not exist
            if verbose:
                print(
                    "Creating new OSL Calibration file for BIMMS " + str(self.ID) + "."
                )
            self.Create_OSLCal()

        data = {}
        data["load"] = data_load.toJson()
        data["open"] = data_open.toJson()
        data["short"] = data_short.toJson()
        data["resistor"] = Z_load

        if differential:
            connection_mode = "differential"
        else:
            connection_mode = "SE"
        if high_current_gain:
            current_gain = "High_gain"
        else:
            current_gain = "Low_gain"

        if excitation_mode == "potentiostat":
            self.OSLCalFile[excitation_mode][connection_mode][coupling] = {}
            self.OSLCalFile[excitation_mode][connection_mode][coupling] = data
        else:
            self.OSLCalFile[excitation_mode][connection_mode][current_gain][
                coupling
            ] = {}
            self.OSLCalFile[excitation_mode][connection_mode][current_gain][
                coupling
            ] = data

        outfile_name = (
            "./" + self.cal_folder + "/OSLCal_BIMMS_" + str(self.ID) + ".json"
        )
        outfile = open(outfile_name, "w")
        json.dump(self.OSLCalFile, outfile)
        outfile.close()
        self.OSLCalibration = True
        self.Load_OSLCal()

    #########################
    ## Calibration methods ##
    #########################

    def apply_OSLCal(
        self,
        freq,
        mag,
        phase,
        excitation_mode="potentiostat",
        differential=True,
        high_current_gain=True,
        coupling="DC",
    ):
        if self.OSLCalibration:
            if differential:
                connection_mode = "differential"
            else:
                connection_mode = "SE"
            if high_current_gain:
                current_gain = "High_gain"
            else:
                current_gain = "Low_gain"
            if excitation_mode == "potentiostat":
                cal_data = self.OSLCalFile[excitation_mode][connection_mode][coupling]

            else:
                cal_data = self.OSLCalFile[excitation_mode][connection_mode][
                    current_gain
                ][coupling]

            if cal_data == {}:
                if excitation_mode == "potentiostat":
                    if verbose:
                        print("WARNING: Potentiostat EIS calibration data not found.")
                else:
                    if verbose:
                        print("WARNING: Galvanostat EIS calibration data not found.")
                return (freq, mag, phase)

            cal_load = cal_data["load"]
            cal_open = cal_data["open"]
            cal_short = cal_data["short"]
            Z_load = cal_data["resistor"]
            load_coef_mag = np.array(cal_load["mag_coeff"])
            load_freq_mag = np.array(cal_load["mag_freq_range"])
            load_coef_phase = np.array(cal_load["phase_coeff"])
            load_freq_phase = np.array(cal_load["phase_freq_range"])

            short_coef_mag = np.array(cal_short["mag_coeff"])
            short_freq_mag = np.array(cal_short["mag_freq_range"])

            short_coef_phase = np.array(cal_short["phase_coeff"])
            short_freq_phase = np.array(cal_short["phase_freq_range"])

            open_coef_mag = np.array(cal_open["mag_coeff"])
            open_freq_mag = np.array(cal_open["mag_freq_range"])

            open_coef_phase = np.array(cal_open["phase_coeff"])
            open_freq_phase = np.array(cal_open["phase_freq_range"])

            # Compute Calibration Poly for freq_meas range
            load_mag_data = ComputeSplitFit(load_coef_mag, load_freq_mag, freq)
            load_phase_data = ComputeSplitFit(load_coef_phase, load_freq_phase, freq)
            short_mag_data = ComputeSplitFit(short_coef_mag, short_freq_mag, freq)
            short_phase_data = ComputeSplitFit(short_coef_phase, short_freq_phase, freq)
            open_mag_data = ComputeSplitFit(open_coef_mag, open_freq_mag, freq)
            open_phase_data = ComputeSplitFit(open_coef_phase, open_freq_phase, freq)

            Z_cal_load = load_mag_data * np.exp(1j * load_phase_data * np.pi / 180)
            Z_cal_short = short_mag_data * np.exp(1j * short_phase_data * np.pi / 180)
            Z_cal_open = open_mag_data * np.exp(1j * open_phase_data * np.pi / 180)
            Z_measured = mag * np.exp(1j * phase * np.pi / 180)

            num = Z_load * (Z_measured - Z_cal_short) * (Z_cal_open - Z_cal_load)
            denom = (Z_cal_open - Z_measured) * (Z_cal_load - Z_cal_short)
            Z_cal = num / denom

            mag_calibrated = np.abs(Z_cal)
            phase_calibrated = np.angle(Z_cal) * 180 / np.pi

        else:
            if verbose:
                print(
                    "WARNING: Calibration file not found. Please consider calibrating the board."
                )
            return (freq, mag, phase)

        return (freq, mag_calibrated, phase_calibrated)

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

        freq, gain_mes, phase_mes, gain_ch1 = self.interface.bode_measurement(
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

        self.interface.configure_network_analyser()
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

        self.interface.configure_network_analyser()
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
        self.interface.in_set_channel(channel=0, Vrange=vrange1, Voffset=0.0)
        self.interface.in_set_channel(channel=1, Vrange=vrange2, Voffset=0.0)
        self.interface.set_Chan_trigger(
            0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left"
        )  # Improvement: use internal trigger instead
        self.interface.triangle(channel=0, freq=1 / period, amp=V_awg, offset=0.0)
        if n_delay:
            print("Wait for settling...")
            sleep(n_delay * period)
        print("Measuring...")
        t = self.interface.set_acq(freq=fs, samples=N_pts)
        voltage, current = self.interface.acq()
        if n_avg > 0:
            current_array = []
            voltage_array = []
            for i in range(n_avg):
                print("Average: " + str(i + 1))
                self.interface.set_Chan_trigger(
                    0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left"
                )  # Improvement: use internal trigger instead
                t = self.interface.set_acq(freq=fs, samples=N_pts)
                voltage, current = self.interface.acq()
                voltage_array.append(voltage)
                current_array.append(current)
            voltage_array = np.array(voltage_array)
            current_array = np.array(current_array)
            voltage = np.mean(voltage_array, axis=0)
            current = np.mean(current_array, axis=0)
        else:
            self.interface.set_Chan_trigger(
                0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left"
            )  # Improvement: use internal trigger instead
            t = self.interface.set_acq(freq=fs, samples=N_pts)
            voltage, current = self.interface.acq()
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

        self.interface.in_set_channel(channel=0, Vrange=vrange1, Voffset=0)
        self.interface.in_set_channel(channel=1, Vrange=vrange2, Voffset=0)
        self.interface.triangle(channel=0, freq=1 / period, amp=amp, offset=0)
        if n_delay:
            print("Wait for settling...")
            sleep(n_delay * period)
        print("Measuring...")
        t = self.interface.set_acq(freq=fs, samples=N_pts)
        voltage, current = self.interface.acq()
        if n_avg > 0:
            current_array = []
            voltage_array = []
            for i in range(n_avg):
                print("Average: " + str(i + 1))
                self.interface.set_Chan_trigger(
                    0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left"
                )  # Improvement: use internal trigger instead
                t = self.interface.set_acq(freq=fs, samples=N_pts)
                voltage, current = self.interface.acq()
                voltage_array.append(voltage)
                current_array.append(current)
            voltage_array = np.array(voltage_array)
            current_array = np.array(current_array)
            voltage = np.mean(voltage_array, axis=0)
            current = np.mean(current_array, axis=0)
        else:
            self.interface.set_Chan_trigger(
                0, trig_th, hysteresis=0.01, type="Rising", position=0, ref="left"
            )  # Improvement: use internal trigger instead
            t = self.interface.set_acq(freq=fs, samples=N_pts)
            voltage, current = self.interface.acq()
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
