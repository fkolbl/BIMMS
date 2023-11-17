
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
        super().__init__()
        # To enable the autocompletion
        self.config = {}
        self.calibration = {}
        self.ID = None

        #
        self['ID'] = ID


    def __setitem__(self, key, value):
        self.__dict__[key] = value
        print(key, value)
        super().__setitem__(key, value)

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
    



