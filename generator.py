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
        matrix = rand(xsize, ysize)
        numCells = xsize * ysize

    def iterate(self):
        """
        Iterate / convole the matrix
        """

        global matrix
        # diffusion
        # save last for spin calc
        #last=ll
        diff=convolve2d(matrix, dkern, mode='same', boundary='wrap')
        # scale before adding to keep value in <-1,+1> bounds
        diffScaled=((1-gl) * matrix + diff)
        # scale before adding to keep value in <-1,+1> bounds
        #ll = 1-(a*(diffScaled**2))
        matrix = (1-gg) * (1- (a* (diffScaled**2))) + (gg/numCells) * sum(matrix)
