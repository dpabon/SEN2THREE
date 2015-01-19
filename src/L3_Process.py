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

    def selectAndProcess(self, tile):
        if(self.config.resolution == 10):
            self.config.logger.info('selected resolution is 10m')
            if(self._processed20 == False):
                self.config.resolution = 20
                stdoutWrite('20m resolution must be processed first ...\n')
                self.config.tracer.info('20m resolution must be processed first')
                self.config.logger.info('20m resolution must be processed first')
                self.selectAndProcess(tile)

            self.config.resolution = 10
            self.config.readPreferences()
            self.tables = L3_Tables(self.config, tile)
            self._processed10 = self.process()
            if(self._processed10 == False):
                return False

        elif(self.config.resolution == 20):
            self.config.logger.info('selected resolution is 20m')
            if(self._processed60 == False):
                self.config.resolution = 60
                stdoutWrite('60m resolution must be processed first ...\n')
                self.config.tracer.info('60m resolution must be processed first')
                self.config.logger.info('60m resolution must be processed first')
                self.selectAndProcess(tile)

            self.config.resolution = 20
            self.config.readPreferences()
            self.tables = L3_Tables(self.config, tile)
            self._processed20 = self.process()
            if(self._processed20 == False):
                return False

        elif(self.config.resolution == 60):
            self.config.logger.info('selected resolution is 60m')
            self.config.readPreferences()
            self.tables = L3_Tables(self.config, tile)
            #self.config.readTileMetadata()
            self._processed60 = self.process()
            if(self._processed60 == False):
                return False
        else:
            self.config.logger.debug('wrong resolution for processing configured: ', str(self.config.resolution))
            return False

    def process(self):
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
        
        return self.tables.importTable()

    def postprocess(self):
        self.config.logger.info('Post-processing with resolution %d m', self.config.resolution)
        res = self.tables.exportTable()
        if(self.config.resolution == 60):
            self.config.postprocess()
        return res


    def resetProcessingStatus(self):
        self._processed60 = False
        self._processed20 = False
        self._processed10 = False
        return

def main(args, config):
    
    if os.path.exists(args.directory) == False:
        stderrWrite('directory "%s" does not exist\n.' % args.directory)
        return False

    processor = L3_Process(args.directory)
    HelloWorld = config.processorName +', '+ config.processorVersion +', created: '+ config.processorDate
    stdoutWrite('\n%s started ...\n' % HelloWorld)
    tStart = time()
    S2A_mask = 'S2A_*'

    # next statement creates L3 product Structure:
    tiles = config.createL3_UserProduct()
    for tile in tiles:
        if(fnmatch.fnmatch(tile, S2A_mask) == False):
            continue

        processor.resetProcessingStatus()
        config.initLogger()
        config.logger.info(HelloWorld)
        config.calcEarthSunDistance2(tile)
        if args.resolution == None:
            resolution = 60.0
        else:
            resolution = args.resolution

        config.resolution = resolution
        config.setTimeEstimation(resolution)
        config.logger.debug('Module L3_Process initialized')

        result = processor.selectAndProcess(tile)
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
        
