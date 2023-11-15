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
from ..backend.file_handler import json_load


def is_config_mode(obj):
    return isinstance(obj, config_mode)

def is_config_mode_list(obj):
    return isinstance(obj, config_mode_list)

def is_float_str(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_int_str(string):
    try:
        return int(string) != float(string)
    except ValueError:
        return False

class config_mode(BIMMS_class):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.modes = []
        self.value = None
        for a in args:
            self.modes += [str(a).upper()]
        
        if self.modes == []:
            self.value = None
        elif "default" in kwargs:
            self(kwargs["default"])
        else:
            self(self.modes[0])
        self.default = self.value
    
    def reset(self):
        self.value = self.default

    def __call__(self, mode):
        if self.is_mode(mode):
            self.value = str(mode).upper()
        else:
            print("Mode: " +str(self.value))
            print("Warning : mode not found, ", self.value, " mode kept")
            print("Possible modes are :", self.modes)

    def __eq__(self, obj):
        try:
            return self.value == str(obj).upper()
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

    def is_mode(self, obj):
        return str(obj).upper() in self.modes



class config_range(config_mode):
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            args = [0, 1]
        else:
            assert(len(args)==2)
        if is_int_str(args[0]) and is_int_str(args[1]):
            self.valuetype = int
        elif is_float_str(args[0]) and is_float_str(args[1]):
            self.valuetype = float
        else:
            print("ERROR: config_range argument should be cinvertible in float or int")
            exit()
        self.min = min(self.valuetype(args[0]), self.valuetype(args[1]))
        self.max = max(self.valuetype(args[0]), self.valuetype(args[1]))

        super().__init__(*args, **kwargs)

    def is_mode(self, obj):
        obj_str = str(obj).upper()
        try:
            val = self.valuetype(obj_str)
            return val > self.min and val < self.max
        except:
            return False


class config_mode_list(BIMMS_class):
    def __init__(self, data=None):
        super().__init__()
        self.list = []
        self.N_list = 0

    def load(self, data, blacklist={}, **kwargs):
        """
        Loading method for config_mode_list

        Parameters
        ----------
        data : dict
            Dictionary containing the BIMMS object
        blacklist : dict, optional
            Dictionary containing the keys to be excluded from the load
        **kwargs : dict, optional
            Additional arguments to be passed to the load method of the BIMMS object
        """
        if isinstance(data, str):
            key_dic = json_load(data)
        else:
            key_dic = data
        for c in key_dic['list']:
            self.__dict__[c] = None
        super().load(key_dic, blacklist, **kwargs)


    def add_mode(self, name, mode):
        name = str(name)
        if name in self.__dict__:
            self.N_list -= 1
            print("WARNING: config mode already in list")
        self.list += [name]
        self.__dict__[name] = mode
        self.N_list += 1

    def reset(self):
        for c in self.list:
            self.__dict__[c].reset()

    def __str__(self) -> str:
        string = ""
        for c in self.list:
            string += c + ": " + str(self.__dict__[c]) + "\n"
        return string

    def __eq__(self, __value: object) -> bool:
        if not is_config_mode_list(__value):
            return False
        if not self.list == __value.list:
            return False
        for c in self.__dict__:
            if not self.__dict__[c] == __value.__dict__[c]:
                return False
        return True
