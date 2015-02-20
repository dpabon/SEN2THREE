'''
Created on Feb 19, 2015

@author: umwilm
'''
from numpy import *
import pylab as P
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import matplotlib.mlab as mlab
from scipy.stats import itemfreq

from L3_Config import L3_Config
from L3_Tables import L3_Tables
from L3_Library import stdoutWrite, stderrWrite, showImage

class L3_Statistics(object):
    def __init__(self, config, tables):
        self._config = config
        self._tables = tables
        self._noData = config.classifier['NO_DATA']
        self._minTime = config.minTime
        self._maxTime = config.maxTime
        

    def display(self):
        mosaic = self._tables.getBand('L3', self._tables.MSC)
        scenec = self._tables.getBand('L3', self._tables.SCL)
        nr, nc = scenec.shape
        ratio = float(nr)/float(nc)
        if ratio > 2.5:
            ax1 = P.subplot2grid((2,3), (0,0), rowspan=2) 
            ax2 = P.subplot2grid((2,3), (0,1), rowspan=2) 
            ax3 = P.subplot2grid((2,3), (0,2))
            ax4 = P.subplot2grid((2,3), (1,2))
        else:
            ax1 = P.subplot2grid((2,2), (0,0)) 
            ax2 = P.subplot2grid((2,2), (1,0)) 
            ax3 = P.subplot2grid((2,2), (0,1))
            ax4 = P.subplot2grid((2,2), (1,1))            
        
        mosaicData = [mosaic != self._noData]
        tiles = self._config.nrTilesProcessed + 1
        yMoif = zeros(tiles, dtype=float32)
        moif = itemfreq(mosaic[mosaicData])
        print moif
        for i in range(len(moif)):
            yMoif[moif[i,0]] = moif[i,1]
        yMoif = yMoif.astype(float32)/moif[:,1].sum() * 100.0               
        xMoif = arange(tiles)
        
        scenecData = [scenec != self._noData]
        classes = ('Sat','Dark','Soil','Snow','Veg','Water','LPC','MPC','HPC','Cirr','ClS')
        yScif = zeros(len(classes), dtype=float32)
        scif = itemfreq(scenec[scenecData])
        for i in range(len(scif)):
            yScif[scif[i,0]] = scif[i,1]
        yScif = yScif.astype(float32)/scif[:,1].sum() * 100.0
        xScif = arange(len(classes))                
        
        ax1.imshow(mosaic, cmap='jet', interpolation='nearest')
        ax2.imshow(scenec, cmap='jet', interpolation='nearest')
        ax3.bar(xMoif, yMoif, align='center', alpha=0.4)
        ax4.bar(xScif, yScif, align='center', alpha=0.4)

        P.tight_layout()
        P.show()
        P.close()    
        return