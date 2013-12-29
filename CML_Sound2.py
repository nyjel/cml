# -*- coding: utf-8 -*-
"""
Hybrid CML displayed via a RawImageWidget in QT
For glitch free sound, you want a long buffer in pyo and order 1 on numpy zoom
"""

from pyqtgraph.graphicsItems.GradientEditorItem import GradientEditorItem
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.widgets import RawImageWidget


from numpy import *

from scipy.ndimage import zoom
from scipy.stats import entropy as stentropy
from diffusiveCML import DiffusiveCML
from competitiveCML import CompetitiveCML
from pyo import *
from initCML import *
from analysisCML import *
#
s = Server(sr=44100, nchnls=2,  buffersize=2048, duplex=0).boot()
# set block during music event loops to prevent stats from changing
block=0
# global scale table, must be same size as bins in pat()
freqs = midiToHz([60,50,64,53,67,69,59,72,60,76,55,81,59,85,87,90])
lofreqs = midiToHz([36,43,35,38])
melfreqs=midiToHz([60,62,64,65,67,69,71,72,72,76,67,69,59,73,75,76])
#
melrow=[]
melrowspins=[]
# this is used at beginning of new phrase
lastnote=-1
melcount=0
# threshold of normalized population used to trigger a note in the scale from bins
thresh = 0.06
# how many secs before next long phrase (chords, melodic statements)
phraseTime=8.0
tempo=phraseTime/8.0
basetempo=tempo
computeTime=.02
# transient controls how many iterations to run before sound starts
transient=0
# update sound phrase after soundIter iterations
# if this is high, lots of dynamical evolution
# low numbers, less. Must be >1.  Try 100
soundIter=int(transient/2)
# melodic sequencing and timing adjustment


# setup sound objects for chords
a = BrownNoise(mul=.2)
f = Biquadx(a, freq=freqs, q=80, type=2)
verb=Freeverb(f,size=.8,bal=.8)
# setup sound objects for melody
vibctl = Sine(freq=1.0/phraseTime, mul=2, add=5)
# LFO (square wave) +/- 0.05 (mul) around 0.07 (add), range = 0.02 -> 0.12.
# Control the feedback of the SineLoop oscillator, giving it more harmonics
vibctl = LFO(freq=vibctl, sharp=.8, type=7,mul=3,add=5)
# less popping with dur
#melEnv=Adsr(attack=tempo/2.0-.03, decay=tempo/12.0, sustain=phraseTime, release=tempo/3.0-.03, dur=tempo-.05, mul=.1)
# merging long notes
melEnv=Adsr(attack=tempo/2.0-.03, decay=tempo/12.0, sustain=phraseTime-.5, release=tempo/12, mul=.05)
mel = SineLoop(freq=[250], feedback=.08, mul=melEnv)
melverb=Freeverb(mel,size=.4,bal=.5).out()

def melFromRow():
    global tempo, melrow, melrowspins, melfreqs,lastnote,melcount,block;
    #print "melCount", melrow
    # get next item from row and play note
    # sample melrow at start of tempo cycle
    block=1
    note=int(floor(16* melrow[melcount]))
    notespin=melrowspins[melcount]
    print 'notespin', notespin
    freq = melfreqs[note]
    if note==lastnote:
      # keep playing same note by not releasing dur 0 envelope
      # same note
      print "same note",melcount
      mel.feedback-=.01
      #melPat.time=tempo
    else:
      # end note
      if notespin<0:
          mult=.4
      else:
          mult=.9
      melPat.time=tempo*mult+stats.bins[note]
      if melPat.time>5:
          # somehow think this is a multithread bug where stats is updated while using
          # or used before normalization.  Used temp var in analysis to make less likely,
          # tried to make block vars so that updates don't happen till these code blocks complete
          # That didn't seem to work
          print 'stats.bins', stats.bins
      #print 'note',note,'melPat.time', melPat.time,'tempo',tempo
      mel.feedback+=.01
      mel.freq = [freq+vibctl,freq*0.995+vibctl]
      melEnv.mul=min(.07-stats.bins[note],.07)
      if melcount>0:
          melEnv.stop()
          melEnv.play(delay=melEnv.release+.01)
      else:
          melEnv.play()
      #melPat.time=melPat.time+.01

