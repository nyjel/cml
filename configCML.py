__author__ = 'nigel'

from pyqtgraph.graphicsItems.GradientEditorItem import GradientEditorItem
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.widgets import RawImageWidget

from numpy import *
from numpy.random import rand
from scipy.signal import convolve2d
from scipy.ndimage import zoom
from diffusiveCML import DiffusiveCML

from initCML import *
from analysisCML import *

class ConfigCML:

    def __init__(self):
        self.sideLen = 80
        self.colorMap = 'thermal'
        self.colorsNum = 256
        #initLattice=imageCML('./sri_mandala.jpg');
        #self.initLattice=randomPing(self.sideLen,self.sideLen,scaleFactor=0.0)
        self.initLattice=magicSquare(self.sideLen)
        #initLattice=primesSquare(sidelen)
        #initLattice=randbin(sidelen,sidelen)
        #print initLattice
        # wait variable can slow things down by running a counter inside
        #why do we have a, gl, and gg in here as well as initCML?
        #cml = DiffusiveCML(initLattice,kern='asymm',a=1.5,gl=0.4,gg=0.2,wait=10000)
        self.cml = DiffusiveCML(self.initLattice,kern='symm4');
        self.stats = AnalysisCML(self.initLattice)
        #cml = DiffusiveCML(initLattice,kern='magic11')
        #cml = CompetitiveCML(initLattice)
        # drawmod is useful to limit framerate or find a cycle avoiding flicker
        self.drawmod=7
        self.kernType='asymm'

