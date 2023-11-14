"""
	Python library to use BIMMS measurement setup - STM32 constants
	Authors: Florian Kolbl / Louis Regnacq / Thomas Couppey
	(c) ETIS - University Cergy-Pontoise
		IMS - University of Bordeaux
		CNRS

	Requires:
		Python 3.6 or higher
"""

from ..backend.BIMMS_Class import BIMMS_class


def is_config_mode(obj):
    return isinstance(obj, config_mode)

def is_config_mode_list(obj):
    return isinstance(obj, config_mode_list)

class config_mode(BIMMS_class):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.modes = []
        self.value = None
        for a in args:
            self.modes += [str(a).upper()]

        if "default" in kwargs:
            self(kwargs["default"])

    def __call__(self, mode):
        if str(mode).upper() in self.modes:
            self.value = str(mode).upper()
        else:
            print("Mode: " +str(self.value))
            print("Warning : mode not found, ", self.value, " mode kept")
            print("Possible modes are :", self.modes)

    def __eq__(self, obj):
        try:
            return self.value == str(obj)
        except:
            return False

    def __str__(self):
        return self.value

    def __repr__(self):
        modes_str = "["
        for mod in self.modes:
            modes_str += str(mod)
            modes_str += ", "
        modes_str = modes_str[:-2] + "]"
        return "['config_mode' : "+ self.value + " "+ modes_str + "]"

    def __int__(self):
        try:
            return int(self.value)
        except:
            print("Warning :", self.value, " cannot be converted to int")

    def get_modes(self, verbose=True):
        """
        return possible modes of the config_mode object

        Parameters
        ----------
        verbose : boolexit()
            if true print the modes

        Return
        ------
        modes   : list(str)
            self.mode
        """
        if verbose:
            print(self.modes)

        return self.modes

class config_mode_list(BIMMS_class):
    def __init__(self, data=None):
        super().__init__()
        self.list = []
        self.N_list = 0


    def add_mode(self, name, mode):
        name = str(name)
        if name in self.__dict__:
            self.N_list -= 1
            print("WARNING: config mode already in list")
        self.list += [name]
        self.__dict__[name] = mode
        self.N_list += 1
