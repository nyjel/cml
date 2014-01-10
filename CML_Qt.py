# -*- coding: utf-8 -*-
"""
Hybrid CML displayed via a RawImageWidget in QT
For glitch free sound, you want a long buffer in pyo and order 1 on numpy zoom
"""

from pyqtgraph.graphicsItems.GradientEditorItem import GradientEditorItem
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.widgets import RawImageWidget


from numpy import *
from numpy.random import rand
from scipy.signal import convolve2d
from scipy.ndimage import zoom
from diffusiveCML import DiffusiveCML
#
#from competitiveCML import CompetitiveCML

from initCML import *
from analysisCML import *
sidelen=80

#cells=sidelen**2


#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])

win = QtGui.QMainWindow()
win.setWindowTitle('pyqtgraph example: VideoSpeedTest')
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
# presets cyclic, spectrum, thermal, flame, yellowy, bipolar, greyclip, grey,bluish
# was cyclic, pretty nice
gei.loadPreset('cyclic')
LUT = gei.getLookupTable(n, alpha=False)

def update():

    global  drawmod
    useLut = LUT

    # diffusion
    cml.iterate()
    # calculate various statistics used for control and influencing musical parameters
    stats.update(cml.matrix,cml.iter)
    # try some spin control

    #print 'spinTrans %d spinTrend %d lastSpinTrend %d alpha %.4f' % (stats.spinTrans, stats.spinTrend, lastSpinTrend, cml.a)
    # experiment with spin control - number of spin transitions > threshold, or else decrease alpha
    # if a is chaotic, it will search and find a more stable (but probably still chaotic) value reducing spin transitions
    if stats.spinTrend>500:
        cml.a=cml.a-.001

    if (cml.iter>1 and cml.iter % drawmod==0):
        # if an image is big, don't do the scaling but rather use it direct.  Could we somtoth
        #llshow=cml.matrix*128

        #llshow=zoom(((cml.matrix)+1)*128, 8, order=3)
        llshow=zoom(((stats.spin)+1)*128, 8, order=2)
        ## Display the data
        rawImg.setImage(llshow, lut=useLut)

# Various initial lattice styles
cmlInit=''
#initLattice=imageCML('/Users/daviddemaris/Dropbox/Public/JungAionFormula.jpg')
#win.resize(size(initLattice,0),size(initLattice,1))
#cmlInit='image'
#initLattice=randomCML(sidelen,sidelen)
#initLattice=randomPing(sidelen,sidelen,scale=0.0)
#initLattice=magicSquare(sidelen)
initLattice=primesSquare(sidelen)
#initLattice=randbin(sidelen,sidelen)
#print initLattice
# wait variable can slow things down by running a counter inside
cml = DiffusiveCML(initLattice,kern='asymm',a=1.755,gl=0.07,gg=0.07,wait=10000)
stats = AnalysisCML(initLattice)
#cml = DiffusiveCML(initLattice,kern='magic11')
#cml = CompetitiveCML(initLattice)
# drawmod is useful to limit framerate or find a cycle avoiding flicker
drawmod=7


def update():

    global  drawmod, cmlInit
    useLut = LUT

    # diffusion
    cml.iterate()
    # calculate various statistics used for control and influencing musical parameters
    stats.update(cml.matrix,cml.iter)
    # try some spin control

    #print 'spinTrans %d spinTrend %d lastSpinTrend %d alpha %.4f' % (stats.spinTrans, stats.spinTrend, lastSpinTrend, cml.a)
    # experiment with spin control - number of spin transitions > threshold, or else decrease alpha
    # if a is chaotic, it will search and find a more stable (but probably still chaotic) value reducing spin transitions
    if stats.spinTrend>500:
        cml.a=cml.a-.001

    if (cml.iter>1 and cml.iter % drawmod==0):
        # if an image is big, don't do the scaling but rather use it direct.
        if cmlInit=='image':
            llshow=cml.matrix*128
        else:
            llshow=zoom(((cml.matrix)+1)*128, 8, order=2)
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
