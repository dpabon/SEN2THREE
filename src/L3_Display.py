'''
Created on Feb 19, 2015

@author: umwilm
'''
from numpy import *
import pylab as P
from scipy.stats import itemfreq

from L3_Config import L3_Config
from L3_Tables import L3_Tables
from L3_Library import stdoutWrite, stderrWrite, showImage

class L3_Display(object):
    def __init__(self, config):
        self._config = config
        self._tables = None
        self._noData = config.classifier['NO_DATA']
        self._minTime = config.minTime
        self._maxTime = config.maxTime
        self._plot = P
        self._plot.ion()
     
    def displayData(self, tables):
        self._tables = tables
        mosaic = self._tables.getBand('L3', self._tables.MSC)
        scenec = self._tables.getBand('L3', self._tables.SCL)
        nr, nc = scenec.shape
        ratio = float(nr)/float(nc)
        fig = self._plot.figure()
        fig.patch.set_facecolor('white')
        if ratio > 2.5:
            ax1 = self._plot.subplot2grid((2,3), (0,0), rowspan=2) 
            ax2 = self._plot.subplot2grid((2,3), (0,1), rowspan=2) 
            ax3 = self._plot.subplot2grid((2,3), (0,2))
            ax4 = self._plot.subplot2grid((2,3), (1,2))
        else:
            ax1 = self._plot.subplot2grid((2,2), (0,0)) 
            ax2 = self._plot.subplot2grid((2,2), (1,0)) 
            ax3 = self._plot.subplot2grid((2,2), (0,1))
            ax4 = self._plot.subplot2grid((2,2), (1,1))            
        
        mosaicData = [mosaic != self._noData]
        tiles = self._config.nrTilesProcessed+1
        xMoif = arange(tiles)
        yMoif = zeros(tiles, dtype=float32)
        moif = itemfreq(mosaic[mosaicData])
        for i in range(len(moif)):
            xMoif[i] = moif[i,0]
            yMoif[i] = moif[i,1]

        yMoif = yMoif.astype(float32)/moif[:,1].sum() * 100.0
        scenecData = [scenec != self._noData]
        classes = ('Sat','Dark','Soil','Snow','Veg','Water','LPC','MPC','HPC','Cirr','ClS')
        yScif = zeros(len(classes), dtype=float32)
        scif = itemfreq(scenec[scenecData])
        for i in range(len(scif)):
            yScif[scif[i,0]] = scif[i,1]
        yScif = yScif.astype(float32)/scif[:,1].sum() * 100.0
        xScif = arange(len(classes))                
        
        ax1.imshow(mosaic, cmap='jet', interpolation='nearest')
        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)
        ax2.imshow(scenec, cmap='jet', interpolation='nearest')
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)
        if len(xMoif) < 2:
            xticks = [1,2]
            xmax = 2
        else:
            xticks = xMoif
            xmax = xMoif.max()+1
        ax3.set_xlim([0, xmax])            
        ax3.set_xticks(xticks)
        ax3.bar(xMoif, yMoif, align='center', alpha=0.4)
        ax4.set_xlim([0, 12])
        ax4.set_color_cycle(['r','g','b','y'])
        ax4.bar(xScif, yScif, align='center', alpha=0.4)
        self._plot.show(block=False)
        return