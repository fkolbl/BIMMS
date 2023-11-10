"""
	Python library to use BIMMS measurement setup - STM32 constants
	Authors: Florian Kolbl / Louis Regnacq / Thomas Couppey
	(c) ETIS - University Cergy-Pontoise
		IMS - University of Bordeaux
		CNRS

	Requires:
		Python 3.6 or higher
"""
import numpy as np

cmd_shift = 2**29
## Comannd values
nothing = 0x00
set_STM32_state = 0x01
set_relay = 0x02
read_register = 0x03

## STM32 STATE
STM32_stopped = 0x00
STM32_idle = 0x01
STM32_locked = 0x02
STM32_error = 0x03

## STM32 to AD2 SPI
STM32_CLK = 1e6
STM32_CLK_p = 1
STM32_MOSI_p = 2
STM32_MISO_p = 3
STM32_CS_p = 0


## IA Gain IOs
CH1_A0_0 = 2**8
CH1_A1_0 = 2**9
CH1_A0_1 = 2**10
CH1_A1_1 = 2**11

CH2_A0_0 = 2**12
CH2_A1_0 = 2**13
CH2_A0_1 = 2**14
CH2_A1_1 = 2**15

## LEDs IO
LED_err = 2**5
LED_status = 2**4

## Free IOs
IO6 = 2**6
IO7 = 2**7

## Relay mapping
Ch1Coupling_rly = 2**0
Chan1Scope1_rly = 2**1
Ch2Coupling_rly = 2**2
Chan2Scope2_rly = 2**3
DCFeedback_rly = 2**4
InternalAWG_rly = 2**5
TIANegIn1_rly = 2**6
TIANegIn2_rly = 2**7
TIA2Chan2_rly = 2**8
TIACoupling_rly = 2**9
EnPotentiostat_rly = 2**10
EnCurrentSource_rly = 2**11
GainCurrentSource_rly = 2**12
Potentiostat2StimPos_rly = 2**13
Ipos2StimPos_rly = 2**14
VoutPos2StimPos_rly = 2**15
Ineg2StimNeg_rly = 2**16
VoutNeg2StimNeg_rly = 2**17
TIA2StimNeg_rly = 2**18
GND2StimNeg_rly = 2**19
StimCoupling_rly = 2**20
StimNeg2VNeg_ryl = 2**21
StimPos2VPos_rly = 2**22

## Memory registers
ID_add = 0
state_add = 1
error_add = 2
relays_map_add = 3

## Gains
gain_array = np.array([1, 2, 4, 5, 10, 20, 25, 50, 100])
gain_IA1 = np.array([1, 2, 2, 5, 5, 10, 5, 10, 10])
gain_IA2 = np.array([1, 1, 2, 1, 2, 2, 5, 5, 10])

## Channels
VRO_channel = 1
IRO_channel = 2

## BIMMS Board/serial-numbers dictionary

BimmsSerialNumbers = {1: '',\
                    2: '',\
                    3: 'SN:210321B2825B',\
                    4: 'SN:210321B28C03',\
                    5: 'SN:210321B281BF',\
                    6: 'SN:210321B28CCD',\
                    7: '',\
                    8: 'SN:210321B2825D',\
                    9: 'SN:210321B28CEB'}
