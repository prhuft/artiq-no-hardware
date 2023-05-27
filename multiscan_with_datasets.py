from artiq.experiment import *
from numpy import e



class MultiScanDatasets(EnvExperiment):
    def build(self):
    
        self.vars = ["x", "y"]
        for var in self.vars:
            self.setattr_argument(var, Scannable(default=RangeScan(-2, 2, 11)))

    def measure(self, x, y):
        """spoof a count signal that varies as a Gaussian in x and y"""
        return e**(-x**2-y**2)

    def run(self):
    
        msm = MultiScanManager(
            ("x", self.x),
            ("y", self.y)
        )
                  
        steps = len(list(msm))
        
        max_counts = 0.0
        counts = 0.0
        best_x = best_y = -2
        self.set_dataset("counts", [counts]*steps)
        for var in self.vars:
            self.set_dataset(var, best_x)

        step = 0
        
        # loop over the points and update x and y to the values which give the best counts. 
        # if we get to what we know if the theoretical maximum, break.
        for point in msm:
            counts = self.measure(point.x,point.y)
            self.mutate_dataset("counts", step, counts)
            if counts > max_counts:
                max_counts = counts
                best_x = point.x
                best_y = point.y
                self.set_dataset("x", point.x)
                self.set_dataset("y", point.y)
                print("updated x,y")
        step += 1

        print("best values: (x,y)=",best_x,best_y)