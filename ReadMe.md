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
    - Add defaults gains (gain_SE, gain_DIFF, etc) in cst files and add use them in examples/tests/selftests --> en cours
    - Add selftests capabilities 
    - Add measurement methods/class --> skeleton OK 
    - Add calibration routines --> skeleton OK 
    - Comments
    - add verbosity mode
    - do "standard configuration" 
    - add check_saturation 
    - change HIGH/LOW GAIN 
    - Test multiple measurements in a row
    - results class
    - offset compensation in scope input

# HARDWARE TEST TODO:
    - Double check excitation/readout signaling 
    - test connect_TIA_to_CH2, disconnect_TIA_from_CH2, disable_current_source, enable_potentiostat
    - test dc feedback
    - Offset values are odds (measure seems ok tho)