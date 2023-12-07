
#import numpy as np

from ..backend.BIMMS_Class import BIMMS_class, abstractmethod,is_BIMMS_class
'''from ..system.BIMMScalibration import BIMMScalibration
from ..utils import constants as BIMMScst
import matplotlib.pyplot as plt'''

class BIMMS_results(BIMMS_class, dict):
    """
    Results class for BIMMS
    """
    @abstractmethod
    def __init__(self, config=None, raw_data=None, ID=0):
        super().__init__()
        self.config = {}
        self.raw_data = {}

        self.__set_config(config)
        self.__set_raw_data(raw_data)
        self.__sync()
        
    def __set_config(self, config):
        if config is None:
            config = {}
        elif is_BIMMS_class(config):
            config = config.save(save=False)
        if "bimms_type" in config:
            config["result_type"] = config.pop("bimms_type")
        self.update({"config":config})

    def __set_raw_data(self, raw_data):
        if raw_data is None:
            raw_data = {}
        self.update({"raw_data":raw_data})

    def save(self, save=False, fname="bimms_save.json", blacklist=[], **kwargs):
        self.__sync()
        return super().save(save, fname, blacklist, **kwargs)

    def load(self, data, blacklist=[], **kwargs):
        super().load(data, blacklist, **kwargs)
        self.__sync()

    def __setitem__(self, key, value):
        if not key == "bimms_type":
            self.__dict__[key] = value
        super().__setitem__(key, value)

    def __delitem__(self, key):
        if not key == "bimms_type":
            del self.__dict__[key]
        super().__delitem__(key)

    def update(self, __m, **kwargs) -> None:
        """
        overload of dict update method to update both attibute and items
        """
        self.__dict__.update(__m, **kwargs)
        super().update(__m, **kwargs)
    
    def __sync(self):
        self.update(self.__dict__)
        self.pop('__BIMMSObject__')

class Results_test(BIMMS_results):
    def __init__(self, ID=0):
        super().__init__(ID=ID)

class bode_results(BIMMS_results):
    """

    """
    def __init__(self,BIMMS,data, ID=0):
        super().__init__(config = BIMMS.config,raw_data=data,ID=ID)
        self.BIMMS = BIMMS
        self['freq'] = self.raw_data['freq']
        self['mag_ch1_raw'] = self.raw_data['mag_ch1_raw']
        self['mag_ch2_raw'] = self.raw_data['mag_ch1_raw']/self.raw_data['mag_raw']
        self['phase_raw'] = self.raw_data['phase_raw']
        if (self.BIMMS.calibrated):
            pass
        else:
            self['V_readout'] =  self['mag_ch1_raw']/self.BIMMS.cal_ch1_gain
            self['I_readout'] = self['mag_ch2_raw']/(self.BIMMS.cal_ch2_gain*self.BIMMS.cal_TIA_gain)

    def EIS(self):
        print("WARNING: EIS measure not fully implemented")
        self['mag_Z'] = self['V_readout']/self['I_readout']
        self['phase_Z'] = self.raw_data['phase_raw']

        




        #results['mag'] = data['']

    

    

class temporal_results(BIMMS_results):
    """

    """
    def __init__(self,BIMMS,data, ID=0):
        super().__init__(config = BIMMS.config,raw_data=data,ID=ID)
        self.BIMMS = BIMMS

        print("WARNING: temporal post-processing measure not fully implemented")
        self['t'] = self.raw_data['t']
        self['chan2_raw'] = self.raw_data['chan2']
        self['chan1_raw'] = self.raw_data['chan1']
