# -*- coding: utf-8 -*-
"""Hybrid CML displayed via a RawImageWidget in QT
For glitch free sound, you want a long buffer in pyo and order 1 on numpy zoom
"""

from pyqtgraph.graphicsItems.GradientEditorItem import GradientEditorItem
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.widgets import RawImageWidget

from numpy import *

from scipy.ndimage import zoom
from configCML import *
from diffusiveCML import DiffusiveCML
from competitiveCML import CompetitiveCML
#from pyo import *
from initCML import *
from analysisCML import *

import pickle
import os, signal, subprocess, time

ggIni=.05
glIni=.2
aIni=1.9
kernIni='asymm'


class CmlGraphics:

    def __init__(self, config):

        self.config = config
        self.scale = 1.0
        gei = GradientEditorItem()

        # see definition of GradientEditorItem() to define an LUT
        # presets cyclic, spectrum, thermal, flame, yellowy, bipolar, greyclip, grey
        #gei.loadPreset(config.colorMap)
        gei.loadPreset('thermal')
        self.lut = gei.getLookupTable(config.colorsNum, alpha=False)

    """
    sidelen=80
    cells=sidelen*sidelen

    #QtGui.QApplication.setGraphicsSystem('raster')
    app = QtGui.QApplication([])

    win = QtGui.QMainWindow()
    win.setWindowTitle('CML Sound Test')
    win.setObjectName("MainWindow")
    win.resize(sidelen*8, sidelen*8)
    #rawImg = RawImageWidget(scaled=True)
    rawImg = RawImageWidget.RawImageWidget()
    win.setCentralWidget(rawImg)
    win.show()

    LUT = None
    n = 256
    gei = GradientEditorItem()
    # see definition of GradientEditorItem() to define an LUT
    # presets cyclic, spectrum, thermal, flame, yellowy, bipolar, greyclip, grey
    gei.loadPreset('blugr2')
    LUT = gei.getLookupTable(n, alpha=False)

    #initLattice=imageCML('/Users/daviddemaris/Dropbox/Public/JungAionFormula.jpg')
    #win.resize(size(initLattice,0),size(initLattice,1))

    #initLattice=randomCML(sidelen,sidelen)
    #initLattice=randomPing(sidelen,sidelen)

    initLattice=magicSquare(sidelen)

    #initLattice=primesSquare(sidelen)

    #initLattice=randbin(sidelen,sidelen)
    #print initLattice
    cml = DiffusiveCML(initLattice,kern=kernIni,gg=ggIni,gl=ggIni,a=aIni,localIter=10)
    stats=AnalysisCML(initLattice)

    #cml = CompetitiveCML(initLattice)


    drawmod=5
    i=0
    """

    def update(self):

        global i  #drawmod,block, cml
        #useLut = None
        i=i+1

        # diffusion
        # experimented with global var block to prevent stats writing vars being read in music events - was getting large values in bins

        self.config.cml.iterate()
        # don't let melody pattern happen during stats write
        #tempTime=melPat.time
        #melPat.time=10000;
        self.config.stats.update(self.config.cml.matrix)
        #melPat.time =tempTime
        #if i>50:
         #   print "was changing kern to asymm"
            #cml=DiffusiveCML(cml.matrix,kern='asymm',a=1.87,gl=0.08,gg=.04)
        # try some spin control

        #print 'spinTrans %d spinTrend %d lastSpinTrend %d alpha %.4f' % (stats.spinTrans, stats.spinTrend, lastSpinTrend, cml.a)
        # experiment with spin control - number of spin transitions < threshold, or else decrease alpha
        """
        if stats.spinTrend>500:
            cml.a=cml.a-.001
        """
        if (i>1 and i % self.config.drawmod==0):
            #llshow=cml.matrix*128

            scaledVal = (self.config.cml.matrix * self.scale)+1
            llshow = zoom(scaledVal*128, 8, order=1)
            #llshow=zoom(((stats.spin)+1)*128, 8, order=1)
            ## Display the data
            rawImg.setImage(llshow, lut=self.config.lut)
        #if i==10000:
        #    s.recstop()

    def cmlPat(self):

        global aIni, ggIni, glIni

        if self.cmlPhase==0:
            print "quench"
            self.cmlPhase=1
            self.cml.a=1.76
            self.cml.gg=.1
            self.cml.gl=.2
            self.cml.kernelType="symm4"
            self.cml.kernelUpdate()
        else:
            print "normal"
            cmlPhase=0
            self.cml.a=aIni
            self.cml.gg=ggIni
            self.cml.gl=glIni
            self.cml.kernelType = config.kernType
            self.cml.kernelUpdate()

    def writeStatsToFile(self):
        global audioIndex, queue, stats
        audioIndex = audioIndex + 1
        with open("stats.dat", 'wb') as f:
            print "writing to stats", audioIndex
            pickle.dump(self.config.stats, f)

    def nextConfig(self):
        global configIndex, configClassesWaits, confTimer
        configIndex = configIndex + 1;
        if (configIndex >= len(configClassesWaits)):
            configIndex = 0
        self.config = configClassesWaits[configIndex][0](self.config)
        print "Switched to config", self.config.name
        # Kill outstanding timer
        if (not confTimer is None):
            confTimer.stop()
        # Create a new timer for current config duration,
        # with a timout handler of this method
        confTimer  = QtCore.QTimer()
        confTimer.timeout.connect(self.nextConfig)
        confTimer.start(configClassesWaits[configIndex][1])

    ### reset to the final config, run for duration of 'finalWait'
    ### then fade to black
    def finalConfig(self):
        global configIndex, configClassesWaits, confTimer, finalConfig, finalWait
        self.config = finalConfig(self.config)
        print "Switched to final config", self.config.name
        # Kill outstanding timer
        if (not confTimer is None):
            confTimer.stop()
        # Create a new timer for current config duration,
        # with a timout handler of the fade out
        confTimer  = QtCore.QTimer()
        confTimer.timeout.connect(self.fadeToBlack)
        confTimer.start(finalWait)

    def fadeToBlack(self):
        print "Fading to black: scale", self.scale
        global confTimer, fadeDecrement
        # Kill outstanding timer
        if (not confTimer is None):
            confTimer.stop()
        self.scale = self.scale - fadeDecrement
        if (self.scale > 0):
            confTimer  = QtCore.QTimer()
            confTimer.timeout.connect(self.fadeToBlack)
            confTimer.start(100) # 1 tenth sec

