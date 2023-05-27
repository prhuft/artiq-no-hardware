"""
Map devices defined in a parent experiment to aliases
"""

from artiq.experiment import *

NO_HARDWARE = True

class DeviceAliases:

    alias_map = {
        "dds_FORT": "urukul0_ch0",
        "dds_cooling_SP": "urukul0_ch1"
    }

    def __init__(self, experiment, device_aliases):
        
        for alias in device_aliases:
            if alias in self.alias_map.keys():
                try:
                    
                    dev_name = self.alias_map[alias]
                    
                    if NO_HARDWARE:
                        setattr(experiment, dev_name, FakeUrukul())
                    else:
                        # setattr for the device, using the device name from device_db.py
                        experiment.setattr_device(dev_name)
                    
                    # make an attribute named alias which points to the device object
                    print(f"setattr self.{alias} = self.{dev_name}")
                    setattr(experiment, alias, getattr(experiment,dev_name))

                except KeyError:
                    print(f"KeyError: {alias} not defined in alias map. Please define it.")

                
class FakeSwitch:

    def on(self):
        print("on")
        
    def off(self):
        print("off")
            
class FakeUrukul:

    def __init__(self):
        self.sw = FakeSwitch()
              
# test class              
class DeviceAliasTest(EnvExperiment):

    def build(self):
        
        # this will do setattr_device using the device names from device_db, 
        # and then define attributes which point to the device objects, using these aliases
        DeviceAliases(
            experiment=self, 
            device_aliases=[
                'dds_FORT',
                'dds_cooling_SP'
            ])
    
    def run(self):
        self.dds_FORT.sw.on()
        print("FORT dds on")

    
    
    