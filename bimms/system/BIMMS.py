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
import json
from scipy.signal import butter, lfilter
from time import sleep

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .BIMMScalibration import BIMMScalibration
from ..measure.Measure import Measure

### for debug
faulthandler.enable()
### verbosity of the verbosity
verbose = True

##############################
## CLASS FOR BIMMS HANDLING ##
##############################
class BIMMS(BIMMScalibration):
    def __init__(self, bimms_id=None, serialnumber=None):
        super().__init__(bimms_id=bimms_id, serialnumber=serialnumber)
        self.measures = []
        self.results = {}

    def attach_calibrator(self, calibrator):
        pass

    def attach_measure(self, m : Measure):
        self.measures += [m]


    def calibrate(self):
        pass

    def check_measures_config():
        pass

    def measure(self,clear_mstack = True):
        self.check_config()
        self.set_config()
        if float(self.config.config_settling):
            sleep(float(self.config.config_settling))
        self.get_awg_parameters()
        self.get_recording_gains()
        if len(self.measures) == 1:
            m = self.measures[0]
            self.results = {
                "config": self.config.save(),
                "measure": m.save()
            }
            self.results.update(m.measure(self))
            
        else:
            for m in self.measures:
                self.results[m.ID] = {
                    "config": self.config.save(),
                    "measure": m.save()
                }
                self.results[m.ID].update(m.measure(self))
        if (clear_mstack):
            self.measures = []
        return self.results

    def check_config(self):
        pass