import andi as ai
import bimms as bm
import time
from bimms import cst

ad2 = ai.Andi()
## STM32 to AD2 SPI
STM32_CLK = 1e6
STM32_CLK_p = 1
STM32_MOSI_p = 2
STM32_MISO_p = 3
STM32_CS_p = 0


## init SPI
ad2.SPI_reset()
ad2.set_SPI_frequency(STM32_CLK)
ad2.set_SPI_Clock_channel(STM32_CLK_p)
ad2.set_SPI_Data_channel(ai.SPIDataIdx["DQ0_MOSI_SISO"], STM32_MOSI_p)
ad2.set_SPI_Data_channel(ai.SPIDataIdx["DQ1_MISO"], STM32_MISO_p)
ad2.set_SPI_mode(ai.SPIMode["CPOL_1_CPA_1"])
ad2.set_SPI_MSB_first()
ad2.set_SPI_CS(STM32_CS_p, ai.LogicLevel["H"])





value = 128
#TX a value
tx_8bvalues = bm.convert(value)

for k in range (5):
	ad2.SPI_select(STM32_CS_p, ai.LogicLevel["L"])
	for k in tx_8bvalues:
		ad2.SPI_write_one(ai.SPI_cDQ["MOSI/MISO"], 8, k)
	ad2.SPI_select(STM32_CS_p, ai.LogicLevel["H"])
	time.sleep(1)

ad2.close()