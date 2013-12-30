__author__ = 'david'

"""
The diffusive CML class:  responsible for initializing defaults, iterating and managing the matrix
"""


from numpy import *
from numpy.random import rand
from scipy.signal import convolve2d




class CompetitiveCML:

    def __init__(self, lattice):
        """
        take initial state as parameter
        """
        #global matrix, numCells
        self.matrix=lattice
        self.computeMod=1
        self.matrix = lattice
        self.numCells = size(lattice,0) * size(lattice,1)
        self.l=2.0
        self.a=0.22
        self.ckern=array([(0,self.a,0,),(self.a,0,0),(0,self.a,0)])
        self.iter=0
        self.localIter=1

    def iterate(self):
        """
        Iterate / convolve the matrix
        """

        self.iter += self.iter
        # diffusion
        # save last for spin calc
        #last=ll
        #for i in range(self.localIter):
        diff=convolve2d(self.matrix, self.ckern, mode='same', boundary='wrap')
        self.matrix = self.l*self.matrix*exp(-(self.matrix+diff))
        print "min ",self.matrix.min().min()