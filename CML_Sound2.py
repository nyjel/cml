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
thresh = 0.1
# how many secs before next long phrase (chords, melodic statements)
phraseTime=4.0
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
#melEnv=Adsr(attack=tempo/2.0-.03, decay=tempo/12.0, sustain=phraseTime-.5, release=tempo/12, mul=.05)
#melEnv=Adsr(attack=tempo/2, decay=tempo, sustain=tempo, release=tempo/4, mul=.05)
melEnv=Adsr(attack=tempo/5, decay=tempo/5, sustain=tempo/5, release=tempo/5, mul=1, dur=tempo-.1)
mel = SineLoop(freq=[250], feedback=.12, mul=melEnv)
melverb=Freeverb(mel,size=.4,bal=.5).out()
melcount=0
cmlPhase=0

def melFromRow():

    global tempo, melrow, melrowspins, melfreqs,lastnote,melcount,block;
    print "melcount", melcount, "melrow", melrow

    # if melrow not yet initialized, exit
    if len(melrow) == 0:
        return

    # get next item from row and play note
    # sample melrow at start of tempo cycle
    block=1
    note=int(floor(16* melrow[melcount]))
    notespin=melrowspins[melcount]
    print 'note', note, 'notespin', notespin
    freq = melfreqs[note]
    if note==lastnote:
      # keep playing same note by not releasing dur 0 envelope
      # same note
      #print "same note",melcount
      mel.feedback-=.01
      #melPat.time=tempo
    else:
      # end note
      if notespin<0:
          mult=.5
      else:
          mult=1.0
      # was -stats.bin
      #melPat.time=tempo*mult+stats.bins[note]
      if melPat.time>5:
          # somehow think this is a multithread bug where stats is updated while using
          # or used before normalization.  Used temp var in analysis to make less likely,
          # tried to make block vars so that updates don't happen till these code blocks complete
          # That didn't seem to work
          print 'stats.bins', stats.bins
      print 'note',note,'melPat.time', melPat.time,'tempo',tempo
      mel.feedback=.12-.1*stats.bins[note]
      mel.freq = [freq+vibctl,freq*0.995+vibctl]
      #melEnv.mul=.04+stats.bins[note]*2*0.03
      #melEnv.mul=min(.07-stats.bins[note],.07)
      #if melcount>0:
      if False:
          melEnv.stop()

          # finish note and delay, but also need to delay next melody cycle?
          # try changing time before play
          melEnv.play(delay=melEnv.release)
          melPat.time=melPat.time+melEnv.release+.5

          #melPat.time=melPat.time+melEnv.release
      else:
          #melEnv.play()
          #melEnv.play()
          xxx = 11
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
gei.loadPreset('cyclic')
LUT = gei.getLookupTable(n, alpha=False)

#initLattice=imageCML('/Users/daviddemaris/Dropbox/Public/JungAionFormula.jpg')
#win.resize(size(initLattice,0),size(initLattice,1))

#initLattice=randomCML(sidelen,sidelen)
#initLattice=randomPing(sidelen,sidelen)

initLattice=magicSquare(sidelen)

#initLattice=primesSquare(sidelen)

#initLattice=randbin(sidelen,sidelen)
#print initLattice
ggIni=.05
glIni=.2
aIni=1.9
kernIni='asymm'
#cml = DiffusiveCML(initLattice,kern=kernIni,gg=ggIni,gl=ggIni,a=aIni)
cml = DiffusiveCML(initLattice,kern='magic11',a=1.685,gl=0.0,gg=0.02,wait=10000,localIter=10)
stats=AnalysisCML(initLattice)

#cml = CompetitiveCML(initLattice)


drawmod=5
i=0

def update():

    global i, drawmod,block, cml
    useLut = LUT
    i=i+1

    # diffusion
    # experimented with global var block to prevent stats writing vars being read in music events - was getting large values in bins

    cml.iterate()
    # don't let melody pattern happen during stats write
    tempTime=melPat.time
    melPat.time=10000;
    stats.update(cml.matrix,i)
    melPat.time =tempTime
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
    if (i>1 and i % drawmod==0):
        #llshow=cml.matrix*128

        #llshow=zoom(((cml.matrix)+1)*128, 8, order=1)
        llshow=zoom(((stats.spin)+1)*128, 8, order=1)
        ## Display the data
        rawImg.setImage(llshow, lut=useLut)
    if i==10000:
        s.recstop()

#app.processEvents()  ## force complete redraw for every plot
#timer = QtCore.QTimer()
#timer.timeout.connect(update)
#timer.start(0)

def pat():
  # this function is called per phrase
  # good programming practice suggests wrap these globals in a class or classes and make accessor methods
  global cells, f1, freqs, thresh, transient, sidelen, melrow, melrowspins,block
  #global phraseTime
  #global soundIter
  #global computeTime
  block=1

  count= cml.iter
  # cml.iter seems broken (stays zero) so this only works since transient is set to zero
  if count >= transient:

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

      h=stats.entropy  # import stats.entropy, another from distributions was found first

      # if value of normalize bins > thresh, play that note with volume (mul) in
      usedbins=where(stats.bins>thresh)[0].tolist()
      normmax=max(stats.bins)
      subamp=[stats.bins[i] / normmax * 0.5 for i in usedbins]

      subfreq=[freqs[i] for i in usedbins]
      #print count, usedbins
      f.freq=subfreq
      # modify envelope based on entropy measure h
      env = Adsr(attack=1, decay=.3, sustain=2, release=2+h/2, dur=4+h/2, mul=subamp)
      a.mul=env
      f.q=12+ h*5
      # next line intended to keep silence until transient period ends
      verb.out()
      # adjust timing based on entropy
      chordPat.time=phraseTime+h
      # this will play the tone set up
      env.play()
       # extract center of center row for 16 note melody, normalize to range 0:1
       # might want to do something like choose average over window in row, subsample
      melrow=(cml.matrix[int(sidelen/2),int(sidelen/2)-8:int(sidelen/2)+8]+1)/2.0
      melrowspins=stats.spin[int(sidelen/2),int(sidelen/2)-8:int(sidelen/2)+8]

def cmlPat():
    global ggIni, glIni, aIni, cml, cmlPhase

    if cmlPhase==0:
        print "quench"
        cmlPhase=1
        cml.a=1.76
        cml.gg=.1
        cml.gl=.2
        cml.kernelType="symm4"
        cml.kernelUpdate()
    else:
        print "normal"
        cmlPhase=0
        cml.a=aIni
        cml.gg=ggIni
        cml.gl=glIni
        cml.kernelType=kernIni
        cml.kernelUpdate()


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    # chords generated and row sampled for melody
    chordPat =Pattern(pat,phraseTime)
    chordPat.play()
    # melody steps at tempo beats / phrases
    melPat=Pattern(melFromRow,tempo)
    melPat.play()
    cmlLFO=tempo * 4.0

    cmlPat=Pattern(cmlPat,cmlLFO)
    cmlPat.play()
    s.start()
    s.recstart()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
