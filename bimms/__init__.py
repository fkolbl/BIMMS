""" Bio Impedance Measurement System, a portable and versatile platform for bio-impedance measurements"""

# Meta information
__title__           = 'BIMMS'
__version__         = '1.0.1'
__date__            = '2021–07–12'
__author__          = 'Louis Regnacq'
__contributors__    = 'Louis Regnacq, Florian Kolbl, Yannick Bornat, Thomas Couppey'
__copyright__       = 'Louis Regnacq'
__license__         = 'CeCILL'

# Public interface
from .system.BIMMS import *
from .utils.PostProcessing import *
from .measure.Measures import *
from .utils import constants as cst
from .utils.functions import *
