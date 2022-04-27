import numpy as np
import scipy.stats as st
from Extension.record import Record

class Newrecord(Record):
    def __init__(self, n, delta, phi):
        Record.__init__(self, n)
        self.delta = delta
        self.phi = phi

    def get_interval(self):
        difference = self.get_difference()

        if len(difference) == 0:
            interval = self.delta
        elif len(difference) == 1:
            interval = difference[0]
        else:
            mean = np.mean(difference)
            scale = np.std(difference)
            interval = st.norm.ppf(1 - np.power(0.1, self.phi), loc=mean, scale=scale)

        return interval
