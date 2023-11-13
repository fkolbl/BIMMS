# BIMMS
*Python librairy for controling [BIMMS](https://www.hardware-x.com/article/S2468-0672(22)00132-8/fulltext)*.


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
    - Add defaults gains (gain_SE, gain_DIFF, etc) in cst files and add use them in examples/tests/selftests
    - Add selftests capabilities
    - Add measurement features 
    - Set G_EIS/P_EIS when voltage/current excitation set
    - Add calibration routines
    - Check "vrange" parameter
    - Double check excitation/readout signaling
    - check "set_recording_voltage" and "set_recording_current" in BIMMSConfig
    - BUG: In 004_test_TIA --> BS.recording_mode is changed between measurements?
