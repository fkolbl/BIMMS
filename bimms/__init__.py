""" Bio Impedance Measurement System, a portable and versatile platform for bio-impedance measurements"""

# Meta information
__title__           = 'BIMMS'
__version__         = '0.0.1'
__date__            = '2021–07–12'
__author__          = 'Louis Regnacq'
__contributors__    = 'Louis Regnacq, Florian Kolbl, Yannick Bornat, Thomas Couppey'
__copyright__       = 'Louis Regnacq'
__license__         = 'CeCILL'

# Public interface
from .system.BIMMS import BIMMS
from .system.BIMMSconfig import BIMMSconfig
#from .utils.PostProcessing import *
from .utils.config_mode import config_mode, config_mode_list, config_range
from .measure.Measure import *
from .results.Results import *
from .utils import constants as cst
from .utils.functions import *

from .backend.BIMMS_Class import BIMMS_class, load_any