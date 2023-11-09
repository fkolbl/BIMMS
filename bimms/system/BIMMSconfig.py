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
from warnings import warn

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


from .BIMMShadware import BIMMShardware
from ..utils import constants as cst

### for debug
faulthandler.enable()
### verbosity of the verbosity
verbose = True


class config_mode():
    def __init__(self, *args, **kwargs):
        self.modes = []
        self.value = None
        for a in args:
            self.modes += [str(a).upper()]

        if "default" in kwargs:
            self(kwargs["default"])

    def __call__(self, mode):
        if str(mode).upper() in self.modes:
            self.value = str(mode).upper()
        else:
            print("Warning : mode not found, ", self.value, " mode kept")
            print("Possible modes are :", self.modes)

    def __eq__(self, obj):
        try:
            return self.value == str(obj)
        except:
            return False

    def __str__(self):
        return self.value
    
    def __int__(self):
        try:
            return int(self.value)
        except:
            print("Warning :", self.value, " cannot be converted to int")



###################################
## CLASS FOR BIMMS CONFIGURATION ##
###################################
class BIMMSconfig(BIMMShardware):
    def __init__(self, bimms_id=None, serialnumber=None):
        super().__init__(bimms_id=bimms_id, serialnumber=serialnumber)

        ## Measeremenet
        self.excitation_sources = config_mode("EXTERNAL" ,"INTERNAL", default="INTERNAL")
        self.excitation_mode =  config_mode("G_EIS", "P_EIS", default="P_EIS")
        self.wire_mode =  config_mode("2", "4", 2, 4,default="2_WIRE")
        self.signaling_mode = config_mode("S_E", "DIFF", default="S_E")
        self.excitation_coupling = config_mode("AC", "DC", default="DC")
        self.readout_coupling = config_mode("AC", "DC", default="DC")

        # gains
        self.G_EIS_gain = config_mode("LOW", "HIGH", "AUTO", default="AUTO")
        self.IRO_gain = config_mode(*cst.gain_array.tolist(), default=1)
        self.VRO_gain = config_mode(*cst.gain_array.tolist(), default=1)
        self.DC_feedback = config_mode(True, False, default=False)
    ##############################################
    ## AD2 Digital IO methods for gains control ##
    ##############################################

    def set_gain_IA(self, channel=1, gain=1):
        gain_array = cst.gain_array
        gain_IA1 = cst.gain_IA1
        gain_IA2 = cst.gain_IA2
        idx_gain = np.where(gain_array == gain)
        idx_gain = idx_gain[0]
        if idx_gain != None:
            if channel == 1:
                self.set_gain_ch1_1(gain_IA1[idx_gain])
                self.set_gain_ch1_2(gain_IA2[idx_gain])
            if channel == 2:
                self.set_gain_ch2_1(gain_IA1[idx_gain])
                self.set_gain_ch2_2(gain_IA2[idx_gain])
        else:
            if verbose:
                print("WARNING: Wrong IA gain value. IA gain set to 1.")
            if channel == 1:
                self.set_gain_ch1_1(gain_IA1[0])
                self.set_gain_ch1_2(gain_IA2[0])
            if channel == 2:
                self.set_gain_ch2_1(gain_IA1[0])
                self.set_gain_ch2_2(gain_IA2[0])


    def set_VRO_gain(self):
        pass

    def set_IRO_gain(self):
        pass



    ################################
    ## BIMMS measurements methods ##
    ################################
    def set_config(self):
        """
        
        """
        if self.excitation_sources == "external":
            self.connect_external_AWG()
        else:
            self.connect_external_AWG()

        if self.excitation_mode == "G_EIS":
            pass
        else:   # P_EIS
            pass

        if self.wire_mode == "2":
            self.set_2_wires_mode()
        else:   # 4
            self.set_4_wires_mode()

        if self.signaling_mode == "S_E":
            pass
        else:   # DIFF
            pass

        if self.excitation_coupling == "AC":
            pass
        else:   # DC
            pass
        if self.readout_coupling == "AC":
            pass
        else:   # DC
            pass
        if self.G_EIS_gain == "LOW":
            pass
        elif self.G_EIS_gain == "HIGH":
            pass
        else:   # AUTO
            pass

        self.set_gain_IA(channel=2, gain=int(self.IRO_gain))
        self.set_gain_IA(channel=1, gain=int(self.VRO_gain))

        if self.DC_feedback == "True":
            pass
        else:   # False
            pass

    def set_2_points_config(self):
        warn('This method is deprecated.', DeprecationWarning, stacklevel=2)
        self.set_2_wires_mode()

    def set_3_points_config(self):
        warn('This method is deprecated.', DeprecationWarning, stacklevel=2)
        self.set_3_wires_mode()

    def set_4_points_config(self):
        warn('This method is deprecated.', DeprecationWarning, stacklevel=2)
        self.set_4_wires_mode()

    def set_2_wires_mode(self):
        self.StimNeg2VNeg = 1
        self.StimPos2VPos = 1

    def set_3_wires_mode(self):
        pass

    def set_4_wires_mode(self):
        self.StimNeg2VNeg = 0
        self.StimPos2VPos = 0

    def set_current_excitation(
        self,
        coupling="DC",
        differential_stim=True,
        DC_feedback=False,
        Internal_AWG=True,
        High_gain=False,
    ):
        if coupling == "DC":
            self.set_Stim_DC_coupling()
            self.disable_DC_feedback()
        else:
            self.set_Stim_AC_coupling()
        if DC_feedback:
            self.enable_DC_feedback()
        else:
            self.disable_DC_feedback()
        self.connect_Ipos_to_StimPos()
        if differential_stim:
            self.connect_Ineg_to_StimNeg()
        else:
            self.connect_GND_to_StimNeg()

        if High_gain:
            self.set_high_gain_current_source()
        else:
            self.set_low_gain_current_source()

        if Internal_AWG:
            self.connect_internal_AWG()
        else:
            self.connect_external_AWG()
        self.disable_potentiostat()

    def set_voltage_excitation(
        self, coupling="DC", differential_stim=True, Internal_AWG=True
    ):
        self.disable_DC_feedback()
        if coupling == "DC":
            self.set_Stim_DC_coupling()
        else:
            self.set_Stim_AC_coupling()
        self.connect_Vpos_to_StimPos()

        if differential_stim:
            self.connect_Vneg_to_StimNeg()
        else:
            self.connect_GND_to_StimNeg()

        if Internal_AWG:
            self.connect_internal_AWG()
        else:
            self.connect_external_AWG()
        # self.disable_current_source()			#need to be tested, bug with AD830?
        self.disable_potentiostat()

    def set_recording_channel_1(self, coupling="DC", gain=1.0):
        self.connect_CH1_to_scope_1()
        if coupling == "DC":
            self.set_CH1_DC_coupling()
        else:
            self.set_CH1_AC_coupling()

        self.set_gain_IA(channel=1, gain=gain)


    def set_recording_channel_2(self, coupling="DC", gain=1.0):
        self.connect_CH2_to_scope_2()
        if coupling == "DC":
            self.set_CH2_DC_coupling()
        else:
            self.set_CH2_AC_coupling()

        self.set_gain_IA(channel=2, gain=gain)

    def set_recording_voltage(self, coupling="DC", gain=1.0):
        self.set_recording_channel_1(coupling=coupling, gain=gain)

    def set_recording_current(self, differential=True, coupling="DC", gain=1.0):
        self.set_recording_channel_2(coupling=coupling, gain=gain)
        self.connect_TIA_to_CH2()
        self.connect_TIA_to_StimNeg()
        # self.connect_TIA_Neg_to_ground()

        if differential:
            if self.VoutPos2StimPos:  # Voltage excitation
                self.connect_TIA_Neg_to_Vneg()
            else:
                if self.connect_Ipos_to_StimPos():  # Current excitation
                    self.connect_TIA_Neg_to_Ineg()
                else:
                    self.connect_TIA_Neg_to_ground()
        else:
            self.connect_TIA_Neg_to_ground()
        if coupling == "DC":
            self.set_TIA_DC_coupling()
        else:
            self.set_TIA_DC_coupling()
    
    def set_potentiostat_EIS_config(
        self,
        differential=True,
        two_wires=True,
        coupling="DC",
        voltage_gain=1,
        current_gain=1,
    ):
        self.set_STM32_idle()
        if differential:
            if coupling == "DC":
                self.set_voltage_excitation(coupling="DC", differential_stim=True)
                self.set_recording_current(
                    differential=True, coupling="DC", gain=current_gain
                )
                self.set_recording_voltage(coupling="DC", gain=voltage_gain)
            else:
                self.set_voltage_excitation(coupling="AC", differential_stim=True)
                self.set_recording_current(
                    differential=True, coupling="DC", gain=current_gain
                )
                self.set_recording_voltage(coupling="AC", gain=voltage_gain)
        else:
            if coupling == "DC":
                self.set_voltage_excitation(coupling="DC", differential_stim=False)
                self.set_recording_current(
                    differential=False, coupling="DC", gain=current_gain
                )
                self.set_recording_voltage(coupling="DC", gain=voltage_gain)
            else:
                self.set_voltage_excitation(coupling="AC", differential_stim=False)
                self.set_recording_current(
                    differential=False, coupling="DC", gain=current_gain
                )
                self.set_recording_voltage(coupling="AC", gain=voltage_gain)
        if two_wires:
            self.set_2_points_config()
        else:
            self.set_4_points_config()
        self.set_config()

    def set_galvanostat_EIS_config(
        self,
        differential=True,
        two_wires=True,
        High_gain=True,
        coupling="DC",
        DC_feedback=False,
        voltage_gain=1,
        current_gain=1,
    ):
        self.set_STM32_idle()
        if differential:
            if coupling == "DC":
                self.set_current_excitation(
                    coupling="DC",
                    differential_stim=True,
                    DC_feedback=DC_feedback,
                    Internal_AWG=True,
                    High_gain=High_gain,
                )
                self.set_recording_current(
                    differential=True, coupling="DC", gain=current_gain
                )
                self.set_recording_voltage(coupling="DC", gain=voltage_gain)
            else:
                self.set_current_excitation(
                    coupling="AC",
                    differential_stim=True,
                    DC_feedback=DC_feedback,
                    Internal_AWG=True,
                    High_gain=High_gain,
                )
                self.set_recording_current(
                    differential=True, coupling="DC", gain=current_gain
                )
                self.set_recording_voltage(coupling="DC", gain=voltage_gain)
        else:
            if coupling == "DC":
                self.set_current_excitation(
                    coupling="DC",
                    differential_stim=False,
                    DC_feedback=DC_feedback,
                    Internal_AWG=True,
                    High_gain=High_gain,
                )
                self.set_recording_current(
                    differential=False, coupling="DC", gain=current_gain
                )
                self.set_recording_voltage(coupling="DC", gain=voltage_gain)
            else:
                self.set_current_excitation(
                    coupling="AC",
                    differential_stim=False,
                    DC_feedback=DC_feedback,
                    Internal_AWG=True,
                    High_gain=High_gain,
                )
                self.set_recording_current(
                    differential=False, coupling="DC", gain=current_gain
                )
                self.set_recording_voltage(coupling="DC", gain=voltage_gain)
        if two_wires:
            self.set_2_points_config()
        else:
            self.set_4_points_config()

        self.set_config()

    def set_cyclic_voltametry_config(
        self, mode="two_points", coupling="DC", differential=True
    ):
        self.set_STM32_idle()
        if mode == "two_points":
            if coupling == "DC":
                self.set_voltage_excitation(
                    coupling="DC", differential_stim=differential
                )
                self.set_recording_current(
                    differential=differential, coupling="DC", gain=1
                )
                self.set_recording_voltage(coupling="DC", gain=1)
            else:
                self.set_voltage_excitation(
                    coupling="AC", differential_stim=differential
                )
                self.set_recording_current(
                    differential=differential, coupling="DC", gain=1
                )
                self.set_recording_voltage(coupling="AC", gain=1)
            self.set_2_points_config()

        self.set_config()

    def set_cyclic_amperometry_config(
        self,
        mode="two_points",
        coupling="DC",
        differential=True,
        High_gain=True,
        DC_feedback=False,
    ):
        self.set_STM32_idle()
        if mode == "two_points":
            if coupling == "DC":
                self.set_current_excitation(
                    coupling="DC",
                    differential_stim=True,
                    DC_feedback=DC_feedback,
                    Internal_AWG=True,
                    High_gain=High_gain,
                )
                self.set_recording_current(
                    differential=differential, coupling="DC", gain=1
                )
                self.set_recording_voltage(coupling="DC", gain=1)
            else:
                self.set_current_excitation(
                    coupling="DC",
                    differential_stim=True,
                    DC_feedback=DC_feedback,
                    Internal_AWG=True,
                    High_gain=High_gain,
                )
                self.set_recording_current(
                    differential=differential, coupling="DC", gain=1
                )
                self.set_recording_voltage(coupling="AC", gain=1)
            self.set_2_points_config()
        self.set_config()
