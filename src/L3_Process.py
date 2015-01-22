#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from numpy import *
from tables import *
import sys
import os
import fnmatch
from time import time

from L3_Config import L3_Config
from L3_Tables import L3_Tables
from L3_XmlParser import L3_XmlParser
from L3_UnitTests import L3_UnitTests
from L3_STP import L3_STP
from L3_Library import stdoutWrite, stderrWrite, showImage
from lxml import etree, objectify

class L3_Process(object):
    def __init__(self, workdir):
        self._config = L3_Config(workdir)
        self._tables = False
        self._processed60 = False
        self._processed20 = False
        self._processed10 = False


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

    def initTarget(self, l3_targetProduct):
        self.tables = L3_Tables(self.config, l3_targetProduct)        
        self.tables.initDatabase()
        
        if self.tables.importBandList('L3') == False:
            stderrWrite('L2A User Products, generation times out of range\n.')
            config.exitError()                              
                
        return True

    def process(self, tile):
        self.tables = L3_Tables(self.config, tile)
        astr = 'L3_Process: processing with resolution ' + str(self.config.resolution) + ' m'
        self.config.timestamp(astr)
        self.config.timestamp('L3_Process: start of Pre Processing')
        if(self.preprocess() == False):
            return False
        
        if(args.tests == True):
            self.config.timestamp('L3_Process: perform a series of Unit Tests')
            self.config.logger.info('Performing unit tests with resolution %d m', self.config.resolution)
            tests = L3_UnitTests(self.config, self.tables)           
            if(tests.process() == False):
                return False
        else:
            self.config.timestamp('L3_Process: start of Spatio Temporal Processing')
            self.config.logger.info('Performing Spatio Temporal Processing with resolution %d m', self.config.resolution)
            stp = L3_STP(self.config, self.tables)
            if(stp.process() == False):
                return False
            
        self.config.timestamp('L3_Process: start of Post Processing')
        if(self.postprocess() == False):
            return False
        return True

    def preprocess(self):
        self.config.logger.info('Pre-processing with resolution %d m', self.config.resolution)
  
        # validate the meta data:
        xp = L3_XmlParser(self.config, 'UP2A')
        xp.validate()
        xp.export()
        xp = L3_XmlParser(self.config, 'T2A')
        xp.validate()
        xp.export()
        xp = L3_XmlParser(self.config, 'DS2A')
        xp.validate()
        xp.export()
        self.tables.initDatabase()
        return self.tables.importBandList('L3')

    def postprocess(self):
        self.config.logger.info('Post-processing with resolution %d m', self.config.resolution)
        res = self.tables.exportTable()
        if(self.config.resolution == 60):
            self.config.postprocess()
        return res

def main(args, config):
    
    if os.path.exists(args.directory) == False:
        stderrWrite('directory "%s" does not exist\n.' % args.directory)
        return False

    workDir = args.directory
    processor = L3_Process(workDir)
    l3_targetProductExists = False
    S2A_mask = 'S2A_*'
    tStart = time()
    for l2A_userProduct in workDir:
        # next statement creates L3 product Structure:
        if l3_targetProductExists == False:
            l3_targetProduct = config.createL3_TargetProduct(l2A_userProduct)
            if l3_targetProduct == False:
                stderrWrite('L2A User Products, generation times out of range\n.')
                config.exitError()

            l3_targetProductExists = processor.initTarget(l3_targetProduct)
            if l3_targetProductExists == False:
                stderrWrite('Error in creation of L3 target product\n.')
                config.exitError()
            # else l3_targetProductExists == True
        else:
            tiles = config.importL2A_UserProduct(l2A_userProduct)
            for tile in tiles:
                if(fnmatch.fnmatch(tile, S2A_mask) == False):
                    continue
                if args.resolution == None:
                    resolution = 60.0
                else:
                    resolution = args.resolution
                config.initSelf(resolution, tile)
                result = processor.process(tile)
                if(result == False):
                    stderrWrite('Application terminated with errors, see log file and traces.\n')
                    return False

                tMeasure = time() - tStart
                config.writeTimeEstimation(resolution, tMeasure)
    
    stdoutWrite('\nApplication terminated successfully.\n')
    return True


if __name__ == "__main__":
    # Someone is launching this directly
    import argparse
    config = L3_Config()
    descr = config.processorName +', '+ config.processorVersion +', created: '+ config.processorDate
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('directory', help='Directory where the Level-2A input files are located')
    parser.add_argument('--resolution', type=int, choices=[10, 20, 60], help='Target resolution, must be 10, 20 or 60 [m]')
    parser.add_argument('--profile', action='store_true', help='Performs a processor performance profile and displays the results')
    parser.add_argument('--tests', action='store_true', help='Performs a series of unit tests on all modules and displays the results')
    args = parser.parse_args()

    if(args.profile == True):
        import cProfile
        import pstats
        logdir = os.environ['S2L3APPHOME'] + '/log'
        profile = logdir + '/profile'
        cProfile.run('main(args, config)', profile)
        p = pstats.Stats(profile)
        p.strip_dirs().sort_stats('cumulative').print_stats(.25, 'L3_')
    else:
        main(args, config)
        
