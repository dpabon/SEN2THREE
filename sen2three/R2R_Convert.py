#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
processorName = 'Sentinel-2 Reflectance to Radiance Converter'
processorVersion = '1.0.0'
processorDate = '2015.09.15'
productVersion = '13'

from numpy import *
import sys, os
import fnmatch
from time import time
import glob
import glymur

from L3_Config import L3_Config
from distutils.dir_util import copy_tree
from L3_Library import rectBivariateSpline, stdoutWrite, stderrWrite
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
                stdoutWrite('Import image %s ...\n' % basename)
                indataset = glymur.Jp2k(band)
                indataArr = indataset[:]
                
                self.config.logger.info('Image: %s', basename)
                self.config.logger.debug('Reflectance values:')
                self.config.logger.debug('Min: %s',  str(indataArr.min()))
                self.config.logger.debug('Mean: %s', str(indataArr.mean()))
                self.config.logger.debug('Max: %s',  str(indataArr.max()))
                self.setResolution(basename)
                self.setBandIndex(basename)
                self.getTileMetadata(filename)
                outdataArr = self.refl2rad(indataArr)
                
                stdoutWrite('converted.\n')
                self.config.logger.debug('Radiance values - upscaled with 100:')
                self.config.logger.debug('Min: %s',  str(outdataArr.min()))
                self.config.logger.debug('Mean: %s', str(outdataArr.mean()))
                self.config.logger.debug('Max: %s',  str(outdataArr.max()))

                stdoutWrite('Export image ...\n')
                glymur.Jp2k(band, outdataArr, **kwargs)            

                self.config.logger.info('Band ' + basename + ' converted')
                stdoutWrite('%d bands remain.\n' % nrBands)
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
    
    def setUpMetadataId(self, L1C_UP_DIR):
        S2A_mask = 'S2A_*_MTD_*1C_*.xml'
        filelist = sorted(os.listdir(L1C_UP_DIR))
        found = False
        for filename in filelist:
            if(fnmatch.fnmatch(filename, S2A_mask) == True):
                found = True
                break
        if found == False:
            stderrWrite('No metadata for user product.\n')
            self.config.exitError()   
        self.config.product.L1C_UP_MTD_XML = os.path.join(L1C_UP_DIR, filename)
        return
    
    def refl2rad(self, indataArr):
        ''' Converts the reflectance to radiance.

            :param indataArray: the digital numbers representing TOA reflectance.
            :type indataArray: a 2 dimensional numpy array (row x column) of type unsigned int 16.
            :return: the pixel data converted to radiance.
            :rtype: a 2 dimensional numpy array (row x column) of type unsigned int 16, representing radiance.
            
            Additional inputs from L1 user Product_Image_Characteristics metadata:
            * QUANTIFICATION_VALUE: the scaling factor for converting DN to reflectance.
            * U: the earth sun distance correction factor.
            * SOLAR_IRRADIANCE: the mean solar exoatmospheric irradiances for each band.

            Additional inputs from L1 tile Geometric_Info metadata:
            * Sun_Angles_Grid.Zenith.Values: the interpolated zenith angles grid.

        '''
        # This converts TOA reflectance to radiance:
        nrows = self.config.nrows
        ncols = self.config.ncols
        # The digital number (DN) as float:         
        DN = indataArr.astype(float32)
        xp = L3_XmlParser(self.config, 'UP1C')
        pic = xp.getTree('General_Info', 'Product_Image_Characteristics')
        qv = pic.QUANTIFICATION_VALUE
        c0 = 0

        # The quantification value for the DN from metadata:      
        c1 =  float32(qv.text)

        # TOA reflectance:        
        rtoa = float32(c0 + DN / c1)

        rc = pic.Reflectance_Conversion

        # The earth sun distance correction factor,
        # apparently already squared:
        u2 =  float32(rc.U.text)

        # The solar irradiance:        
        si = rc.Solar_Irradiance_List.SOLAR_IRRADIANCE
        e0 = float32(si[self._bandIndex].text)

        # The solar zenith array:
        x = arange(nrows, dtype=float32) / (nrows-1) * self.config.solze_arr.shape[0]
        y = arange(ncols, dtype=float32) / (ncols-1) * self.config.solze_arr.shape[1]
        szi = rectBivariateSpline(x,y,self.config.solze_arr)
        rad_szi = radians(szi)
        sza = float32(cos(rad_szi))
        rtoa_e0_sza = float32(rtoa * sza * e0)
        pi_u2 = float32(pi * u2 )
        
        # Finally, calculate the radiance and return array as unsigned int, this is multiplied by 100,
        # to keep resolution - glymur only allows integer integer values for storage.        
         
        L = (rtoa_e0_sza / pi_u2 ) * 100.0
        return (L + 0.5).astype(uint16)

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

    config = L3_Config('60', directory, 'R2R_GIPP')
    config.init(processorVersion)
    result = False

    HelloWorld = processorName +', '+ processorVersion +', created: '+ processorDate
    stdoutWrite('\n%s started ...\n' % HelloWorld)    
    processor = R2R_Converter(config)
    L1C_mask = 'S2?_*L1C_*'
    exclusionMask = 'S2?_*_RAD'
    upList = sorted(os.listdir(directory))
    l1cList = []    
    nrUserProducts = 0
    
    for upId in upList:
        if(fnmatch.fnmatch(upId, exclusionMask) == True):
            continue
        elif(fnmatch.fnmatch(upId, L1C_mask) == True):
            nrUserProducts += 1
            l1cList.append(upId)

    for upId in l1cList:                 
        stdoutWrite('%d user product(s) to be converted ...\n' % nrUserProducts)
        nrUserProducts -=1
        upFullPath = os.path.join(directory, upId) 
        targetDir = config.targetDir
        if targetDir == 'DEFAULT':   
            targetDir = directory + '_RAD'
        else:
            targetDir = os.path.join(targetDir, upId)
        copy_tree(upFullPath, targetDir)
        processor.setUpMetadataId(targetDir)
        result = processor.convert(targetDir)
        if(result == False):
            stderrWrite('Application terminated with errors, see log file and traces.\n')
            return False
        else:
            config.logger.info('User product ' + upId + ' converted')
            stdoutWrite('%d user product(s) remain\n\n' % nrUserProducts)
                
    stdoutWrite('Application terminated successfully.\n')
    return result

if __name__ == "__main__":
    sys.exit(main() or 0)
