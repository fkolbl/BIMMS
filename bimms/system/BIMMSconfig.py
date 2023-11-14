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
from warnings import warn

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .BIMMSHardware import BIMMShardware
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
            print("Mode: " +str(self.value))
            print("Warning : mode not found, ", self.value, " mode kept")
            print("Possible modes are :", self.modes)

    def __eq__(self, obj):
        try:
            return self.value == str(obj)
        except:
            return False

    def __str__(self):
        return self.value

    def __repr__(self):
        modes_str = "["
        for mod in self.modes:
            modes_str += str(mod)
            modes_str += ", "
        modes_str = modes_str[:-2] + "]"
        return "['config_mode' : "+ self.value + " "+ modes_str + "]"

    def __int__(self):
        try:
            return int(self.value)
        except:
            print("Warning :", self.value, " cannot be converted to int")

    def get_modes(self, verbose=True):
        """
        return possible modes of the config_mode object

        Parameters
        ----------
        verbose : boolexit()
            if true print the modes

        Return
        ------
        modes   : list(str)
            self.mode
        """
        if verbose:
            print(self.modes)

        return self.modes




###################################
## CLASS FOR BIMMS CONFIGURATION ##
###################################
class BIMMSconfig(BIMMShardware):
    def __init__(self, bimms_id=None, serialnumber=None):
        super().__init__(bimms_id=bimms_id, serialnumber=serialnumber)

        ## Measeremenet
        self.excitation_sources = config_mode("EXTERNAL" ,"INTERNAL", default="INTERNAL")
        self.excitation_mode =  config_mode("G_EIS", "P_EIS", default="P_EIS")
        self.wire_mode =  config_mode("2_WIRE", "4_WIRE", "2", "4",default="2_WIRE")
        self.excitation_signaling_mode = config_mode("SE", "DIFF", default="SE")
        self.excitation_coupling = config_mode("AC", "DC", default="DC")
        self.readout_coupling = config_mode("AC", "DC", default="DC")
        self.recording_mode =  config_mode("I", "V", "BOTH",default="BOTH")
        self.recording_signaling_mode = config_mode("SE", "DIFF", "AUTO", default="AUTO")

        # gains
        self.G_EIS_gain = config_mode("LOW", "HIGH", "AUTO", default="AUTO")
        self.IRO_gain = config_mode(*cst.gain_array.tolist(), default=1)
        self.VRO_gain = config_mode(*cst.gain_array.tolist(), default=1)
        self.DC_feedback = config_mode(True, False, default=False)

        # Signals
        #self.I_amplitude = config_mode("", "None", default="None")

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

    ################################
    ## BIMMS measurements methods ##
    ################################
    def set_config(self,send = True):
        """
        
        """
        self.set_STM32_idle()
        if self.wire_mode == "2" or self.wire_mode == "2_WIRE":
            self.set_2_wires_mode()
        else:   # 4
            self.set_4_wires_mode()
        self.set_exitation_config()
        self.set_recording_config()

        # Send the configuration to set the relays
        if (send):
            self.send_config()

    def reset_config():
        print("WARNING: RESET CONFIG NOT IMPLEMENTED")
        pass # TO IMPLEMENT

    def set_exitation_config(self):
        """
        
        """
        if self.excitation_sources == "EXTERNAL":
            self.connect_external_AWG()
        else:
            self.connect_internal_AWG()

        if self.excitation_mode == "G_EIS":
            self.connect_Ipos_to_StimPos()
            self.disable_potentiostat()
            if self.G_EIS_gain == "LOW":
                self.set_low_gain_current_source()
            elif self.G_EIS_gain == "HIGH":
                self.set_high_gain_current_source()
            else:   # AUTO
                self.set_low_gain_current_source()  ### TO IMPLEMENT
                print("WARNING: AUTO CURRENT GAIN NOT IMPLEMENTED")
        else:   # P_EIS
            self.connect_Vpos_to_StimPos()
            # self.disable_current_source()			#need to be tested, bug with AD830?
            self.disable_potentiostat()

        if self.excitation_signaling_mode == "DIFF": 
            if self.excitation_mode == "G_EIS":
                self.connect_Ineg_to_StimNeg()
            else:   # P_EIS
                self.connect_Vneg_to_StimNeg()
        else:   # SE
            self.connect_GND_to_StimNeg()

        if self.excitation_coupling == "AC":
            self.set_Stim_AC_coupling()
        else:   # DC
            self.set_Stim_DC_coupling()

        if self.DC_feedback == True:
            self.enable_DC_feedback()
        else:   # False
            self.disable_DC_feedback()


    def set_recording_config(self):
        """
        
        """

        if self.recording_signaling_mode == "AUTO":
            self.recording_signaling_mode(str(self.excitation_signaling_mode))

        if self.recording_mode == "I":
            self.set_I_recording()

        elif self.recording_mode == "V":
            self.set_V_recording()
        else: # BOTH
            self.set_I_recording()
            self.set_V_recording()

        if self.readout_coupling == "AC":
            self.set_CH1_AC_coupling()
            self.set_CH2_AC_coupling()
        else:   # DC
            self.set_CH1_DC_coupling()
            self.set_CH2_DC_coupling()

        self.set_gain_IA(channel=cst.IRO_channel, gain=int(self.IRO_gain))
        self.set_gain_IA(channel=cst.VRO_channel, gain=int(self.VRO_gain))

    def set_I_recording(self):

        if self.recording_mode == "I":
            self.disconnect_CH1_from_scope_1()
        self.connect_CH2_to_scope_2()
        self.connect_TIA_to_CH2()
        self.connect_TIA_to_StimNeg()
        if self.excitation_mode == "G_EIS":
            print("I_recording signalling configuration forced.")
            if self.excitation_signaling_mode == "DIFF":
                self.connect_TIA_Neg_to_Ineg()
            else:
                self.connect_TIA_Neg_to_ground()
        else:   # P_EIS
            if self.recording_signaling_mode == "DIFF":
                self.connect_TIA_Neg_to_Ineg()
            else:
                self.connect_TIA_Neg_to_ground()

    def set_V_recording(self):
        if self.recording_mode == "V":
            self.disconnect_CH2_from_scope_2()
            ##self.disconnect_TIA_from_CH2() fix BUG
        self.connect_CH1_to_scope_1()
        if self.excitation_mode == "G_EIS":
            if self.recording_signaling_mode == "DIFF":
                print("WARNING: Manual connection between V- and GND required (check CH1 jumper)")

    #######################################
    ##  excitation source config methods ##
    #######################################
    def set_current_excitation(
        self,
        coupling="DC",
        differential_stim=True,
        DC_feedback=False,
        Internal_AWG=True,
        High_gain=False,
    ):
        warn('Deprecated: consider using explicit configuration instead."', DeprecationWarning, stacklevel=2)
        self.excitation_mode("G_EIS")
        self.excitation_coupling(coupling)
        self.DC_feedback(DC_feedback)
        if differential_stim:
            self.excitation_signaling_mode("DIFF")
        else:
            self.excitation_signaling_mode("SE")
        if High_gain:
            self.G_EIS_gain("HIGH")
        else:
            self.G_EIS_gain("LOW")

        if Internal_AWG:
            self.excitation_sources("INTERNAL")
        else:
            self.excitation_sources("EXTERNAL")

    def set_voltage_excitation(
        self, coupling="DC", differential_stim=True, Internal_AWG=True
    ):
        warn('Deprecated: consider using explicit configuration instead."', DeprecationWarning, stacklevel=2)
        self.excitation_mode("P_EIS")
        self.excitation_coupling(coupling)
        if differential_stim:
            self.excitation_signaling_mode("DIFF")
        else:
            self.excitation_signaling_mode("SE")
        if Internal_AWG:
            self.excitation_sources("INTERNAL")
        else:
            self.excitation_sources("EXTERNAL")

    ########################################
    ##  recording channels config methods ##
    ########################################
    def set_recording_voltage(self, coupling="DC", gain=1.0):
        """        if self.recording_mode == 'V':
            self.recording_mode('BOTH')
        else:
            self.recording_mode('I')"""
        self.readout_coupling(coupling)
        self.VRO_gain(gain)

    def set_recording_current(self, differential=True, coupling="DC", gain=1.0):
        """if self.recording_mode == 'I':
            self.recording_mode('BOTH')
        else:
            self.recording_mode('V')
        """
        self.readout_coupling(coupling)
        self.VRO_gain(gain)
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

    ######################################
    ## high-level configuration methods ##
    ######################################
    def set_recording_channel_1(self, coupling="DC", gain=1.0):
        """
                
        """
        self.connect_CH1_to_scope_1()
        if coupling == "DC":
            self.set_CH1_DC_coupling()
        else:
            self.set_CH1_AC_coupling()

        self.set_gain_IA(channel=1, gain=gain)

    def set_recording_channel_2(self, coupling="DC", gain=1.0):
        """
                
        """
        self.connect_CH2_to_scope_2()
        if coupling == "DC":
            self.set_CH2_DC_coupling()
        else:
            self.set_CH2_AC_coupling()

        self.set_gain_IA(channel=2, gain=gain)

    def set_potentiostatic_EIS_config(
        self,
        differential=True,
        two_wires=True,
        coupling="DC",
        voltage_gain=1,
        current_gain=1,
    ):
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
            self.wire_mode(2)
        else:
            self.wire_mode(4)


    def set_galvanostatic_EIS_config(
        self,
        differential=True,
        two_wires=True,
        High_gain=True,
        coupling="DC",
        DC_feedback=False,
        voltage_gain=1,
        current_gain=1,
    ):
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
            self.wire_mode(2)
        else:
            self.wire_mode(4)

    def set_cyclic_voltametry_config(
        self, mode="two_points", coupling="DC", differential=True
    ):
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
            self.wire_mode(2)

    def set_cyclic_amperometry_config(
        self,
        mode="two_points",
        coupling="DC",
        differential=True,
        High_gain=True,
        DC_feedback=False,
    ):
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
            self.wire_mode(2)

