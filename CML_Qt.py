# -*- coding: utf-8 -*-
"""
Hybrid CML displayed via a RawImageWidget in QT
"""

from pyqtgraph.graphicsItems.GradientEditorItem import GradientEditorItem
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph import RawImageWidget

from numpy import *
from numpy.random import rand
from scipy.signal import convolve2d
from scipy.ndimage import zoom
from generator import Generator

sidelen=128
#cells=sidelen**2

#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])

win = QtGui.QMainWindow()
win.setWindowTitle('pyqtgraph example: VideoSpeedTest')
win.setObjectName("MainWindow")
win.resize(sidelen*8, sidelen*8)
#rawImg = RawImageWidget(scaled=True)
rawImg = RawImageWidget()
win.setCentralWidget(rawImg)
win.show()

LUT = None
n = 256
gei = GradientEditorItem()
gei.loadPreset('cyclic')
LUT = gei.getLookupTable(n, alpha=False)

llshow=rand(sidelen,sidelen)

gen = Generator(sidelen, sidelen)

drawmod=20
i=0

def update():

    global i, drawmod
    useLut = LUT
    i=i+1

    # diffusion
    gen.iterate()

    if (i>1 and i % drawmod==0): 
    
        llshow=zoom((gen.matrix)*128, 8, order=2)
        ## Display the data
        rawImg.setImage(llshow, lut=useLut)


app.processEvents()  ## force complete redraw for every plot
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
