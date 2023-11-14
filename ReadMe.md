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
    - Add measurement methods/class --> en cours
    - Add AD2config class --> en cours  
    - Set G_EIS/P_EIS when voltage/current excitation magnitude 
    - Add calibration routines 
    - Check "vrange" parameter --> probably useless, to be defined in AD2config()
    - Double check excitation/readout signaling
    - Comments
    - add verbosity mode
    - do "standard configuration" 
    - add check_saturation
