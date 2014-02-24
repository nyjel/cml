# -*- coding: utf-8 -*-
"""
Use GLImageItem to display image data on rectangular planes.

In this example, the image data is sampled from a volume and the image planes
placed as if they slice through the volume.
"""
## Add path to library (just for examples; you do not need this)

from pyqtgraph.graphicsItems.GradientEditorItem import GradientEditorItem
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import scipy.ndimage as ndi

from scipy.ndimage import zoom
from diffusiveCML import DiffusiveCML
from initCML import *
from analysisCML import *
sidelen=80



app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 500 # was 200 in demo

w.show()
w.setWindowTitle('pyqtgraph example: GLImageItem')
LUT = None
n = 256
gei = GradientEditorItem()
# see definition of GradientEditorItem() to define an LUT
# presets cyclic, spectrum, thermal, flame, yellowy, bipolar, greyclip, grey,bluish
# was cyclic, pretty nice
gei.loadPreset('cyclic')
LUT = gei.getLookupTable(n, alpha=False)
## create volume data set to slice three images from
"""
shape = (100,100,70)
data = ndi.gaussian_filter(np.random.normal(size=shape), (4,4,4))
data += ndi.gaussian_filter(np.random.normal(size=shape), (15,15,15))*15
"""
initLattice=randomPing(sidelen,sidelen)

#initLattice=magicSquare(sidelen)

#initLattice=primesSquare(sidelen)

#initLattice=randbin(sidelen,sidelen)
#print initLattice
cml = DiffusiveCML(initLattice,kern='symm4')
#stats = AnalysisCML(initLattice)
drawmod=1
v1=1
def update():

    global  drawmod, v1, LUT

    # diffusion
    cml.iterate()
    # calculate various statistics used for control and influencing musical parameters
    #stats.update(cml.matrix,cml.iter)

    if (cml.iter % drawmod==0):
        # if an image is big, don't do the scaling but rather use it direct.  Could we somtoth
        #llshow=cml.matrix*128

        if cml.iter>1:
            w.removeItem(v1)
        ## slice out three planes, convert to RGBA for OpenGL texture
        #levels = (-0.08, 0.08)
        llshow=zoom(((cml.matrix)+1)*128, 4, order=4)
        tex1 = pg.makeRGBA(llshow,lut=LUT)[0]       # yz plane
        ## Create image items from textures, add to view
        v1 = gl.GLImageItem(tex1)
        v1.translate(-llshow.shape[0]/2, -llshow.shape[1]/2, 0)
        #v1.rotate(90, 0,0,1)
        #v1.rotate(-90, 0,1,0)
        w.addItem(v1)


        ax = gl.GLAxisItem()
        w.addItem(ax)

app.processEvents()  ## force complete redraw for every plot
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
