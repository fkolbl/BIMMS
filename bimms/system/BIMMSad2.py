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
from abc import abstractmethod
import sys
import os
import andi as ai
import os
from warnings import warn

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from ..backend.BIMMS_Class import BIMMS_class
from ..utils.functions import convert
from ..utils import constants as cst


### verbosity of the verbosity
verbose = True


##############################
## CLASS FOR BIMMS HANDLING ##
##############################
class BIMMSad2(BIMMS_class):
    @abstractmethod
    def __init__(self, bimms_id=None, serialnumber=None):
        super().__init__()
        # To maintain connection use keep_on
        self.switch_off = True
        self.ad2_on = False

        self.__start_ad2(bimms_id=bimms_id, serialnumber=serialnumber)
        self.__DIO_init()


    def __start_ad2(self, bimms_id, serialnumber):
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
            self.ad2 = ai.Andi(self.serialnumber)
        else:
            self.ad2 = ai.Andi()
            self.serialnumber = self.ad2.serialnumber
        self.ad2_on = True
        if verbose:
            print("ad2 device opened")
        self.ID = 0


    def __del__(self):
        if self.switch_off and self.ad2_on:
            self.close()


    def close(self):
        self.ad2.close()
        self.ad2_on = False
        if verbose:
            print("ad2 device closed")

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
        self.ad2.SPI_reset()
        self.ad2.set_SPI_frequency(clk)
        self.ad2.set_SPI_Clock_channel(clk_p)
        self.ad2.set_SPI_Data_channel(ai.SPIDataIdx["DQ0_MOSI_SISO"], mosi_p)
        self.ad2.set_SPI_Data_channel(ai.SPIDataIdx["DQ1_MISO"], miso_p)
        self.ad2.set_SPI_mode(ai.SPIMode["CPOL_1_CPA_1"])
        self.ad2.set_SPI_MSB_first()
        self.ad2.set_SPI_CS(cs_p, ai.LogicLevel["H"])

    def SPI_write_32(self, cs_p, value):
        """ """
        tx_8bvalues = convert(value)
        self.ad2.SPI_select(cs_p, ai.LogicLevel["L"])
        for k in tx_8bvalues:
            self.ad2.SPI_write_one(ai.SPI_cDQ["MOSI/MISO"], 8, k)
        self.ad2.SPI_select(cs_p, ai.LogicLevel["H"])

    def SPI_read_32(self, cs_p):
        """ """
        offsets = [2**24, 2**16, 2**8, 2**0]
        value = 0
        self.ad2.SPI_select(cs_p, ai.LogicLevel["L"])
        for k in offsets:
            rx = self.ad2.SPI_read_one(ai.SPI_cDQ["MOSI/MISO"], 8)
            value += rx * k
        self.ad2.SPI_select(cs_p, ai.LogicLevel["H"])
        return value

    ############################
    ## AD2 Digital IO methods ##
    ############################
    def __DIO_init(self):
        self.ad2.configure_digitalIO()
