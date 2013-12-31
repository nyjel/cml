
from numpy import *
from numpy.random import rand
import sys
import time
from PIL import Image
from magic_square import *

def imageCML(imagePath,scaleFactor=1.0):
    img=Image.open(imagePath)
    #img=Image.open('/Users/david/Desktop/shri_mandala.jpg')
    img=img.convert('L')

    ll=array(img.getdata(),float).reshape(img.size[1], img.size[0])
    xlen=img.size[1]
    ylen=img.size[0]
    # scale into range 0,1
    ll=ll/ndarray.max(ll) * scaleFactor
    return ll

def randomCML(xside,yside,cmlType='KK',scaleFactor=1.0):
    ll=rand(xside,yside)
    if cmlType == 'KK':
        ll=((ll*1.999)-.999)*scaleFactor
    else:
        ll=ll*scaleFactor
    return ll

def randomPing(xside,yside,cmlType='KK',scale=.000000000001):
    ll=rand(xside,yside)*scale
    if cmlType == 'KK':
        ll=((ll*1.999)-.999*scale)
        ll[xside/2,yside/2]=.99
    else:
        # in case we add a domain 0 to 1 map
        ll[xside/2,yside/2]=.99
    return ll

def randbin(xlen,ylen,scaleFactor=1.0):
    ll=rand(xlen, ylen)
    ll[where(ll>=.5)]=1.0
    ll[where(ll<.5)]=0.0
    return ll

def magicSquare(n):
    ll=magic(n)/(n*n*1.0)
    return ll

def primesSquare(n):
    N=n*n
    primes  = []
    chkthis = 2
    while len(primes) < N:
        ptest    = [chkthis for i in primes if chkthis%i == 0]
        primes  += [] if ptest else [chkthis]
        chkthis += 1

    ll=reshape(primes,(n,n))/(primes[N-1]*1.0) # mult by one to get floats otherwise you get all zero
    return ll