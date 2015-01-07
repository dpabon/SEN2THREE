#!/usr/bin/env python

from numpy import *
from PIL import Image
from L3_Config import L3_Config
from scipy import ndimage
from scipy import stats
from scipy.signal import medfilt2d
from scipy.signal import medfilt
from scipy.ndimage import map_coordinates
from scipy import interpolate as sp
from scipy import stats
from scipy.ndimage.filters import uniform_filter
from matplotlib import pyplot as plt

import time
import os, sys, fnmatch

def stdoutWrite(s):
    sys.stdout.write(s)
    sys.stdout.flush()
    

def stderrWrite(s):
    sys.stderr.write(s)
    sys.stderr.flush() 


def statistics(arr, comment = ''):
    if len(arr) == 0:
        return False
    s = 'object:' + str(comment) + '\n'
    s += '--------------------' + '\n'
    s += 'shape: ' + str(shape(arr)) + '\n'
    s += 'sum  : ' + str(arr.sum()) + '\n'
    s += 'mean : ' + str(arr.mean()) + '\n'
    s += 'std  : ' + str(arr.std())  + '\n'
    s += 'min  : ' + str(arr.min())  + '\n'
    s += 'max  : ' + str(arr.max())  + '\n'
    s += '-------------------' + '\n'
    return s


def showImage(arr):
    if(arr.ndim) != 2:
        print('Must be a two dimensional array')
        return False

    arrmin = arr.mean() - 3*arr.std()
    arrmax = arr.mean() + 3*arr.std()
    arrlen = arrmax-arrmin
    arr = clip(arr, arrmin, arrmax)
    scale = 255.0
    scaledArr = (arr-arrmin).astype(float32) / float32(arrlen) * scale
    arr = (scaledArr.astype(uint8))
    #plt.imshow(arr, interpolation='nearest')
    #plt.show()
    img = Image.fromarray(arr)
    img.show()
    return True


def reverse(a): return a[::-1]


