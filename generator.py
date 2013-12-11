__author__ = 'nigel'

"""
The generator of the CML matrix:  responsible for generating, iterating and managing the matrix
"""


from numpy import *
from numpy.random import rand
from scipy.signal import convolve2d

a=1.7
# good parms gg=.1,gl=.4,a=1.7
# gg.05, same
# gg 0.05, gl 0.5
drawmod=20
gg=0.1
gl=0.5
cc=gl/5
dkern=array([(0,cc,0.1),(cc,0,cc),(0,cc,cc)])
i=0

class Generator:

    def __init__(self, xsize, ysize):
        """
        Create a new matrix, and populate it with a default random population
        """
        global matrix, numCells
        self.matrix = rand(xsize, ysize)
        numCells = xsize * ysize

    def iterate(self):
        """
        Iterate / convolve the matrix
        """

        global gg, i, drawmod

        i = i+1
        # diffusion
        # save last for spin calc
        #last=ll
        diff=convolve2d(self.matrix, dkern, mode='same', boundary='wrap')
        # scale before adding to keep value in <-1,+1> bounds
        diffScaled=((1-gl) * self.matrix + diff)
        # scale before adding to keep value in <-1,+1> bounds
        #ll = 1-(a*(diffScaled**2))
        self.matrix = (1-gg) * (1- (a* (diffScaled**2))) + (gg/numCells) * sum(self.matrix)

        if (i>1 and i % drawmod==0):
            if (i % 80 == 0):
                gg=gg+.001
                #a=a-.001
                if gg<.04 : gg=gg+.02