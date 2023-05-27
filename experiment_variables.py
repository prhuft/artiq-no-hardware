from artiq.experiment import *
import numpy as np
from collections import namedtuple
# from exceptions import KeyError


class ExperimentVariables(EnvExperiment):

    def build(self):
        
        Variable = namedtuple("Variable","name value value_type kwargs") 
        # kwargs is a dictionary of keyword arguments for the appropriate ARTIQ value function, e.g. NumberValue.
        # see the examples below.
        
        # list of the global experiment variables. these must be valid python variable names. 
        # the values entered are default values that are only used to initialize the GUI the very 
        # first time that the code is run with the new variable. i.e., after you add a new variable,
        # the next time the code runs it will pull the value from the dataset, not this list.
        self.vars_list = [
            Variable("fMHz_cooling_dds", 111.0*MHz, NumberValue, {'type':'float', 'unit': 'MHz'}),
            Variable("pdB_cooling_dds", -4, NumberValue, {'type': 'float'}),
            Variable("fMHz_FORT_dds", 111.0*MHz, NumberValue, {'type': 'float', 'unit': 'MHz'}),
            Variable("pdB_FORT_dds", -4, NumberValue, {'type': 'float'}),
            Variable("fMHz_OP_dds", 111.0*MHz, NumberValue, {'type': 'float', 'unit': 'MHz'}),
            Variable("pdB_OP_dds", -4, NumberValue, {'type': 'float'}),
            Variable("UV_light_on", False, BooleanValue, {})
        ]
        
        # can only call get_dataset in build, but can only call set_dataset in run. so 
        # we need to see which datasets exist here, create new ones if there are new vars,
        # and then in run we will set all the datasets with the values from the GUI.
        for var in self.vars_list:
            try: # get the value of the variable from the dataset, if it exists
                value = self.get_dataset(var.name)
                self.setattr_argument(var.name, var.value_type(value, **var.kwargs))
            except Exception as e: 
                if type(e) == KeyError: # if the variable does not exist, create the dataset
                    print(f"Found new variable {e}! Adding argument.")
                    self.setattr_argument(var.name, var.value_type(var.value, **var.kwargs))
                else:
                    print(f"Exception {e}")
    
    def run(self):
    
        for var in self.vars_list:
            self.set_dataset(var.name, getattr(self, var.name), broadcast=True, persist=True)