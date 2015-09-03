#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys, os

from L2A_SceneClass import L2A_SceneClass
from L3_XmlParser import L3_XmlParser

class L2A_Process(object):
    def __init__(self, config):
        self._config = config
        self._tables = False


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

    def preprocess(self):
        self.config.logger.info('Pre-processing with resolution %d m', self.config.resolution)
        self.config.tTotal = 0
        # validate the meta data:
        xp = L3_XmlParser(self.config, 'UP1C')
        xp.export()
        xp.validate()
        xp = L3_XmlParser(self.config, 'T1C')
        xp.export()
        xp.validate()
        xp = L3_XmlParser(self.config, 'DS1C')
        xp.export()
        xp.validate()

        if(self.tables.importBandList() == False):
            return False   
        return True

    def process(self, tables):
        self.tables = tables
        astr = 'L2A_Process: processing with resolution ' + str(self.config.resolution) + ' m'
        self.config.timestamp(astr)
        self.config.timestamp('L2A_Process: start of pre processing')
        self.config.readTileMetadata('T2A')
        if(self.preprocess() == False):
            return False

        if(self.config.resolution > 10):
            self.config.timestamp('L2A_Process: start of Scene Classification')
            sc = L2A_SceneClass(self.config, tables)
            self.config.logger.info('Performing Scene Classification with resolution %d m', self.config.resolution)
            if(sc.process() == False):
                return False

        self.config.timestamp('L2A_Process: start of post processing')
        if(self.postprocess() == False):
            return False

        return True

    def postprocess(self):
        self.config.logger.info('Post-processing with resolution %d m', self.config.resolution)
        res = self.tables.exportBandList()
        #if(self.config.resolution == 60):
        self.config.postprocess()

        # validate the meta data:
        xp = L3_XmlParser(self.config, 'UP2A')
        xp.validate()
        xp = L3_XmlParser(self.config, 'T2A')
        xp.validate()
        xp = L3_XmlParser(self.config, 'DS2A')
        xp.validate()
        return res