#


    melcount+=1
    lastnote=note
    if melcount==15:
        melcount=0
        lastnote=-1
        melPat.time=tempo
        mel.feedback=.12
    block=0

#
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
gei.loadPreset('flame')
LUT = gei.getLookupTable(n, alpha=False)

#initLattice=imageCML('/Users/daviddemaris/Dropbox/Public/JungAionFormula.jpg')
#win.resize(size(initLattice,0),size(initLattice,1))

#initLattice=randomCML(sidelen,sidelen)
initLattice=randomPing(sidelen,sidelen)

#initLattice=magicSquare(sidelen)

#initLattice=primesSquare(sidelen)

#initLattice=randbin(sidelen,sidelen)
#print initLattice
cml = DiffusiveCML(initLattice,kern='symm4')
stats=AnalysisCML(initLattice)

#cml = CompetitiveCML(initLattice)


drawmod=2
i=0

def update():

    global i, drawmod,block, cml
    useLut = LUT
    i=i+1

    # diffusion

    cml.iterate()
    stats.update(cml.matrix,i)
    if i>200:
        "changing kern to asymm"
        "changing kern to asymm"
        cml=DiffusiveCML(cml.matrix,kern='magic11')
    # try some spin control

    #print 'spinTrans %d spinTrend %d lastSpinTrend %d alpha %.4f' % (stats.spinTrans, stats.spinTrend, lastSpinTrend, cml.a)
    # experiment with spin control - number of spin transitions < threshold, or else decrease alpha
    """
    if stats.spinTrend>500:
        cml.a=cml.a-.001
    """
    if (i>1 and i % drawmod==0):
        #llshow=cml.matrix*128

        llshow=zoom(((cml.matrix)+1)*128, 8, order=1)
        ## Display the data
        rawImg.setImage(llshow, lut=useLut)


app.processEvents()  ## force complete redraw for every plot
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

def pat():
  # this function is called per phrase
  # good programming practice suggests wrap these globals in a class or classes and make accessor methods
  global cells, f1, freqs, thresh, transient, sidelen, melrow, melrowspins,block
  #global phraseTime
  #global soundIter
  #global computeTime
  block=1

  count= cml.iter
  print "count",count
  # cml.iter seems broken (stays zero) so this only works since transient is set to zero
  if count >= transient:
    if count % 50 == 0:
      # could make the bin range "zoom" to where the action is
      """
      if count < 100:
         bins,edges=histogram(cml.matrix,bins=16,range=(-1.0,1.0))
      else:
        # let the data bounds determine the min and max, giving more resolution around
        # attractors
         bins,edges=histogram(cml.matrix,bins=16)
      # normalize

      bins= bins/float(cells)
      print "in chordPat,bins=",bins
      #plot(bins,16,'r00',linewidth=1.5)
      #longbins=longbins+bins
      #longmean=mean(longbins)
      """

      h=stentropy(stats.bins)  # import stats.entropy, another from distributions was found first

      # if value of normalize bins > thresh, play that note with volume (mul) in
      usedbins=where(stats.bins>thresh)[0].tolist()
      normmax=max(stats.bins)
      subamp=[stats.bins[i] / normmax for i in usedbins]

      subfreq=[freqs[i] for i in usedbins]
      #print count, usedbins
      f.freq=subfreq
      env = Adsr(attack=1, decay=.3, sustain=2, release=2+h/2, dur=4+h/2, mul=subamp)
      a.mul=env
      f.q=12+ h*5
      # next line intended to keep silence until transient period ends
      if count == transient: verb.out()
      # adjust timing based on entropy
      chordPat.time=phraseTime+h
      # this will play the tone set up
      env.play()
       # extract center of center row for 16 note melody, normalize to range 0:1
       # might want to do something like choose average over window in row, subsample
      melrow=(cml.matrix[int(sidelen/2),int(sidelen/2)-8:int(sidelen/2)+8]+1)/2.0
      melrowspins=stats.spin[int(sidelen/2),int(sidelen/2)-8:int(sidelen/2)+8]
    else:
      # need to compute dynamics, stats, and draw 50 per sec or will get glitchy
      chordPat.time=.02
  block=0

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    # chords generated and row sampled for melody
    chordPat =Pattern(pat,phraseTime)
    chordPat.play()
    # melody steps at tempo beats / phrases
    melPat=Pattern(melFromRow,tempo)
    melPat.play()


    s.start()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()