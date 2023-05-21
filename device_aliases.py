"""
Map devices defined in a parent experiment to aliases
"""

from artiq.experiment import *


class DeviceAliases:

    alias_map = {
        "urukul0_ch0": "dds_FORT",
        "urukul0_ch1": "dds_cooling_SP"
    }

    def __init__(self, experiment):
        for key,val in self.alias_map.items():
            if hasattr(experiment, key):
                print(f"setting attr {key} to {val}")
                setattr(experiment, val, getattr(experiment,key))
                
class FakeSwitch:

    def on(self):
        print("on")
        
    def off(self):
        print("off")
            
class FakeUrukul:

    def __init__(self):
        self.sw = FakeSwitch()
              
# test class              
class FakeExperiment(EnvExperiment):

    # todo: this approach is not too bad, but can we define hardware aliases elsewhere and make them global
    # so we don't still have to declare the hardware channels explicitly in every experiment?
    # probably we can do this in a base experiment, and then our experiments will inherit from the base exp.
    def build(self):
        # with actual hardware we would use self.setattr_device("device")
        self.urukul0_ch0 = FakeUrukul()
        
        # map the hardware channels
        DeviceAliases(experiment=self)
        assert hasattr(self, DeviceAliases.alias_map['urukul0_ch0']), f"whoops, still missing attr {DeviceAliases.alias_map['urukul0_ch0']}"
    
    def run(self):
        self.dds_FORT.sw.on()
        print("FORT dds on")

    
    
    