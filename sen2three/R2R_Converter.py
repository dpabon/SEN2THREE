#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
processorName = 'Sentinel-2 Reflectance to Radiance Converter'
processorVersion = '0.9.0'
processorDate = '2015.06.15'
productVersion = '12'

from numpy import *
import sys, os
import fnmatch
from time import time
import glob
import glymur

from L3_Config import L3_Config
from L2A_Tables import L2A_Tables
from L3_Tables import L3_Tables
from L3_Product import L3_Product
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from L3_Library import rectBivariateSpline, stdoutWrite, stderrWrite, showImage
from L3_XmlParser import L3_XmlParser

class R2R_Converter(object):
    def __init__(self, config):
        self._config = config
        self._bandIndex = None

    def get_config(self):
        return self._config

    def set_config(self, value):
        self._config = value

    def del_config(self):
        del self._config

    def __exit__(self):
            sys.exit(-1)

    config = property(get_config, set_config, del_config, "config's docstring")
    
    def convert(self, targetDir):
        #basename = os.path.basename(targetDir)
        L1C_mask = 'S2?_*L1C_*'
        L2A_mask = 'S2?_*L2A_*'
        XML_mask = 'S2?_*.xml'
        kwargs = {"tilesize": (2048, 2048), "prog": "RPCL"}
        tiledir = targetDir + '/GRANULE' 
        os.chdir(tiledir)
        tiles = sorted(os.listdir(tiledir))
        nrTiles = len(tiles)
        for tilename in tiles:
            # needed for self.config.d2:
            if(('S2' in tilename) == False):
                nrTiles -=1
                continue
            stdoutWrite('%d tile(s) to be converted ...\n' % nrTiles)
            self.config.logger.info('Converting reflectance to radiance')
            stdoutWrite('Converting reflectance to radiance ...\n')
            self.config.calcEarthSunDistance2(tilename)
            # get metadata filename:
            globlist = tiledir + '/' + tilename + '/' + XML_mask
            for fn in glob.glob(globlist):
                filename = fn
            if(fnmatch.fnmatch(tilename, L1C_mask) == True):
                globlist = tiledir + '/' + tilename + '/IMG_DATA/S2*_B??.jp2'
            elif(fnmatch.fnmatch(tilename, L2A_mask) == True):
                globlist = tiledir + '/' + tilename + '/IMG_DATA/R??m/S2*_B??_*.jp2'
            nrBands = len(glob.glob(globlist))
            stdoutWrite('%d bands to be converted ...\n' % nrBands)
            for band in glob.glob(globlist):
                nrBands -= 1
                basename = os.path.basename(band)
                indataset = glymur.Jp2k(band)
                indataArr = indataset[:]
                self.setResolution(basename)
                self.setBandIndex(basename)
                self.getTileMetadata(filename)
                outdataArr = self.refl2rad(indataArr)
                print '========================='
                print indataArr.min()
                print indataArr.mean()
                print indataArr.max()
                print '-------------------------'
                print outdataArr.min()
                print outdataArr.mean()
                print outdataArr.max()
                print '========================='
                glymur.Jp2k(band, outdataArr, **kwargs)            
                self.config.logger.info('Band ' + basename + ' converted')
                stdoutWrite('%d bands remain\n' % nrBands)
        return

    def setResolution(self, bandname):
        res60 = ['B01', 'B09', 'B10']
        res10 = ['B02', 'B03', 'B04', 'B08']
        if any([band in bandname for band in res60]): 
            self.config.resolution = 60
        elif any([band in bandname for band in res10]): 
            self.config.resolution = 10
        else:                   
            self.config.resolution = 20
        return

    def setBandIndex(self, bandname):
        if 'B01' in bandname:
            self._bandIndex = 0
        elif 'B02' in bandname:
            self._bandIndex = 1 
        elif 'B03' in bandname:
            self._bandIndex = 2
        elif 'B04' in bandname:
            self._bandIndex = 3
        elif 'B05' in bandname:
            self._bandIndex = 4
        elif 'B06' in bandname:
            self._bandIndex = 5
        elif 'B07' in bandname:
            self._bandIndex = 6
        elif 'B08' in bandname:
            self._bandIndex = 7
        elif 'B8A' in bandname:
            self._bandIndex = 8
        elif 'B09' in bandname:
            self._bandIndex = 9       
        elif 'B10' in bandname:
            self._bandIndex = 10   
        elif 'B11' in bandname:
            self._bandIndex = 11   
        elif 'B12' in bandname:
            self._bandIndex = 12          
        return

    def getTileMetadata(self, metafile):
        XML_L1C_mask = '*S2?_*L1C_*.xml'
        XML_L2A_mask = '*S2?_*L2A_*.xml'
        if(fnmatch.fnmatch(metafile, XML_L1C_mask) == True):
            self.config.product.L1C_TILE_MTD_XML = metafile
            self.config.readTileMetadata('T1C')
        elif(fnmatch.fnmatch(metafile, XML_L2A_mask) == True):
            self.config.product.L2A_TILE_MTD_XML = metafile            
            self.config.readTileMetadata('T2A')
        return
    
    def refl2rad(self, indataArr):
        # this converts TOA reflectance to radiance:
        nrows = self.config.nrows
        ncols = self.config.ncols
        DN = indataArr.astype(float32)

        c0 = self.config.c0[self._bandIndex]
        c1 = self.config.c1[self._bandIndex]
        e0 = self.config.e0[self._bandIndex]
        dnScale = float32(self.config.dnScale)

        rtoa = float32(c0 + DN / dnScale)
        d2 = self.config.d2
        x = arange(nrows, dtype=float32) / (nrows-1) * self.config.solze_arr.shape[0]
        y = arange(ncols, dtype=float32) / (ncols-1) * self.config.solze_arr.shape[1]
        szi = rectBivariateSpline(x,y,self.config.solze_arr)
        rad_szi = radians(szi)
        sza = cos(rad_szi)
        L = float32(rtoa * e0 * sza / (pi * d2) / c1)
        return (L/c1).astype(uint16)

