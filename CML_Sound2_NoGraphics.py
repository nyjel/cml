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

# competitive CML is very interesting but somehow doesn't work in pycharm, gives numerical errors
#from competitiveCML import CompetitiveCML
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
# i.e. a bin only plays a note in the chord if the fraction of cells in lattice exceeds thresh
thresh = 0.06
# how many secs before next long phrase (chords, melodic statements)
phraseTime=8.0
tempo=phraseTime/8
basetempo=tempo
computeTime=.02
# transient controls how many iterations to run before sound starts
transient=1
# update sound phrase after soundIter iterations
# if this is high, lots of dynamical evolution
# low numbers, less. Must be >1.  Try 100
soundIter=int(transient/2)
# melodic sequencing and timing adjustment


# setup sound objects for chords
a = BrownNoise(mul=.2)
# filter the brown noise into bands defined by freqs pitch array defined babove
f = Biquadx(a, freq=freqs, q=80, type=2)
# put it through some verb
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
    #print "melcount",melcount, "melrow",melrow
    note=int(floor(16* melrow[melcount]))
    notespin=melrowspins[melcount]
    #print 'notespin', notespin
    freq = melfreqs[note]
    if note==lastnote:
      # keep playing same note by not releasing dur 0 envelope
      # same note
      #print "same note",melcount
      mel.feedback-=.008
      #melPat.time=tempo
    else:
      # end note
      if notespin<0:
          mult=.5
      else:
          mult=1.0
      melPat.time=tempo*mult+stats.bins[note]
      if melPat.time>5:
          # somehow think this is a multithread bug where stats is updated while using
          # or used before normalization.  Used temp var in analysis to make less likely,
          # tried to make block vars so that updates don't happen till these code blocks complete
          # That didn't seem to work
          print 'stats.bins', stats.bins
      #print 'note',note,'melPat.time', melPat.time,'tempo',tempo
      mel.feedback+=.01
      # second arg is just a detuned osc for richness
      mel.freq = [freq+vibctl,freq*0.995+vibctl]
      #
      melEnv.mul=.06+stats.bins[note]*0.03  # make max 0.9
      if melcount>0:
          melEnv.stop()
          # this should do the release then start next note, but next note seems to often start causing click
          #melPat.time=tempo
          melEnv.play(delay=melEnv.release+.05)
      else:
          #print "play without delay"
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


sidelen=80


#initLattice=imageCML('/Users/daviddemaris/Dropbox/Public/JungAionFormula.jpg')
#win.resize(size(initLattice,0),size(initLattice,1))

initLattice=randomCML(sidelen,sidelen)
#initLattice=randomPing(sidelen,sidelen)

#initLattice=magicSquare(sidelen)

#initLattice=primesSquare(sidelen)

#initLattice=randbin(sidelen,sidelen)


cml = DiffusiveCML(initLattice,kern='symm4')
stats=AnalysisCML(initLattice)

#cml = CompetitiveCML(initLattice)

def update():

    global cml

    # diffusion
    # experimented with global var block to prevent stats writing vars being read in music events - was getting large values in bins
    cml.iterate()
    stats.update(cml.matrix,cml.iter)
    # try some spin control

    #print 'spinTrans %d spinTrend %d lastSpinTrend %d alpha %.4f' % (stats.spinTrans, stats.spinTrend, lastSpinTrend, cml.a)
    # experiment with spin control - number of spin transitions < threshold, or else decrease alpha
    """
    if stats.spinTrend>500:
        cml.a=cml.a-.001
    """

def pat():
  # this function is called per phrase
  # good programming practice suggests wrap these globals in a class or classes and make accessor methods
  global f1, freqs, thresh, transient, sidelen, melrow, melrowspins,block

  count= cml.iter

  if count >= transient:
    if count % 1 == 0:

      h=stats.entropy  # import stats.entropy, another from distributions was found first

      # if value of normalize bins > thresh, play that note with volume (mul) in
      usedbins=where(stats.bins>thresh)[0].tolist()
      normmax=max(stats.bins)
      subamp=[stats.bins[i] / normmax for i in usedbins]

      subfreq=[freqs[i] for i in usedbins]
      #print count, usedbins
      f.freq=subfreq
      env = Adsr(attack=1, decay=.3, sustain=2, release=2+h/2, dur=4+h/2, mul=subamp)
      # mul is the amplitude, controld by the envelope just defined
      a.mul=env
      # use entropy to adjust chord filter resonance
      f.q=12+ h*5
      # next line intent is to start chords after transient period ends
      verb.out()
      """
      # need to revisit this since running async with patterns, count goes very fast compared to time
      if count == transient:
          print "verb on"
          verb.out()
      """
      # adjust timing based on entropy
      chordPat.time=phraseTime+h
      tempo=chordPat.time/8.0
      # this will play the tone set up
      env.play()
       # extract center of center row for 16 note melody, normalize to range 0:1
       # might want to do something like choose average over window in row, subsample
      melrow=(cml.matrix[int(sidelen/2),int(sidelen/2)-8:int(sidelen/2)+8]+1)/2.0
      melrowspins=stats.spin[int(sidelen/2),int(sidelen/2)-8:int(sidelen/2)+8]
    else:
      # need to compute dynamics, stats, and draw 50 per sec or will get glitchy
      #chordPat.time=.02
      chordPat.time=phraseTime

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
    while True:
        update()
