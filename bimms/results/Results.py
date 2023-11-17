
import numpy as np

from ..backend.BIMMS_Class import BIMMS_class, abstractmethod
from ..system.BIMMScalibration import BIMMScalibration
from ..utils import constants as BIMMScst
import matplotlib.pyplot as plt

class Results_class(BIMMS_class):
    """
    Results class for BIMMS
    """
    @abstractmethod
    def __init__(self, ID=0):
        super().__init__()
        self.ID = ID