### A main window class with an even handler
class MyQMainWin(QtGui.QMainWindow):

    def keyPressEvent(self, e):

        global subProcess
        print "KeyPress", e.key()

        # Escape -> exit
        if (e.key() == QtCore.Qt.Key_Escape):
            # kill the sound subprocess
            os.kill(subProcess.pid, signal.SIGTERM)
            # kill self
            self.close()
        # space -> next config
        elif (e.key() == QtCore.Qt.Key_Space):
            graphics.nextConfig()
        # backspace -> final config
        elif (e.key() == QtCore.Qt.Key_Backspace):
            graphics.finalConfig()



if __name__ == '__main__':

    import sys

    audioIndex = 0;
    configIndex = -1;
    #  A list of pairs of:
    #     - configuration class of this configuration
    #     - duration to display this config b4 moving to next (msecs)
    configClassesWaits = [
        [ConfigCML, 30000],
        [ConfigCML2, 30000],
        #[ConfigCML3, 3000],
        [ConfigCML4, 30000],
        [ConfigCML5, 30000],
        ]

    finalConfig = ConfigCML6
    finalWait = 3000
    finalFadeDuration = 5000
    fadeDecrement = 100.0 / finalFadeDuration


    i=0
    app = QtGui.QApplication([])
    win = MyQMainWin()
    win.setWindowTitle('CML Sound Test')
    win.setObjectName("MainWindow")

    config = ConfigCML(None)

    win.resize(config.sideLen*8, config.sideLen*8)

    #rawImg = RawImageWidget(scaled=True)
    rawImg = RawImageWidget.RawImageWidget()
    win.setCentralWidget(rawImg)
    win.show()

    app.processEvents()  ## force complete redraw for every plot
    timer = QtCore.QTimer()

    graphics = CmlGraphics(config)
    timer.timeout.connect(graphics.update)
    timer.start(0)

    timer2 = QtCore.QTimer()
    timer2.timeout.connect(graphics.writeStatsToFile)
    timer2.start(1000)

    #timer3 = QtCore.QTimer()
    #timer3.timeout.connect(graphics.nextConfig)
    #timer3.start(10000)

    confTimer = None
    graphics.nextConfig()

    # Launch sound CML subprocess and process in global var
    subProcess = subprocess.Popen(args=["python CML4_Sound.py"], shell=True)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

    print 'end of CML3_Graphics'

