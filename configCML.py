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

    def __init__(self, lastConfig):
        self.name = "CML"
        self.sideLen = 80
        self.colorMap = 'thermal'
        self.colorsNum = 256

        self.initLattice=randomPing(self.sideLen,self.sideLen,scaleFactor=0.0)

        #self.initLattice=imageCML('./sri_mandala.jpg');
        #self.initLattice=magicSquare(self.sideLen)

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

        gei = GradientEditorItem()
        gei.loadPreset(self.colorMap)
        self.lut = gei.getLookupTable(self.colorsNum, alpha=False)

class ConfigCML2:

    def __init__(self, lastConfig):
        self.name = "CML2"
        self.sideLen = 80
        self.colorMap = 'flame'
        self.colorsNum = 256
        #initLattice=imageCML('./sri_mandala.jpg');
        #self.initLattice=randomPing(self.sideLen,self.sideLen,scaleFactor=0.0)
        #self.initLattice=magicSquare(self.sideLen)
        #self.initLattice=primesSquare(self.sideLen)
        self.initLattice=randbin(self.sideLen,self.sideLen)
        #self.initLattice = lastConfig.initLattice
        #print initLattice
        # wait variable can slow things down by running a counter inside
        #why do we have a, gl, and gg in here as well as initCML?
        self.cml = DiffusiveCML(self.initLattice,kern='asymm',a=1.5,gl=0.4,gg=0.2,wait=10000)
        #self.cml = DiffusiveCML(self.initLattice,kern='symm4');
        self.stats = AnalysisCML(self.initLattice)
        #cml = DiffusiveCML(initLattice,kern='magic11')
        #cml = CompetitiveCML(initLattice)
        # drawmod is useful to limit framerate or find a cycle avoiding flicker
        self.drawmod=20
        self.kernType='asymm'

        gei = GradientEditorItem()
        gei.loadPreset(self.colorMap)
        self.lut = gei.getLookupTable(self.colorsNum, alpha=False)


class ConfigCML3:

    def __init__(self, lastConfig):
        self.name = "CML3"
        self.sideLen = 80
        self.colorMap = 'blugr3'
        self.colorsNum = 256
        #initLattice=imageCML('./sri_mandala.jpg');
        self.initLattice=randomPing(self.sideLen,self.sideLen,scaleFactor=0.001)
        #self.initLattice=magicSquare(self.sideLen)
        #self.initLattice=primesSquare(self.sideLen)
        #self.initLattice=randbin(self.sideLen,self.sideLen)
        #self.initLattice = lastConfig.initLattice
        #print initLattice
        # wait variable can slow things down by running a counter inside
        #why do we have a, gl, and gg in here as well as initCML?
        self.cml = DiffusiveCML(self.initLattice,kern='asymm',a=1.5,gl=0.4,gg=0.2,wait=10000)
        #self.cml = DiffusiveCML(self.initLattice,kern='symm4');
        self.stats = AnalysisCML(self.initLattice)
        #cml = DiffusiveCML(initLattice,kern='magic11')
        #cml = CompetitiveCML(initLattice)
        # drawmod is useful to limit framerate or find a cycle avoiding flicker
        self.drawmod=20
        self.kernType='asymm'

        gei = GradientEditorItem()
        gei.loadPreset(self.colorMap)
        self.lut = gei.getLookupTable(self.colorsNum, alpha=False)

class ConfigCML4:

    def __init__(self, lastConfig):
        self.name = "CML4"
        self.sideLen = 80
        self.colorMap = 'blugreen'
        self.colorsNum = 256

        #self.initLattice=randomPing(self.sideLen,self.sideLen,scaleFactor=0.0)

        #self.initLattice=imageCML('./sri_mandala.jpg');
        self.initLattice=magicSquare(self.sideLen)

        #initLattice=primesSquare(sidelen)
        #self.initLattice=randbin(self.sidelen,self.sidelen)
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

        gei = GradientEditorItem()
        gei.loadPreset(self.colorMap)
        self.lut = gei.getLookupTable(self.colorsNum, alpha=False)

class ConfigCML5:

    def __init__(self, lastConfig):
        self.name = "CML5"
        self.sideLen = 80
        self.colorMap = 'grey'
        self.colorsNum = 256

        self.initLattice=randomPing(self.sideLen,self.sideLen,scaleFactor=0.0)

        #self.initLattice=imageCML('./sri_mandala.jpg');
        #self.initLattice=magicSquare(self.sideLen)

        #initLattice=primesSquare(sidelen)
        #self.initLattice=randbin(self.sidelen,self.sidelen)
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

        gei = GradientEditorItem()
        gei.loadPreset(self.colorMap)
        self.lut = gei.getLookupTable(self.colorsNum, alpha=False)


class ConfigCML6:

    def __init__(self, lastConfig):
        self.name = "CML6"
        self.sideLen = 80
        self.colorMap = 'grey'
        self.colorsNum = 256
        #initLattice=imageCML('./sri_mandala.jpg');
        #self.initLattice=randomPing(self.sideLen,self.sideLen,scaleFactor=0.0)
        #self.initLattice=magicSquare(self.sideLen)
        #self.initLattice=primesSquare(self.sideLen)
        self.initLattice=randbin(self.sideLen,self.sideLen)
        #self.initLattice = lastConfig.initLattice
        #print initLattice
        # wait variable can slow things down by running a counter inside
        #why do we have a, gl, and gg in here as well as initCML?
        self.cml = DiffusiveCML(self.initLattice,kern='asymm',a=1.5,gl=0.4,gg=0.2,wait=10000)
        #self.cml = DiffusiveCML(self.initLattice,kern='symm4');
        self.stats = AnalysisCML(self.initLattice)
        #cml = DiffusiveCML(initLattice,kern='magic11')
        #cml = CompetitiveCML(initLattice)
        # drawmod is useful to limit framerate or find a cycle avoiding flicker
        self.drawmod=20
        self.kernType='asymm'

        gei = GradientEditorItem()
        gei.loadPreset(self.colorMap)
        self.lut = gei.getLookupTable(self.colorsNum, alpha=False)