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

ll=rand(sidelen,sidelen)
llshow=rand(sidelen,sidelen)

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

gen = Generator(sidelen, sidelen)

def update():
#    global ui, ptr, lastTime, fps, LUT, img
    global a,drawmod,gg,gl,cc,dkern,i,ll,I,llshow,LUT,ui, rawImg

    useLut = LUT
    i=i+1

    # diffusion
    gen.iterate()

    if (i>1 and i % drawmod==0): 
    
        llshow=zoom((gen.matrix)*128, 8, order=2)
        ## Display the data
        rawImg.setImage(llshow, lut=useLut)

        if (i % 80 == 0):
                  gg=gg+.001
                  #a=a-.001
                  if gg<.04 : gg=gg+.02

app.processEvents()  ## force complete redraw for every plot
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
