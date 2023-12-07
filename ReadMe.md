# BIMMS
*Python library for controling [BIMMS](https://www.hardware-x.com/article/S2468-0672(22)00132-8/fulltext)*.


# Installation

use pip for installation : 
```
pip install bimms
```

# Requirements

Third party software (Waveform) has to be installed before BIMMS python API. 
BIMMS has been developped for python 3.
Required packages:
- numpy
- scipy
- matplotlib
- andi-py


for the third party softwares, please visit:
[Waveform](https://digilent.com/shop/software/digilent-waveforms/)

# TODO
    - Add selftests capabilities 
    - Add calibration routines --> skeleton OK 
    - Comments
    - add verbosity mode
    - do "standard configuration" 
    - add check_saturation 
    - add auto HIGH/LOW GAIN 
    - offset compensation in scope input

# HARDWARE TEST TODO:
    - Double check excitation/readout signaling 
    - test connect_TIA_to_CH2, disconnect_TIA_from_CH2, disable_current_source, enable_potentiostat
    - test dc feedback
    - Offset values are odds (measure seems ok tho)
    - Test Readout AC coupling (IA, TIA, etc) --> TIA AC COupling???

# Calibration todo
    - Offset calibration
    - DC calibration
    - OSL calibration


#TODO CONF AD2:
#SET in_channel_range_set --> 2.0,5.0 or 5.0 --> 2.0 by default; check if saturation?
#BS.ad2.in_average_filter_mode(-1)
#AD2 attenation = 1.0
#AD2 offsets = 0.0 
#Triggers --> AWG by default --> external TODO
#Conf modes (bode,)