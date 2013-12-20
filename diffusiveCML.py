__author__ = 'nigel'

"""
The diffusive CML class:  responsible for initializing defaults, iterating and managing the matrix
"""


from numpy import *
from numpy.random import rand
from scipy.signal import convolve2d




class DiffusiveCML:

    def __init__(self, lattice,kern='symm4'):
        """
        take initial state as parameter
        """
        #global matrix, numCells
        self.computeMod=20
        self.matrix = lattice
        self.numCells = size(lattice,0) * size(lattice,1)
        self.kernType=kern
        self.localIter=1
        # good parms gg=.1,gl=.4,a=1.7
        # gg.05, same
        # gg 0.05, gl 0.5
        self.a=1.55
        self.gg=0.044
        #self.gl=0.454545
        self.gl=0.1

        # center was .05050505
        # experimental scaled magic square kernel
        #self.dkern=[[ 0.06837607,  0.00854701,  0.05128205],
        #             [ 0.02564103,  0.0,  0.05982906],
        #              [ 0.03418803,  0.07692308,  0.01709402]]
        #self.dkern=[[ 0.08080808,  0.01010101,  0.06060606],
         #           [ 0.03030303,  0.0,  0.07070707],
          #          [ 0.04040404,  0.09090909,  0.02020202]]
        if self.kernType == 'symm4':
            self.cc=self.gl/4
            self.dkern=array([(0,self.cc,0.0),(self.cc,0,self.cc),(0,self.cc,0)])
        if self.kernType == 'symm8':
            self.cc=self.gl/8
            self.dkern=array([(self.cc,self.cc,self.cc),(self.cc,0,self.cc),(self.cc,self.cc,self.cc)])
        elif self.kernType =='asymm':
            self.cc=self.gl/5
            self.dkern=array([(0,self.cc,0.0),(self.cc,0,0),(0,self.cc,0)])
        elif self.kernType == 'magic11':
            self.gl=0.404040
            self.dkern=[[ 0.08080808,  0.01010101,  0.06060606],
                         [ 0.03030303,  0.0,  0.07070707],
                         [ 0.04040404,  0.09090909,  0.02020202]]
        self.iter=0

    def iterate(self):
        """
        Iterate / convolve the matrix
        """

        self.iter += self.iter
        # diffusion
        # save last for spin calc
        #last=ll
        for i in range(self.localIter):
            diff=convolve2d(self.matrix, self.dkern, mode='same', boundary='wrap')
            # scale before adding to keep value in <-1,+1> bounds
            diffScaled=((1-self.gl) * self.matrix + diff)
            # scale before adding to keep value in <-1,+1> bounds

        self.matrix = (1-self.gg) * (1- (self.a * (diffScaled**2))) + (self.gg/self.numCells) * sum(self.matrix)
