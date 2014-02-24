# -*- coding: utf-8 -*-
"""
Saves CML output to png files
"""
import time
import png
import threading
from threading import Timer
import atexit
import numpy as np
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

# Various initial lattice styles
cmlInit=''
#initLattice=imageCML('/Users/daviddemaris/Dropbox/Public/JungAionFormula.jpg')
#win.resize(size(initLattice,0),size(initLattice,1))
#cmlInit='image'
initLattice=imageCML('./sri_mandala.jpg');
#initLattice=randomPing(sidelen,sidelen,scaleFactor=0.0)
#initLattice=magicSquare(sidelen)
#initLattice=primesSquare(sidelen)
#initLattice=randbin(sidelen,sidelen)
#print initLattice
# wait variable can slow things down by running a counter inside
#why do we have a, gl, and gg in here as well as initCML?
#cml = DiffusiveCML(initLattice,kern='asymm',a=1.5,gl=0.4,gg=0.2,wait=10000)
cml = DiffusiveCML(initLattice,kern='symm4');
stats = AnalysisCML(initLattice)
#cml = DiffusiveCML(initLattice,kern='magic11')
#cml = CompetitiveCML(initLattice)
# drawmod is useful to limit framerate or find a cycle avoiding flicker
drawmod=1

last_render_time = 0
frame = 0
def update():
    global  drawmod, cmlInit, last_render_time, frame

    # diffusion
    cml.iterate()
    # calculate various statistics used for control and influencing musical parameters
    stats.update(cml.matrix,cml.iter)
    # try some spin control

    #print 'spinTrans %d spinTrend %d lastSpinTrend %d alpha %.4f' % (stats.spinTrans, stats.spinTrend, lastSpinTrend, cml.a)
    # experiment with spin control - number of spin transitions > threshold, or else decrease alpha
    # if a is chaotic, it will search and find a more stable (but probably still chaotic) value reducing spin transitions
    print(cml.iter),
    if stats.spinTrend>500:
        print "reducing alpha"
        cml.a=cml.a-.001
    if (cml.iter>1 and cml.iter % drawmod==0):	    
        #calculating fps with goal of 30fps
        current_time = time.time()
        render_time = current_time - last_render_time
        last_render_time = current_time
        fps = round(1/render_time)
	#try to get fps up to 30.
	drawmod = 1
	scaled = (cml.matrix+1)*64
	done = np.array(scaled).astype(short).tolist()
	#print(done)
        ## Display the data
	filename = "frame" + str(frame) + ".png"
	png.from_array(done, 'L').save(filename)
	frame+=1
    

class Repeat(object):
    count = 0
    @staticmethod
    def repeat(rep, delay, func):
        #repeat func rep times with a delay given in seconds
        if Repeat.count < rep:
            func()
            Repeat.count += 1
            timer = Timer(delay, Repeat.repeat, (rep, delay, func))
            atexit.register(timer.cancel)
            timer.start()
total_frames = 100
if(sys.argv[1]):
     total_frames = sys.argv[1]
Repeat.repeat(200,.01,update)
