#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
processorName = 'Sentinel-2 Level 3 Prototype Processor (SEN2THREE)'
processorVersion = '0.0.1'
processorDate = '2015.01.01'

#from numpy import *
from tables import *
import sys, os
import fnmatch
from time import time

from L3_Config import L3_Config
from L3_Tables import L3_Tables
from L3_Synthesis import L3_Synthesis
from L3_Library import stdoutWrite, stderrWrite


class L3_Process(object):
    def __init__(self, config):
        self._config = config

        self._l3Synthesis = L3_Synthesis(config)

    def get_tables(self):
        return self._tables


    def set_tables(self, value):
        self._tables = value


    def del_tables(self):
        del self._tables


    def get_config(self):
        return self._config


    def set_config(self, value):
        self._config = value


    def del_config(self):
        del self._config


    def __exit__(self):
            sys.exit(-1)

    config = property(get_config, set_config, del_config, "config's docstring")
    tables = property(get_tables, set_tables, del_tables, "tables's docstring")

    def process(self, tables):
        self._tables = tables
        astr = 'L3_Process: processing with resolution ' + str(self.config.resolution) + ' m'
        self.config.timestamp(astr)
        self.config.timestamp('L3_Process: start of Pre Processing')
        if(self.preprocess() == False):
            return False
        
        self.config.timestamp('L3_Process: start of Spatio Temporal Processing')
        self.config.logger.info('Performing Spatio Temporal Processing with resolution %d m', self.config.resolution)
        if(self._l3Synthesis.process(self._tables) == False):
            return False

        # append processed tile to list
        processedTile = self.config.product.L2A_TILE_ID + '\n'
        processedFn = self.config.workDir + '/' + 'processed'
        try:
            f = open(processedFn, 'a')
            f.write(processedTile)
            f.flush()
            f.close()
        except:
            stderrWrite('Could not update processed tile history.\n')
            self.config.exitError()
            return False
        return True

    def preprocess(self):
        self.config.logger.info('Pre-processing with resolution %d m', self.config.resolution)
        return

    def postprocess(self):
        self.config.timestamp('L3_Process: start of Post Processing')
        self.config.logger.info('Post-processing with resolution %d m', self.config.resolution)

        GRANULE = self.config.workDir + '/' + self.config.product.L3_TARGET_ID + '/GRANULE'
        tilelist = sorted(os.listdir(GRANULE))
        L3_TILE_MSK = 'S2A_*_TL_*'
        res = False
        for tile in tilelist:
            if fnmatch.fnmatch(tile, L3_TILE_MSK) == False:
                continue
            res = self.tables.exportTile(tile)
            if(self.config.resolution == 60):
                self.config.product.postprocess()
        if res == False:
            return res
        return self._l3Synthesis.postProcessing()

def main(args):
    
    if os.path.exists(args.directory) == False:
        stderrWrite('directory "%s" does not exist\n.' % args.directory)
        sys.exit(-1)

    workDir = args.directory
    if args.resolution == None:
        resolution = 60.0
    else:
        resolution = args.resolution

    config = L3_Config(resolution, workDir)
    config.init()
    processedTiles = ''
    result = False
    processedFn = workDir + '/' + 'processed'
    L2A_mask = 'S2?_*L2A_*'
    HelloWorld = processorName +', '+ processorVersion +', created: '+ processorDate
    stdoutWrite('\n%s started ...\n' % HelloWorld)    
    uplist = sorted(os.listdir(workDir))
    processor = L3_Process(config)
    for L2A_UP_ID in uplist:
        if(fnmatch.fnmatch(L2A_UP_ID, L2A_mask) == False):     
            continue
        if config.checkTimeRange(L2A_UP_ID) == False:
            continue
        config.updateUserProduct(L2A_UP_ID)
        GRANULE = workDir + '/' + L2A_UP_ID + '/GRANULE'
        tilelist = sorted(os.listdir(GRANULE))
        for tile in tilelist:
            # process only L2A tiles:
            if fnmatch.fnmatch(tile, L2A_mask) == False:
                continue
            # ignore already processed tiles:
            try:
                # read list of tiles already processed
                f = open(processedFn)
                processedTiles = f.read()
            except:
                pass
            if tile[:-7] in processedTiles:
                continue
            tStart = time()
            nrTilesProcessed = len(processedTiles.split())
            config.updateTile(tile, nrTilesProcessed)
            tables = L3_Tables(config)
            tables.init()
            # no processing if first initialisation:
            if tables.testBand('L2A', 1) == False:
                # append processed tile to list
                processedTile = tile + '\n'
                processedFn = config.workDir + '/' + 'processed'
                try:
                    f = open(processedFn, 'a')
                    f.write(processedTile)
                    f.flush()
                    f.close()
                except:
                    stderrWrite('Could not update processed tile history.\n')
                    config.exitError()
                    return False
                continue
            result = processor.process(tables)
            if(result == False):
                stderrWrite('Application terminated with errors, see log file and traces.\n')
                return False

            tMeasure = time() - tStart
            config.writeTimeEstimation(resolution, tMeasure)

    if result == True:
        result = processor.postprocess()
        if(result == False):
            stderrWrite('Application terminated with errors, see log file and traces.\n')
            return False
                
    stdoutWrite('\nApplication terminated successfully.\n')
    return result

if __name__ == "__main__":
    # Someone is launching this directly
    import argparse
    descr = processorName +', '+ processorVersion +', created: '+ processorDate
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('directory', help='Directory where the Level-2A input files are located')
    parser.add_argument('--clean', action='store_true', help='Cleans the history of processed files and starts from scratch')
    parser.add_argument('--profile', action='store_true', help='Performs a processor performance profile and displays the results')
    parser.add_argument('--resolution', type=int, choices=[10, 20, 60], help='Target resolution, must be 10, 20 or 60 [m]')
    parser.add_argument('--tests', action='store_true', help='Performs a series of unit tests on all modules and displays the results')
    
    args = parser.parse_args()

    if(args.profile == True):
        import cProfile
        import pstats
        logdir = os.environ['S2L3APPHOME'] + '/log'
        profile = logdir + '/profile'
        cProfile.run('main(args)', profile)
        p = pstats.Stats(profile)
        p.strip_dirs().sort_stats('cumulative').print_stats(.25, 'L3_')
    else:
        main(args)
        
