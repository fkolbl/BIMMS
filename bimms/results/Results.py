
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
    def __init__(self, config=None, Raw_data=None, ID=0):
        super().__init__()
        self.__set_config(config)
        self.__set_raw_data(Raw_data)
        self.__sync()
        
    def __set_config(self, config):
        if config is None:
            config = {}
        elif is_BIMMS_class(config):
            config.save(save=False)
        if "bimms_type" in config:
            config["result_type"] = config.pop("bimms_type")
        self.update({"config":config})

    def __set_raw_data(self, Raw_data):
        if Raw_data is None:
            Raw_data = {}
        elif is_BIMMS_class(Raw_data):
            Raw_data.save(save=False)
        if "bimms_type" in Raw_data:
            Raw_data["result_type"] = Raw_data.pop("bimms_type")
        self.update({"Raw_data":Raw_data})

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
        super().__init__(ID)

class bode_results(BIMMS_results):
    """

    """
    def __init__(self,BIMMS,data, ID=0):
        super().__init__(ID)
        self.BIMMS = BIMMS
        self.data = data

    def EIS(self):
        print("WARNING: Not fully implemented")

        results['mag'] = data['']

    

    

class temporal_results(BIMMS_results):
    """

    """
    def __init__(self,BIMMS,data, ID=0):
        super().__init__(ID)
        self.BIMMS = BIMMS
        self.data = data
    