def main(args=None):
    import argparse
    descr = processorName +', '+ processorVersion +', created: '+ processorDate + \
        ', supporting Level-1C product version: ' + productVersion + '.'
     
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('directory', help='Directory where the reflectance input files are located')
    args = parser.parse_args()

    # SIITBX-49: directory should not end with '/':
    directory = args.directory
    if directory[-1] == '/':
        directory = directory[:-1]

    # check if directory argument starts with a relative path. If not, expand: 
    if(os.path.isabs(directory)) == False:
        cwd = os.getcwd()
        directory = os.path.join(cwd, directory)
    elif os.path.exists(args.directory) == False:
        stderrWrite('directory "%s" does not exist\n.' % args.directory)
        return False

    config = L3_Config('60', directory)
    config.init(processorVersion)
    result = False

    HelloWorld = processorName +', '+ processorVersion +', created: '+ processorDate
    stdoutWrite('\n%s started ...\n' % HelloWorld)    
    processor = R2R_Converter(config)
    upList = sorted(os.listdir(directory))
    L1C_mask = 'S2?_*L1C_*'
    L2A_mask = 'S2?_*L2A_*'
    exclusionMask = 'S2?_*_RAD'
    nrUserProducts = len(upList)
    for upId in upList:
        if(('S2' in upId) == False):
            nrUserProducts -=1
            continue
        # avoid reprocessing of converted data:
        if(fnmatch.fnmatch(upId, exclusionMask) == True):
            continue
        if((fnmatch.fnmatch(upId, L1C_mask) == False) and \
           (fnmatch.fnmatch(upId, L2A_mask) == False)):     
            continue
        stdoutWrite('%d user product(s) to be converted ...\n' % nrUserProducts)    
        nrUserProducts -=1
        upFullPath = os.path.join(directory, upId) 
        targetDir = config.targetDirectory
        if targetDir == 'DEFAULT':   
            targetDir = directory + '_RAD'
        else:
            targetDir = os.path.join(targetDir, upId)
        copy_tree(upFullPath, targetDir)
        result = processor.convert(targetDir)
        config.logger.info('User product ' + upId + ' converted')
        stdoutWrite('%d user product(s) remain\n\n' % nrUserProducts)
        if(result == False):
            stderrWrite('Application terminated with errors, see log file and traces.\n')
            return False
                
    stdoutWrite('\nApplication terminated successfully.\n')
    return result

if __name__ == "__main__":
    sys.exit(main() or 0)
