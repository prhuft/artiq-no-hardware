from artiq.experiment import *
import numpy as np
import time

# a no-hardware simulation that we can use to test plotting

class SingleAtomLoading(EnvExperiment):

    def build(self):
        self.setattr_argument("measurements", NumberValue(100, ndecimals=0, step=1))
        self.setattr_argument("bins", NumberValue(50, ndecimals=0, step=1))
        self.setattr_argument("counts_per_bin", NumberValue(10, ndecimals=0, step=1))
        
    def sample_photocounts(self):
        """generator function to sample counts from background + single atom distribution"""
    
        n = self.measurements
    
        mu_bg = 100 # the mean background
        mu_sig = 100 # the signal mean 
        poisson = lambda x, m: (m**x/np.math.factorial(x))*np.exp(-m)
        count_dist = lambda counts: poisson(counts, mu_bg) + poisson(counts, mu_sig+mu_bg)
        
        domain = [0,500] # assume we don't measure fewer than 0 or more than 500 counts
        x1,x2 = domain

        fmax = poisson(mu_bg, mu_bg) # the maximum
        y_dist = np.empty(n) 
        f_dist = np.empty(n)
        x_dist = np.empty(n) # this is the distribution we want
        j = 0 # dist index
        
        while j < n:
        
            x = int((x2-x1)*np.random.rand()+0.5) # rand val on domain of f(x)
            f = count_dist(x)
            y = np.random.rand()*fmax # rand val on range of f(x)
            if y <= f:
                y_dist[j]=y
                f_dist[j]=f
                x_dist[j]=x # x vals with approximate gaussian pdf
                j+=1
                yield x # the number of counts

        
    def run(self):
        
        hist_bins = np.zeros(self.bins,dtype=int)
        self.set_dataset("photocounts", hist_bins, broadcast=True)
        
        print("starting")
        for counts in self.sample_photocounts():
        
            bin = int(counts/self.counts_per_bin)
            if bin < self.bins:
                hist_bins[bin] += 1
                self.mutate_dataset("photocounts", bin, hist_bins[bin])
            # print("counts=",counts,"bin=",bin)
            time.sleep(0.5)
                
        print("finished")
