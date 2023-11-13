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
from abc import ABC, abstractmethod
import sys
import os
import andi as ai
import os
from warnings import warn

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from ..utils.functions import convert
from ..utils import constants as cst


### verbosity of the verbosity
verbose = True


##############################
## CLASS FOR BIMMS HANDLING ##
##############################
class BIMMShardware(object):
    @abstractmethod
    def __init__(self, bimms_id=None, serialnumber=None):
        # default values for gains of all channels
        self.CalFile = ""
        self.Gain_TIA = 100
        self.Gain_Voltage_SE = 1.1
        self.Gain_Voltage_DIFF = 2.2
        self.Gain_High_current = 1 / 5000
        self.Gain_Low_current = 1 / 50000

        # Relay states
        self.Ch1Coupling = 0
        self.Chan1Scope1 = 0
        self.Ch2Coupling = 0
        self.Chan2Scope2 = 0
        self.DCFeedback = 0
        self.InternalAWG = 0
        self.TIANegIn1 = 0
        self.TIANegIn2 = 0
        self.TIA2Chan2 = 0
        self.TIACoupling = 0
        self.EnPotentiostat = 0
        self.EnCurrentSource = 0
        self.GainCurrentSource = 0
        self.Potentiostat2StimPos = 0
        self.Ipos2StimPos = 0
        self.VoutPos2StimPos = 0
        self.Ineg2StimNeg = 0
        self.VoutNeg2StimNeg = 0
        self.TIA2StimNeg = 0
        self.GND2StimNeg = 0
        self.StimCoupling = 0
        self.StimNeg2VNeg = 0
        self.StimPos2VPos = 0

        # IA gain IO
        self.CH1_A0_0 = 0
        self.CH1_A1_0 = 0
        self.CH1_A0_1 = 0
        self.CH1_A1_1 = 0
        self.CH2_A0_0 = 0
        self.CH2_A1_0 = 0
        self.CH2_A0_1 = 0
        self.CH2_A1_1 = 0

        # LEDs
        self.LED_status = 0
        self.LED_err = 0

        # Free AD2 DIO (O is input, 1 is ouput)
        self.IO6_IO = 0
        self.IO7_IO = 0
        self.IO6_value = 0
        self.IO7_value = 0

        self.OSLCalibration = False
        self.cal_folder = "./CalibrationData/"
        self.OSL_cal_data = 0

        # To maintain connection use keep_on
        self.switch_off = True
        self.interface_on = False

        self.__start_interface(bimms_id=bimms_id, serialnumber=serialnumber)
        self.__DIO_init()


    def __del__(self):
        if self.switch_off and self.interface_on:
            self.close()

    def close(self):
        self.set_state(cst.STM32_stopped)
        self.interface.close()
        self.interface_on = False
        if verbose:
            print("device closed")

    def keep_on(self):
        self.switch_off = False

    def keep_off(self):
        self.switch_off = True

    def __start_interface(self, bimms_id, serialnumber):
        selected = False
        if isinstance(bimms_id, int):
            if bimms_id in cst.BimmsSerialNumbers:
                self.serialnumber = cst.BimmsSerialNumbers[bimms_id]
                selected = True
            else:
                print(
                    "warning 'bimms_id' not referentced: first device will be selected"
                )
                exit()
        elif isinstance(serialnumber, str):
            if serialnumber in cst.BimmsSerialNumbers.values():
                self.serialnumber
                selected = True
            else:
                print(
                    "warning 'serialnumber' not referentced: first device will be selected"
                )
                exit()

        if selected:
            self.interface = ai.Andi(self.serialnumber)
        else:
            self.interface = ai.Andi()
            self.serialnumber = self.interface.serialnumber
        self.interface_on = True
        if verbose:
            print("device opened")
        self.ID = 0

        self.SPI_init_STM32()

        self.ID = self.get_board_ID()

        if self.ID == 0 or self.ID > 16:  # only 8 bimms for now
            self.close()
            if verbose:
                raise ValueError(
                    "Failed to communicate with STM32 MCU. Make sure that BIMMS is powered (try to reconnect Power Jack)."
                )
            quit()

        if verbose:
            print("You are connected to BIMMS " + str(self.ID))


    def __del__(self):
        if self.switch_off and self.interface_on:
            self.close()


    def keep_on(self):
        self.switch_off = False

    def keep_off(self):
        self.switch_off = True


    #################################
    ## SPI communitation methods ##
    #################################
    def SPI_init(self, clk, clk_p, mosi_p, miso_p, cs_p):
        """
        init an spi communication
        """
        self.interface.SPI_reset()
        self.interface.set_SPI_frequency(clk)
        self.interface.set_SPI_Clock_channel(clk_p)
        self.interface.set_SPI_Data_channel(ai.SPIDataIdx["DQ0_MOSI_SISO"], mosi_p)
        self.interface.set_SPI_Data_channel(ai.SPIDataIdx["DQ1_MISO"], miso_p)
        self.interface.set_SPI_mode(ai.SPIMode["CPOL_1_CPA_1"])
        self.interface.set_SPI_MSB_first()
        self.interface.set_SPI_CS(cs_p, ai.LogicLevel["H"])

    def SPI_write_32(self, cs_p, value):
        """ """
        tx_8bvalues = convert(value)
        self.interface.SPI_select(cs_p, ai.LogicLevel["L"])
        for k in tx_8bvalues:
            self.interface.SPI_write_one(ai.SPI_cDQ["MOSI/MISO"], 8, k)
        self.interface.SPI_select(cs_p, ai.LogicLevel["H"])

    def SPI_read_32(self, cs_p):
        """ """
        offsets = [2**24, 2**16, 2**8, 2**0]
        value = 0
        self.interface.SPI_select(cs_p, ai.LogicLevel["L"])
        for k in offsets:
            rx = self.interface.SPI_read_one(ai.SPI_cDQ["MOSI/MISO"], 8)
            value += rx * k
        self.interface.SPI_select(cs_p, ai.LogicLevel["H"])
        return value

    def SPI_init_STM32(self):
        self.SPI_init(
            cst.STM32_CLK,
            cst.STM32_CLK_p,
            cst.STM32_MOSI_p,
            cst.STM32_MISO_p,
            cst.STM32_CS_p,
        )

    def tx_2_STM32(self, value):
        self.SPI_write_32(cst.STM32_CS_p, value)

    def rx_from_STM32(self):
        return self.SPI_read_32(cst.STM32_CS_p)

    def read_STM32_register(self, address):
        value = cst.cmd_shift * cst.read_register + address
        # print(bin(2**32))
        # print(bin(value))
        self.tx_2_STM32(value)
        register_value = self.rx_from_STM32()
        return register_value

    #######################
    ## low level methods ##
    #######################
    def get_board_ID(self):
        ID = self.read_STM32_register(cst.ID_add)
        return ID

    def get_config_vector(self):
        vector = 0
        vector += self.Ch1Coupling * cst.Ch1Coupling_rly
        vector += self.Chan1Scope1 * cst.Chan1Scope1_rly
        vector += self.Ch2Coupling * cst.Ch2Coupling_rly
        vector += self.Chan2Scope2 * cst.Chan2Scope2_rly
        vector += self.DCFeedback * cst.DCFeedback_rly
        vector += self.InternalAWG * cst.InternalAWG_rly
        vector += self.TIANegIn1 * cst.TIANegIn1_rly
        vector += self.TIANegIn2 * cst.TIANegIn2_rly
        vector += self.TIA2Chan2 * cst.TIA2Chan2_rly
        vector += self.TIACoupling * cst.TIACoupling_rly
        vector += self.EnPotentiostat * cst.EnPotentiostat_rly
        vector += self.EnCurrentSource * cst.EnCurrentSource_rly
        vector += self.GainCurrentSource * cst.GainCurrentSource_rly
        vector += self.Potentiostat2StimPos * cst.Potentiostat2StimPos_rly
        vector += self.Ipos2StimPos * cst.Ipos2StimPos_rly
        vector += self.VoutPos2StimPos * cst.VoutPos2StimPos_rly
        vector += self.Ineg2StimNeg * cst.Ineg2StimNeg_rly
        vector += self.VoutNeg2StimNeg * cst.VoutNeg2StimNeg_rly
        vector += self.TIA2StimNeg * cst.TIA2StimNeg_rly
        vector += self.GND2StimNeg * cst.GND2StimNeg_rly
        vector += self.StimCoupling * cst.StimCoupling_rly
        vector += self.StimNeg2VNeg * cst.StimNeg2VNeg_ryl
        vector += self.StimPos2VPos * cst.StimPos2VPos_rly
        return vector

    def set_relays(self, rvector):
        """
        Set all the relays values at once

        Parameters
        ----------
        rvector : int
            see BIMMS_constant for relays mapping
        """
        value = cst.cmd_shift * cst.set_relay + rvector
        self.tx_2_STM32(value)

    def get_relays(self):
        """
        Get the values of all relays

        Returns
        -------
        values : int
            see BIMMS_constant for relays mapping
        """
        relays_map = self.read_STM32_register(cst.relays_map_add)
        return relays_map

    def send_config(self):
        """
        Send the one stored in the current object to the stm32 to set relay config
        """
        rvector = self.get_config_vector()
        self.set_relays(rvector)
        # error handling to be written here

    ###########################################
    ## BIMMS low-level configuration methods ##
    ###########################################

    def connect_CH1_to_scope_1(self):
        self.Chan1Scope1 = 1

    def disconnect_CH1_from_scope_1(self):
        self.Chan1Scope1 = 0

    def connect_CH2_to_scope_2(self):
        self.Chan2Scope2 = 1

    def disconnect_CH2_from_scope_2(self):
        self.Chan2Scope2 = 0

    def set_CH1_AC_coupling(self):
        self.Ch1Coupling = 1

    def set_CH1_DC_coupling(self):
        self.Ch1Coupling = 0

    def set_CH2_AC_coupling(self):
        self.Ch2Coupling = 1

    def set_CH2_DC_coupling(self):
        self.Ch2Coupling = 0

    def connect_Vpos_to_StimPos(self):
        self.VoutPos2StimPos = 1
        self.Ipos2StimPos = 0
        self.Potentiostat2StimPos = 0

    def connect_Ipos_to_StimPos(self):
        self.VoutPos2StimPos = 0
        self.Ipos2StimPos = 1
        self.Potentiostat2StimPos = 0

    def connect_Potentiostat_to_StimPos(self):
        self.VoutPos2StimPos = 0
        self.Ipos2StimPos = 0
        self.Potentiostat2StimPos = 1

    def disconnect_StimPos(self):
        self.VoutPos2StimPos = 0
        self.Ipos2StimPos = 0
        self.Potentiostat2StimPos = 0

    def connect_Ineg_to_StimNeg(self):
        self.Ineg2StimNeg = 1
        self.VoutNeg2StimNeg = 0
        self.TIA2StimNeg = 0
        self.GND2StimNeg = 0

    def connect_Vneg_to_StimNeg(self):
        self.Ineg2StimNeg = 0
        self.VoutNeg2StimNeg = 1
        self.TIA2StimNeg = 0
        self.GND2StimNeg = 0

    def connect_TIA_to_StimNeg(self):
        self.Ineg2StimNeg = 0
        self.VoutNeg2StimNeg = 0
        self.TIA2StimNeg = 1
        self.GND2StimNeg = 0

    def connect_GND_to_StimNeg(self):
        self.Ineg2StimNeg = 0
        self.VoutNeg2StimNeg = 0
        self.TIA2StimNeg = 0
        self.GND2StimNeg = 1

    def disconnect_StimNeg(self):
        self.Ineg2StimNeg = 0
        self.VoutNeg2StimNeg = 0
        self.TIA2StimNeg = 0
        self.GND2StimNeg = 0

    def enable_DC_feedback(self):
        self.DCFeedback = 1

    def disable_DC_feedback(self):
        self.DCFeedback = 0

    def connect_external_AWG(self):
        self.InternalAWG = 1

    def connect_internal_AWG(self):
        self.InternalAWG = 0

    def connect_TIA_to_CH2(
        self,
    ):  # BUG !! Normalement = 0 pour disconnect mais 1 ici pour réparer bug Hardware
        self.TIA2Chan2 = 0

    def disconnect_TIA_from_CH2(self):  # Ne marche pas car BUG Hardware
        self.TIA2Chan2 = 1

    def connect_TIA_Neg_to_ground(self):
        self.TIANegIn1 = 0
        self.TIANegIn2 = 0

    def connect_TIA_Neg_to_Vneg(self):
        self.TIANegIn1 = 1
        self.TIANegIn2 = 0

    def connect_TIA_Neg_to_Ineg(self):
        self.TIANegIn1 = 1
        self.TIANegIn2 = 1

    def set_TIA_AC_coupling(self):
        self.TIACoupling = 1

    def set_TIA_DC_coupling(self):
        self.TIACoupling = 0

    def enable_potentiostat(self):
        self.EnPotentiostat = 1

    def disable_potentiostat(self):
        self.EnPotentiostat = 0

    def enable_current_source(self):
        self.EnCurrentSource = 0

    def disable_current_source(self):  # Might not be usefull / bad for AD830
        self.EnCurrentSource = 1

    def set_high_gain_current_source(self):
        self.GainCurrentSource = 0

    def set_low_gain_current_source(self):
        self.GainCurrentSource = 1

    def set_Stim_DC_coupling(self):
        self.StimCoupling = 1

    def set_Stim_AC_coupling(self):
        self.StimCoupling = 0

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

    ##############################################
    ## AD2 Digital IO methods for gains control ##
    ##############################################
    def __DIO_init(self):
        self.interface.configure_digitalIO()
        self.set_DIO_mode()

    def set_DIO_mode(self):
        IO_vector = 0
        IO_vector += self.IO6_IO * cst.IO6

        # IO_vector += self.IO7_IO * cst.IO7
        # LEDs and IA gain IOs are always set as outputs
        IO_vector += cst.LED_status
        IO_vector += cst.LED_err
        IO_vector += cst.CH1_A0_0
        IO_vector += cst.CH1_A1_0
        IO_vector += cst.CH1_A0_1
        IO_vector += cst.CH1_A1_1
        IO_vector += cst.CH2_A0_0
        IO_vector += cst.CH2_A1_0
        IO_vector += cst.CH2_A0_1
        IO_vector += cst.CH2_A1_1
        self.interface.digitalIO_set_as_output(IO_vector)

    def set_DIO_output(self):
        OUTPUT_vector = 0
        OUTPUT_vector += self.IO6_value * cst.IO6
        OUTPUT_vector += self.IO7_value * cst.IO7
        # LEDs and IA gain IOs are always set as outputs
        OUTPUT_vector += self.LED_status * cst.LED_status
        OUTPUT_vector += self.LED_err * cst.LED_err
        OUTPUT_vector += self.CH1_A0_0 * cst.CH1_A0_0
        OUTPUT_vector += self.CH1_A1_0 * cst.CH1_A1_0
        OUTPUT_vector += self.CH1_A0_1 * cst.CH1_A0_1
        OUTPUT_vector += self.CH1_A1_1 * cst.CH1_A1_1
        OUTPUT_vector += self.CH2_A0_0 * cst.CH2_A0_0
        OUTPUT_vector += self.CH2_A1_0 * cst.CH2_A1_0
        OUTPUT_vector += self.CH2_A0_1 * cst.CH2_A0_1
        OUTPUT_vector += self.CH2_A1_1 * cst.CH2_A1_1

        self.interface.digitalIO_output(OUTPUT_vector)

    def set_gain_ch1_1(self, value):
        if (
            (value != 1) and (value != 2) and (value != 5) and (value != 10)
        ):  # Invalid gain value
            self.CH1_A0_0 = 0  # Gain is one
            self.CH1_A1_0 = 0
        if value == 1:
            self.CH1_A0_0 = 0
            self.CH1_A1_0 = 0
        if value == 2:
            self.CH1_A0_0 = 1
            self.CH1_A1_0 = 0
        if value == 5:
            self.CH1_A0_0 = 0
            self.CH1_A1_0 = 1
        if value == 10:
            self.CH1_A0_0 = 1
            self.CH1_A1_0 = 1
        self.set_DIO_output()

    def set_gain_ch1_2(self, value):
        if (
            (value != 1) and (value != 2) and (value != 5) and (value != 10)
        ):  # Invalid gain value
            self.CH1_A0_1 = 0
            self.CH1_A1_1 = 0  # Gain is one
        if value == 1:
            self.CH1_A0_1 = 0
            self.CH1_A1_1 = 0
        if value == 2:
            self.CH1_A0_1 = 1
            self.CH1_A1_1 = 0
        if value == 5:
            self.CH1_A0_1 = 0
            self.CH1_A1_1 = 1
        if value == 10:
            self.CH1_A0_1 = 1
            self.CH1_A1_1 = 1
        self.set_DIO_output()

    def set_gain_ch2_1(self, value):
        if (
            (value != 1) and (value != 2) and (value != 5) and (value != 10)
        ):  # Invalid gain value
            self.CH2_A0_0 = 0
            self.CH2_A1_0 = 0  # Gain is one
        if value == 1:
            self.CH2_A0_0 = 0
            self.CH2_A1_0 = 0
        if value == 2:
            self.CH2_A0_0 = 1
            self.CH2_A1_0 = 0
        if value == 5:
            self.CH2_A0_0 = 0
            self.CH2_A1_0 = 1
        if value == 10:
            self.CH2_A0_0 = 1
            self.CH2_A1_0 = 1
        self.set_DIO_output()

    def set_gain_ch2_2(self, value):
        if (
            (value != 1) and (value != 2) and (value != 5) and (value != 10)
        ):  # Invalid gain value
            self.CH2_A0_1 = 0
            self.CH2_A1_1 = 0  # Gain is one
        if value == 1:
            self.CH2_A0_1 = 0
            self.CH2_A1_1 = 0
        if value == 2:
            self.CH2_A0_1 = 1
            self.CH2_A1_1 = 0
        if value == 5:
            self.CH2_A0_1 = 0
            self.CH2_A1_1 = 1
        if value == 10:
            self.CH2_A0_1 = 1
            self.CH2_A1_1 = 1
        self.set_DIO_output()

    #################################
    ## STM32 communitation methods ##
    #################################
    def set_state(self, state):
        """
        Set the state of STM32

        Parameters
        ----------
        state : int
            either STM32_stopped, STM32_idle, STM32_locked, STM32_error = 0x03
            defined in BIMMS_constants
        """
        value = cst.cmd_shift * cst.set_STM32_state + state
        self.tx_2_STM32(value)

    def set_STM32_stopped(self):
        self.set_state(cst.STM32_stopped)

    def set_STM32_idle(self):
        self.set_state(cst.STM32_idle)

    def set_STM32_locked(self):
        self.set_state(cst.STM32_locked)

    def set_STM32_error(self):
        self.set_state(cst.STM32_error)

    def get_state(self):
        """
        Get the state of the STM32

        Returns
        -------
        state	: int
            0: STM32_stopped
            1: STM32_idle
            2: STM32_locked
            3: STM32_error
        """
        state = self.read_STM32_register(cst.state_add)
        return state

    def get_STM32_error(self):
        error = self.read_STM32_register(cst.error_add)
        return error