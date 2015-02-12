#!/usr/bin/env pythonimport osimport sysfrom numpy import *from time import timefrom L3_Borg import Borgfrom L3_Config import L3_Configfrom L3_Library import *from L3_Tables import L3_Tablesfrom PIL import *set_printoptions(precision = 7, suppress = True)class L3_UnitTests(Borg):    def __init__(self, config, tables):        self._config = config        self._tables = tables        self.config.logger.debug('Module L3_UnitTests initialized')        self._processingStatus = True    def __exit__(self):        sys.exit(-1)    def __del__(self):        self.config.logger.info('Module L3_UnitTests deleted')    def assignClassifcation(self, arr, treshold, classification):        cm = self.classificationMask        cm[(arr == treshold) & (cm == self._notClassified)] = classification        self.confidenceMaskCloud[(cm == classification)] = 0        return    def get_config(self):        return self._config    def get_tables(self):        return self._tables    def set_config(self, value):        self._config = value    def set_tables(self, value):        self._tables = value    def del_config(self):        del self._config    def del_tables(self):        del self._tables    config = property(get_config, set_config, del_config, "config's docstring")    tables = property(get_tables, set_tables, del_tables, "tables's docstring")    def process(self):        ts = time.time()        self.config.timestamp('test tables module')        context = ['L2A', 'L3']        tables = self.tables        bands = self.tables.bandIndex        print 'testBand():'         for c in context:            for i in bands:                result = tables.testBand(c,i)                print 'Context:', c, 'Band:', tables.getBandNameFromIndex(i), 'Result:', result        print        print 'getBandSize()'        print 'set L2A bands, if L3 was set:'         for i in bands:            result = tables.testBand('L3', i)            if result == True:                tables.setBand('L2A', i, tables.getBand('L3', i))                result = tables.testBand('L2A', i)                print 'Context: L2A', 'Band:', tables.getBandNameFromIndex(i), 'Result:', result                dataType = tables.getDataType('L2A', i)                print 'Context: L2A', 'Band:', tables.getBandNameFromIndex(i), 'Data Type:', dataType                bandSize = tables.getBandSize('L2A', i)                print 'Context: L2A', 'Band:', tables.getBandNameFromIndex(i), 'Band Size:', bandSize                        tDelta = time.time() - ts        self.config.logger.info('Procedure L3_UnitTests overall time [s]: %0.3f' % tDelta)        if(self.config.loglevel == 'DEBUG'):            print 'Procedure L3_UnitTests, overall time[s]: %0.3f' % tDelta        return True