
import numpy as np

from ..backend.BIMMS_Class import BIMMS_class, abstractmethod
from ..system.BIMMScalibration import BIMMScalibration
from ..utils import constants as BIMMScst
import matplotlib.pyplot as plt

class Results_class(BIMMS_class, dict):
    """
    Results class for BIMMS
    """
    @abstractmethod
    def __init__(self, ID=0):
        super().__init__(fixed_attr=False)
        # To enable the autocompletion
        self.config = {}
        self.calibration = {}
        self.ID = None
        self.__sync()

    def load(self, data, blacklist=[], **kwargs):
        super().load(data, blacklist, **kwargs)
        self.__sync()


    def __setitem__(self, key, value):
        self.__dict__[key] = value
        super().__setitem__(key, value)

    def __sync(self):
        self.update(self.__dict__)
        bl = ['__BIMMSObject__', 'verbose', 'bimms_type', '_BIMMS_class__fixed_attr']
        for key in bl:
            self.pop(key)

class Results_test(Results_class):
    def __init__(self, ID=0):
        super().__init__(ID)

class bode_results(Results_class):
    """

    """
    def __init__(self, ID=0):
        super().__init__(ID)
    

class temporal_results(Results_class):
    """

    """
    def __init__(self, ID=0):
        super().__init__(ID)
    



