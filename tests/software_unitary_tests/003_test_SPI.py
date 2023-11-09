import andi as ai
import bimms as bm
import time
from bimms import cst

interface = ai.Andi()
## STM32 to AD2 SPI
STM32_CLK = 1e6
STM32_CLK_p = 1
STM32_MOSI_p = 2
STM32_MISO_p = 3
STM32_CS_p = 0


## init SPI
interface.SPI_reset()
interface.set_SPI_frequency(STM32_CLK)
interface.set_SPI_Clock_channel(STM32_CLK_p)
interface.set_SPI_Data_channel(ai.SPIDataIdx['DQ0_MOSI_SISO'],STM32_MOSI_p)
interface.set_SPI_Data_channel(ai.SPIDataIdx['DQ1_MISO'],STM32_MISO_p)
interface.set_SPI_mode(ai.SPIMode['CPOL_1_CPA_1'])

interface.set_SPI_MSB_first()
interface.set_SPI_CS(STM32_CS_p,ai.LogicLevel['H'])



value = 128
#TX a value
tx_8bvalues = bm.convert(value)

offsets = [2**24, 2**16, 2**8, 2**0]
value = 0
interface.SPI_select(cst.STM32_CS_p,ai.LogicLevel['L'])
for k in offsets:
	rx = interface.SPI_read_one(ai.SPI_cDQ['MOSI/MISO'],8)
	value += rx*k
interface.SPI_select(cst.STM32_CS_p,ai.LogicLevel['H'])


