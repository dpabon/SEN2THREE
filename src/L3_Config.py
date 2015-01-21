#!/usr/bin/env python

from numpy import *
import fnmatch
import sys, os
import logging
import ConfigParser
from L3_XmlParser import L3_XmlParser
from L3_Library import stdoutWrite, stderrWrite
from lxml import etree, objectify
from time import strftime
from datetime import datetime, date
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from L3_Borg import Borg


class L3_Config(Borg):

    def get_shared(self):
        return self._shared


    def get_processor_name(self):
        return self._processorName


    def get_processor_version(self):
        return self._processorVersion


    def get_processor_date(self):
        return self._processorDate


    def get_home(self):
        return self._home


    def get_work_dir(self):
        return self._workDir


    def get_config_dir(self):
        return self._configDir


    def get_bin_dir(self):
        return self._binDir


    def get_lib_dir(self):
        return self._libDir


    def get_log_dir(self):
        return self._logDir


    def get_config_fn(self):
        return self._configFn


    def get_processing_status_fn(self):
        return self._processingStatusFn


    def get_processing_estimation_fn(self):
        return self._processingEstimationFn


    def get_ncols(self):
        return self._ncols


    def get_nrows(self):
        return self._nrows


    def get_nbnds(self):
        return self._nbnds


    def get_t_total(self):
        return self._tTotal


    def get_zenith_angle(self):
        return self._zenith_angle


    def get_azimuth_angle(self):
        return self._azimuth_angle


    def get_gipp(self):
        return self._GIPP


    def get_ecmwf(self):
        return self._ECMWF


    def get_dem(self):
        return self._DEM


    def get_l_2_a_boa_quantification_value(self):
        return self._L2A_BOA_QUANTIFICATION_VALUE


    def get_l_2_a_wvp_quantification_value(self):
        return self._L2A_WVP_QUANTIFICATION_VALUE


    def get_l_2_a_aot_quantification_value(self):
        return self._L2A_AOT_QUANTIFICATION_VALUE


    def get_dn_scale(self):
        return self._dnScale


    def get_timestamp(self):
        return self._timestamp


    def get_l_2_a_inspire_xml(self):
        return self._L2A_INSPIRE_XML


    def get_l_2_a_manifest_safe(self):
        return self._L2A_MANIFEST_SAFE


    def get_l_1_c_up_mtd_xml(self):
        return self._L1C_UP_MTD_XML


    def get_l_1_c_ds_mtd_xml(self):
        return self._L1C_DS_MTD_XML


    def get_l_1_c_tile_mtd_xml(self):
        return self._L1C_TILE_MTD_XML


    def get_l_1_c_up_id(self):
        return self._L1C_UP_ID


    def get_l_1_c_ds_id(self):
        return self._L1C_DS_ID


    def get_l_1_c_tile_id(self):
        return self._L1C_TILE_ID


    def get_l_2_a_up_mtd_xml(self):
        return self._L2A_UP_MTD_XML


    def get_l_2_a_ds_mtd_xml(self):
        return self._L2A_DS_MTD_XML


    def get_l_2_a_tile_mtd_xml(self):
        return self._L2A_TILE_MTD_XML


    def get_l_3_up_id(self):
        return self._L3_UP_ID


    def get_l_3_ds_id(self):
        return self._L3_DS_ID


    def get_l_3_tile_id(self):
        return self._L3_TILE_ID


    def get_l_3_tile_mtd_xml(self):
        return self._L3_TILE_MTD_XML


    def get_creation_date(self):
        return self._creationDate


    def get_acquisition_date(self):
        return self._acquisitionDate


    def get_l_3_up_dir(self):
        return self._L3_UP_DIR


    def set_shared(self, value):
        self._shared = value


    def set_processor_name(self, value):
        self._processorName = value


    def set_processor_version(self, value):
        self._processorVersion = value


    def set_processor_date(self, value):
        self._processorDate = value


    def set_home(self, value):
        self._home = value


    def set_work_dir(self, value):
        self._workDir = value


    def set_config_dir(self, value):
        self._configDir = self.home + value + '/'       


    def set_bin_dir(self, value):
        self._binDir = self.home + value + '/'


    def set_lib_dir(self, value):
        self._libDir = self.home + value + '/'


    def set_log_dir(self, value):
        self._logDir = self.home + value + '/'


    def set_config_fn(self, value):
        self._configFn = self._configDir + value + '.xml'


    def set_processing_status_fn(self, value):
        self._processingStatusFn = value


    def set_processing_estimation_fn(self, value):
        self._processingEstimationFn = value


    def set_ncols(self, value):
        self._ncols = value


    def set_nrows(self, value):
        self._nrows = value


    def set_nbnds(self, value):
        self._nbnds = value


    def set_t_total(self, value):
        self._tTotal = value


    def set_zenith_angle(self, value):
        self._zenith_angle = value


    def set_azimuth_angle(self, value):
        self._azimuth_angle = value


    def set_gipp(self, value):
        self._GIPP = value


    def set_ecmwf(self, value):
        self._ECMWF = value


    def set_dem(self, value):
        self._DEM = value


    def set_l_2_a_boa_quantification_value(self, value):
        self._L2A_BOA_QUANTIFICATION_VALUE = value


    def set_l_2_a_wvp_quantification_value(self, value):
        self._L2A_WVP_QUANTIFICATION_VALUE = value


    def set_l_2_a_aot_quantification_value(self, value):
        self._L2A_AOT_QUANTIFICATION_VALUE = value


    def set_dn_scale(self, value):
        self._dnScale = value


    def set_timestamp(self, value):
        self._timestamp = value


    def set_l_2_a_inspire_xml(self, value):
        self._L2A_INSPIRE_XML = value


    def set_l_2_a_manifest_safe(self, value):
        self._L2A_MANIFEST_SAFE = value


    def set_l_1_c_up_mtd_xml(self, value):
        self._L1C_UP_MTD_XML = value


    def set_l_1_c_ds_mtd_xml(self, value):
        self._L1C_DS_MTD_XML = value


    def set_l_1_c_tile_mtd_xml(self, value):
        self._L1C_TILE_MTD_XML = value


    def set_l_1_c_up_id(self, value):
        self._L1C_UP_ID = value


    def set_l_1_c_ds_id(self, value):
        self._L1C_DS_ID = value


    def set_l_1_c_tile_id(self, value):
        self._L1C_TILE_ID = value


    def set_l_2_a_up_mtd_xml(self, value):
        self._L2A_UP_MTD_XML = value


    def set_l_2_a_ds_mtd_xml(self, value):
        self._L2A_DS_MTD_XML = value


    def set_l_2_a_tile_mtd_xml(self, value):
        self._L2A_TILE_MTD_XML = value


    def set_l_3_up_id(self, value):
        self._L3_UP_ID = value


    def set_l_3_ds_id(self, value):
        self._L3_DS_ID = value


    def set_l_3_tile_id(self, value):
        self._L3_TILE_ID = value


    def set_l_3_tile_mtd_xml(self, value):
        self._L3_TILE_MTD_XML = value


    def set_creation_date(self, value):
        self._creationDate = value


    def set_acquisition_date(self, value):
        self._acquisitionDate = value


    def set_l_3_up_dir(self, value):
        self._L3_UP_DIR = value


    def del_shared(self):
        del self._shared


    def del_processor_name(self):
        del self._processorName


    def del_processor_version(self):
        del self._processorVersion


    def del_processor_date(self):
        del self._processorDate


    def del_home(self):
        del self._home


    def del_work_dir(self):
        del self._workDir


    def del_config_dir(self):
        del self._configDir


    def del_bin_dir(self):
        del self._binDir


    def del_lib_dir(self):
        del self._libDir


    def del_log_dir(self):
        del self._logDir


    def del_config_fn(self):
        del self._configFn


    def del_processing_status_fn(self):
        del self._processingStatusFn


    def del_processing_estimation_fn(self):
        del self._processingEstimationFn


    def del_ncols(self):
        del self._ncols


    def del_nrows(self):
        del self._nrows


    def del_nbnds(self):
        del self._nbnds


    def del_t_total(self):
        del self._tTotal


    def del_zenith_angle(self):
        del self._zenith_angle


    def del_azimuth_angle(self):
        del self._azimuth_angle


    def del_gipp(self):
        del self._GIPP


    def del_ecmwf(self):
        del self._ECMWF


    def del_dem(self):
        del self._DEM


    def del_l_2_a_boa_quantification_value(self):
        del self._L2A_BOA_QUANTIFICATION_VALUE


    def del_l_2_a_wvp_quantification_value(self):
        del self._L2A_WVP_QUANTIFICATION_VALUE


    def del_l_2_a_aot_quantification_value(self):
        del self._L2A_AOT_QUANTIFICATION_VALUE


    def del_dn_scale(self):
        del self._dnScale


    def del_timestamp(self):
        del self._timestamp


    def del_l_2_a_inspire_xml(self):
        del self._L2A_INSPIRE_XML


    def del_l_2_a_manifest_safe(self):
        del self._L2A_MANIFEST_SAFE


    def del_l_1_c_up_mtd_xml(self):
        del self._L1C_UP_MTD_XML


    def del_l_1_c_ds_mtd_xml(self):
        del self._L1C_DS_MTD_XML


    def del_l_1_c_tile_mtd_xml(self):
        del self._L1C_TILE_MTD_XML


    def del_l_1_c_up_id(self):
        del self._L1C_UP_ID


    def del_l_1_c_ds_id(self):
        del self._L1C_DS_ID


    def del_l_1_c_tile_id(self):
        del self._L1C_TILE_ID


    def del_l_2_a_up_mtd_xml(self):
        del self._L2A_UP_MTD_XML


    def del_l_2_a_ds_mtd_xml(self):
        del self._L2A_DS_MTD_XML


    def del_l_2_a_tile_mtd_xml(self):
        del self._L2A_TILE_MTD_XML


    def del_l_3_up_id(self):
        del self._L3_UP_ID


    def del_l_3_ds_id(self):
        del self._L3_DS_ID


    def del_l_3_tile_id(self):
        del self._L3_TILE_ID


    def del_l_3_tile_mtd_xml(self):
        del self._L3_TILE_MTD_XML


    def del_creation_date(self):
        del self._creationDate


    def del_acquisition_date(self):
        del self._acquisitionDate


    def del_l_3_up_dir(self):
        del self._L3_UP_DIR
        
        
    def get_logger(self):
        return self._logger


    def set_logger(self, value):
        self._logger = value


    def del_logger(self):
        del self._logger

    
    def get_resolution(self):
        return self._resolution


    def set_resolution(self, value):
        self._resolution = value


    def del_resolution(self):
        del self._resolution


    resolution = property(get_resolution, set_resolution, del_resolution, "resolution's docstring")
    shared = property(get_shared, set_shared, del_shared, "shared's docstring")
    logger = property(get_logger, set_logger, del_logger, "logger's docstring")
    processorName = property(get_processor_name, set_processor_name, del_processor_name, "processorName's docstring")
    processorVersion = property(get_processor_version, set_processor_version, del_processor_version, "processorVersion's docstring")
    processorDate = property(get_processor_date, set_processor_date, del_processor_date, "processorDate's docstring")
    home = property(get_home, set_home, del_home, "home's docstring")
    workDir = property(get_work_dir, set_work_dir, del_work_dir, "workDir's docstring")
    configDir = property(get_config_dir, set_config_dir, del_config_dir, "configDir's docstring")
    binDir = property(get_bin_dir, set_bin_dir, del_bin_dir, "binDir's docstring")
    libDir = property(get_lib_dir, set_lib_dir, del_lib_dir, "libDir's docstring")
    logDir = property(get_log_dir, set_log_dir, del_log_dir, "logDir's docstring")
    configFn = property(get_config_fn, set_config_fn, del_config_fn, "configFn's docstring")
    processingStatusFn = property(get_processing_status_fn, set_processing_status_fn, del_processing_status_fn, "processingStatusFn's docstring")
    processingEstimationFn = property(get_processing_estimation_fn, set_processing_estimation_fn, del_processing_estimation_fn, "processingEstimationFn's docstring")
    ncols = property(get_ncols, set_ncols, del_ncols, "ncols's docstring")
    nrows = property(get_nrows, set_nrows, del_nrows, "nrows's docstring")
    nbnds = property(get_nbnds, set_nbnds, del_nbnds, "nbnds's docstring")
    tTotal = property(get_t_total, set_t_total, del_t_total, "tTotal's docstring")
    zenith_angle = property(get_zenith_angle, set_zenith_angle, del_zenith_angle, "zenith_angle's docstring")
    azimuth_angle = property(get_azimuth_angle, set_azimuth_angle, del_azimuth_angle, "azimuth_angle's docstring")
    GIPP = property(get_gipp, set_gipp, del_gipp, "GIPP's docstring")
    ECMWF = property(get_ecmwf, set_ecmwf, del_ecmwf, "ECMWF's docstring")
    DEM = property(get_dem, set_dem, del_dem, "DEM's docstring")
    L2A_BOA_QUANTIFICATION_VALUE = property(get_l_2_a_boa_quantification_value, set_l_2_a_boa_quantification_value, del_l_2_a_boa_quantification_value, "L2A_BOA_QUANTIFICATION_VALUE's docstring")
    L2A_WVP_QUANTIFICATION_VALUE = property(get_l_2_a_wvp_quantification_value, set_l_2_a_wvp_quantification_value, del_l_2_a_wvp_quantification_value, "L2A_WVP_QUANTIFICATION_VALUE's docstring")
    L2A_AOT_QUANTIFICATION_VALUE = property(get_l_2_a_aot_quantification_value, set_l_2_a_aot_quantification_value, del_l_2_a_aot_quantification_value, "L2A_AOT_QUANTIFICATION_VALUE's docstring")
    dnScale = property(get_dn_scale, set_dn_scale, del_dn_scale, "dnScale's docstring")
    timestamp = property(get_timestamp, set_timestamp, del_timestamp, "timestamp's docstring")
    L2A_INSPIRE_XML = property(get_l_2_a_inspire_xml, set_l_2_a_inspire_xml, del_l_2_a_inspire_xml, "L2A_INSPIRE_XML's docstring")
    L2A_MANIFEST_SAFE = property(get_l_2_a_manifest_safe, set_l_2_a_manifest_safe, del_l_2_a_manifest_safe, "L2A_MANIFEST_SAFE's docstring")
    L1C_UP_MTD_XML = property(get_l_1_c_up_mtd_xml, set_l_1_c_up_mtd_xml, del_l_1_c_up_mtd_xml, "L1C_UP_MTD_XML's docstring")
    L1C_DS_MTD_XML = property(get_l_1_c_ds_mtd_xml, set_l_1_c_ds_mtd_xml, del_l_1_c_ds_mtd_xml, "L1C_DS_MTD_XML's docstring")
    L1C_TILE_MTD_XML = property(get_l_1_c_tile_mtd_xml, set_l_1_c_tile_mtd_xml, del_l_1_c_tile_mtd_xml, "L1C_TILE_MTD_XML's docstring")
    L1C_UP_ID = property(get_l_1_c_up_id, set_l_1_c_up_id, del_l_1_c_up_id, "L1C_UP_ID's docstring")
    L1C_DS_ID = property(get_l_1_c_ds_id, set_l_1_c_ds_id, del_l_1_c_ds_id, "L1C_DS_ID's docstring")
    L1C_TILE_ID = property(get_l_1_c_tile_id, set_l_1_c_tile_id, del_l_1_c_tile_id, "L1C_TILE_ID's docstring")
    L2A_UP_MTD_XML = property(get_l_2_a_up_mtd_xml, set_l_2_a_up_mtd_xml, del_l_2_a_up_mtd_xml, "L2A_UP_MTD_XML's docstring")
    L2A_DS_MTD_XML = property(get_l_2_a_ds_mtd_xml, set_l_2_a_ds_mtd_xml, del_l_2_a_ds_mtd_xml, "L2A_DS_MTD_XML's docstring")
    L2A_TILE_MTD_XML = property(get_l_2_a_tile_mtd_xml, set_l_2_a_tile_mtd_xml, del_l_2_a_tile_mtd_xml, "L2A_TILE_MTD_XML's docstring")
    L3_UP_ID = property(get_l_3_up_id, set_l_3_up_id, del_l_3_up_id, "L3_UP_ID's docstring")
    L3_DS_ID = property(get_l_3_ds_id, set_l_3_ds_id, del_l_3_ds_id, "L3_DS_ID's docstring")
    L3_TILE_ID = property(get_l_3_tile_id, set_l_3_tile_id, del_l_3_tile_id, "L3_TILE_ID's docstring")
    L3_TILE_MTD_XML = property(get_l_3_tile_mtd_xml, set_l_3_tile_mtd_xml, del_l_3_tile_mtd_xml, "L3_TILE_MTD_XML's docstring")
    creationDate = property(get_creation_date, set_creation_date, del_creation_date, "creationDate's docstring")
    acquisitionDate = property(get_acquisition_date, set_acquisition_date, del_acquisition_date, "acquisitionDate's docstring")
    L3_UP_DIR = property(get_l_3_up_dir, set_l_3_up_dir, del_l_3_up_dir, "L3_UP_DIR's docstring")
    _shared = {}
    
    def __init__(self, workDir = False):
        self._processorName = 'Sentinel-2 Level 3 Prototype Processor (SEN2THREE)'
        self._processorVersion = '0.0.1'
        self._processorDate = '2015.01.01'

        if(workDir):
            self._home = os.environ['S2L3APPHOME'] + '/'
            self._workDir = workDir
            if(os.environ['S2L3APPCFG'] == ''):
                self._configDir = self._home + 'cfg/'
            else:
                self._configDir = os.environ['S2L3APPCFG'] + '/'
            self._binDir = self._home + 'bin/'
            self._libDir = self._home + 'lib/'
            self._logDir = self._home + 'log/'
            self._configFn = self._configDir + 'L3_GIPP.xml'
            self._tEstimation = 0.0
            self._tEst60 = 100.0
            self._tEst20 = 500.0
            self._tEst10 = 1500.0
            self._processingStatusFn = self._logDir + '/' + '.progress'
            self._processingEstimationFn = self._configDir + '/' + '.estimation'
            if os.path.isfile(self._processingEstimationFn) == False:
            # init processing estimation file:
                config = ConfigParser.RawConfigParser()
                config.add_section('time estimation')
                config.set('time estimation','t_est_60', self._tEst60)
                config.set('time estimation','t_est_20', self._tEst20)
                config.set('time estimation','t_est_10', self._tEst10)
                with open(self._processingEstimationFn, 'a') as configFile:
                    config.write(configFile)
            self._resolution = 60
            self._ncols = -1
            self._nrows = -1
            self._nbnds = -1
            self._tTotal = 0.0
            self._zenith_angle = -1
            self._azimuth_angle = -1
            self._GIPP = ''
            self._ECMWF = ''
            self._DEM = ''
            self._L2A_BOA_QUANTIFICATION_VALUE = 2000
            self._L2A_WVP_QUANTIFICATION_VALUE = 1000
            self._L2A_AOT_QUANTIFICATION_VALUE = 1000
            self._dnScale = 4095
            self._timestamp = datetime.now()
            self._L2A_INSPIRE_XML = None
            self._L2A_MANIFEST_SAFE = None
            self._L1C_UP_MTD_XML = None
            self._L1C_DS_MTD_XML = None
            self._L1C_TILE_MTD_XML = None
            self._L1C_UP_ID = None
            self._L1C_DS_ID = None
            self._L1C_TILE_ID = None
            self._L2A_UP_MTD_XML = None
            self._L2A_DS_MTD_XML = None
            self._L2A_TILE_MTD_XML = None
            self._L3_UP_ID = None
            self._L3_DS_ID = None
            self._L3_TILE_ID = None
            self._L3_TILE_MTD_XML = None
            self._logger = None
            self._fnLog = None
            self._creationDate = None
            self._acquisitionDate = None
            self._classifier = None

    def set_logLevel(self, level):
        self.logger.info('Log level will be updated to: %s', level)
        if (level == 'DEBUG'):
            self.logger.setLevel(logging.DEBUG)
        elif (level == 'INFO'):
            self.logger.setLevel(logging.INFO)
        elif (level == 'WARNING'):
            self.logger.setLevel(logging.WARNING)
        elif (level == 'ERROR'):
            self.logger.setLevel(logging.ERROR)
        elif  (level == 'CRITICAL'):
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger.setLevel(logging.NOTSET)

    def get_logLevel(self):
        if(self.logger.getEffectiveLevel() == logging.DEBUG):
            return 'DEBUG'
        elif(self.logger.getEffectiveLevel() == logging.INFO):
            return 'INFO'
        elif(self.logger.getEffectiveLevel() == logging.WARNING):
            return 'WARNING'
        elif(self.logger.getEffectiveLevel() == logging.ERROR):
            return 'ERROR'
        elif(self.logger.getEffectiveLevel() == logging.CRITICAL):
            return 'CRITICAL'
        else:
            return 'NOTSET'

    loglevel = property(get_logLevel, set_logLevel)
    
    def initLogger(self):
        dt = datetime.now()
        self._creationDate = strftime('%Y%m%dT%H%M%S', dt.timetuple())
        logname = 'L3_' + self._creationDate
        self._logger = logging.Logger(logname)
        self._fnLog = self._logDir + logname + '_report.xml'
        f = open(self._fnLog, 'w')
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<Sen2Cor_Level-3_Report_File>\n')
        f.close()
        lHandler = logging.FileHandler(self._fnLog)
        lFormatter = logging.Formatter('<check>\n<inspection execution=\"%(asctime)s\" level=\"%(levelname)s\" module=\"%(module)s\" function=\"%(funcName)s\" line=\"%(lineno)d\"/>\n<message contentType=\"Text\">%(message)s</message>\n</check>')
        lHandler.setFormatter(lFormatter)
        self._logger.addHandler(lHandler)
        self._logger.level = logging.INFO
        self._logger.info('Application started')
        self._logger.info('Logging system initialized with level: INFO')
        self._logger.info('Application initialized with root level %s', self._home)
        self._logger.info('Report file opened for results')
        self._logger.debug('Module L3_Config initialized')
        return

    def readGipp(self):
        xp = L3_XmlParser(self, 'GIPP')
        xp.validate()
        xp.export()
        
        try:
            doc = objectify.parse(self._configFn)
            root = doc.getroot()
            cs = root.Common_Section
            self.loglevel = cs.Log_Level.text
            self._dnScale = cs.DN_Scale.pyval
            
            l3s = root.L3_Synthesis
            self._minTime = l3s.Min_Time.text
            self._maxTime = l3s.Max_Time.text
            self._priority = l3s.Priority.text
            self._algorithm = l3s.Algorithm.text
            self._cirrusRemoval = l3s.Cirrus_Removal.pyval
            self._shadowRemoval = l3s.Shadow_Removal.pyval
            self._snowRemoval = l3s.Snow_Removal.pyval
            self._maxCloudProbability = l3s.Max_Cloud_Probability.pyval
            self._maxInvalidPixelsPercentage = l3s.Max_Invalid_Pixels_Percentage.pyval
            self._maxAerosolOptical_hickness = l3s.Max_Aerosol_Optical_Thickness.pyval
            self._maxSolarZenithAngle = l3s.Max_Solar_Zenith_Angle.pyval
            self._maxViewingAngle = l3s.Max_Viewing_Angle.pyval
            
            cl = root.Classificators
            self._classifier =  {'NO_DATA'              : cl.NO_DATA.pyval,
                                'SATURATED_DEFECTIVE'   : cl.SATURATED_DEFECTIVE.pyval,
                                'DARK_FEATURES'         : cl.DARK_FEATURES.pyval,
                                'CLOUD_SHADOWS'         : cl.CLOUD_SHADOWS.pyval,
                                'VEGETATION'            : cl.VEGETATION.pyval,
                                'BARE_SOILS'            : cl.BARE_SOILS.pyval,
                                'WATER'                 : cl.WATER.pyval,
                                'LOW_PROBA_CLOUDS'      : cl.LOW_PROBA_CLOUDS.pyval,
                                'MEDIUM_PROBA_CLOUDS'   : cl.MEDIUM_PROBA_CLOUDS.pyval,
                                'HIGH_PROBA_CLOUDS'     : cl.HIGH_PROBA_CLOUDS.pyval,
                                'THIN_CIRRUS'           : cl.THIN_CIRRUS.pyval,
                                'SNOW_ICE'              : cl.SNOW_ICE.pyval,
                                'URBAN_AREAS'           : cl.URBAN_AREAS.pyval
                                }
        except:
            self._logger.fatal('Error in parsing configuration file.')
            self.exitError();
        return True

    def initSelf(self, resolution, tile):
        self.initLogger()
        HelloWorld = self._processorName +', '+ self._processorVersion +', created: '+ self._processorDate
        stdoutWrite('\n%s started ...\n' % HelloWorld)
        self._logger.info(HelloWorld)
        self._resolution = resolution
        self.readGipp()
        self.calcEarthSunDistance2(tile)
        self.setTimeEstimation(resolution)
        self._logger.debug('Module L3_Process initialized')
        return True

    def createL3_UserProduct(self):
        L2A_UP_MASK = '*2A_*'
        L2A_UP_DIR = self.workDir
        if os.path.exists(L2A_UP_DIR) == False:
            stderrWrite('directory "' + L2A_UP_DIR + '" does not exist.')
            self.exitError()
            return False

        # detect the filename for the datastrip metadata:
        L2A_DS_DIR = L2A_UP_DIR + '/DATASTRIP/'
        if os.path.exists(L2A_DS_DIR) == False:
            stderrWrite('directory "%s" does not exist.\n' % L2A_DS_DIR)
            self.exitError()
            return False

        L2A_DS_MASK = '*_L2A_*'
        dirlist = sorted(os.listdir(L2A_DS_DIR))
        found = False
        
        for dirname in dirlist:
            if(fnmatch.fnmatch(dirname, L2A_DS_MASK) == True):
                found = True
                break
        
        if found == False:
            stderrWrite('No metadata in datastrip\n.')
            self.exitError()

        L2A_DS_DIR += dirname
        L2A_DS_MTD_XML = (dirname[:-7]+'.xml').replace('_MSI_', '_MTD_')
        self.L2A_DS_MTD_XML = L2A_DS_DIR + '/' + L2A_DS_MTD_XML

        dirname, basename = os.path.split(L2A_UP_DIR)
        if(fnmatch.fnmatch(basename, L2A_UP_MASK) == False):
            stderrWrite(basename + ': identifier "*2A_*" is missing')
            self.exitError()
            return False

        GRANULE = L2A_UP_DIR + '/GRANULE'
        if os.path.exists(GRANULE) == False:
            stderrWrite('directory "' + GRANULE + '" does not exist.')
            self.exitError()
            return False
        #
        # the product (directory) structure:
        #-------------------------------------------------------
        L3_UP_ID = basename
        L3_UP_ID = L3_UP_ID.replace('L2A_', 'L03_')
        L3_UP_DIR = dirname + '/' + L3_UP_ID
        self._L3_UP_DIR = L3_UP_DIR
        self.L3_UP_ID = L3_UP_ID

        L2A_INSPIRE_XML = L2A_UP_DIR + '/INSPIRE.xml'
        L2A_MANIFEST_SAFE = L2A_UP_DIR + '/manifest.safe'

        L3_INSPIRE_XML = L3_UP_DIR + '/INSPIRE.xml'
        L3_MANIFEST_SAFE = L3_UP_DIR + '/manifest.safe'

        AUX_DATA = '/AUX_DATA'
        DATASTRIP = '/DATASTRIP'
        GRANULE = '/GRANULE'
        HTML = '/HTML'
        REP_INFO = '/rep_info'
        #firstInit = False

        #if(os.path.exists(L3_UP_DIR + GRANULE) == False):
        copy_tree(L2A_UP_DIR + AUX_DATA, L3_UP_DIR + AUX_DATA)
        copy_tree(L2A_UP_DIR + DATASTRIP, L3_UP_DIR + DATASTRIP)
        copy_tree(L2A_UP_DIR + HTML, L3_UP_DIR + HTML)
        copy_tree(L2A_UP_DIR + REP_INFO, L3_UP_DIR + REP_INFO)
        copy_file(L2A_INSPIRE_XML, L3_INSPIRE_XML)
        copy_file(L2A_MANIFEST_SAFE, L3_MANIFEST_SAFE)
        if(os.path.exists(L3_UP_DIR + GRANULE) == False):
            os.mkdir(L3_UP_DIR + GRANULE)

        self.L3_INSPIRE_XML = L2A_INSPIRE_XML
        self.L3_MANIFEST_SAFE = L2A_MANIFEST_SAFE

        #create user product:
        S2A_mask = 'S2A_*'
        filelist = sorted(os.listdir(L2A_UP_DIR))
        found = False
        for filename in filelist:
            if(fnmatch.fnmatch(filename, S2A_mask) == True):
                found = True
                break
        if found == False:
            stderrWrite('No metadata for user product')
            self.exitError()

        # prepare L3 User Product metadata file
        fn_L2A = L2A_UP_DIR  + '/' + filename
        fn_L3 = filename[:4] + 'USER' + filename[8:]
        fn_L3 = fn_L3.replace('L2A_', 'L03_')
        fn_L3 = L3_UP_DIR + '/' + fn_L3
        self.L2A_UP_MTD_XML = fn_L2A        
        self.L3_UP_MTD_XML = fn_L3

        # copy L2A schemes from config_dir into rep_info:    
        xp = L3_XmlParser(self, 'GIPP')
        cs = xp.getRoot('Common_Section')
        upScheme2a = cs.UP_Scheme_2A.text
        tileScheme2a = cs.Tile_Scheme_2A.text
        dsScheme2a = cs.DS_Scheme_2A.text
        copy_file(self.get_config_dir() + upScheme2a, L3_UP_DIR + REP_INFO + '/' + upScheme2a)
        copy_file(self.get_config_dir() + tileScheme2a, L3_UP_DIR + REP_INFO + '/' + tileScheme2a)
        copy_file(self.get_config_dir() + dsScheme2a, L3_UP_DIR + REP_INFO + '/' + dsScheme2a)
        # copy L3 User Product metadata file:
        copy_file(fn_L2A, fn_L3)
        # remove old L2A entries from L3_UP_MTD_XML:
        xp = L3_XmlParser(self, 'UP03')
        if(xp.convert() == False):
            self.logger.fatal('error in converting user product metadata to level 3')
            self.exitError()
        xp = L3_XmlParser(self, 'UP03')
        pi = xp.getTree('General_Info', 'L3_Product_Info')        
        # update L2A entries from L2A_UP_MTD_XML:
        pi.PRODUCT_URI = 'http://www.telespazio-vega.de'
        pi.PROCESSING_LEVEL = 'Level-3p'
        pi.PRODUCT_TYPE = 'S2MSI03p'
        dt = datetime.utcnow()
        pi.GENERATION_TIME = strftime('%Y-%m-%dT%H:%M:%SZ', dt.timetuple())
        pi.PREVIEW_IMAGE_URL = 'http://www.telespazio-vega.de'
        qo = pi.Query_Options
        qo.Aux_List.attrib['productLevel'] = 'Level-3p'
        xp.export()

        #create datastrip ID:
        L3_DS_DIR = self._L3_UP_DIR + DATASTRIP
        dirlist = sorted(os.listdir(L3_DS_DIR))
        found = False
        for dirname in dirlist:
            if(fnmatch.fnmatch(dirname, S2A_mask) == True):
                found = True
                break
        if found == False:
            stderrWrite('No subdirectory in datastrip')
            self.exitError()

        L2A_DS_ID = dirname
        L3_DS_ID = L2A_DS_ID[:4] + 'USER' + L2A_DS_ID[8:]
        L3_DS_ID = L3_DS_ID.replace('L2A_', 'L03_')
        self.L3_DS_ID = L3_DS_ID

        olddir = L3_DS_DIR + '/' + L2A_DS_ID
        newdir = L3_DS_DIR + '/' + L3_DS_ID
        os.rename(olddir, newdir)

        #find datastrip metadada, rename and change it:
        L3_DS_DIR = newdir
        filelist = sorted(os.listdir(L3_DS_DIR))
        found = False
        for filename in filelist:
            if(fnmatch.fnmatch(filename, S2A_mask) == True):
                found = True
                break
        if found == False:
            stderrWrite('No metadata in datastrip')
            self.exitError()

        LXX_DS_MTD_XML = filename
        L3_DS_MTD_XML = LXX_DS_MTD_XML[:4] + 'USER' + LXX_DS_MTD_XML[8:]
        L3_DS_MTD_XML = L3_DS_MTD_XML.replace('L2A_', 'L03_')

        oldfile = L3_DS_DIR + '/' + LXX_DS_MTD_XML
        newfile = L3_DS_DIR + '/' + L3_DS_MTD_XML
        self.L3_DS_MTD_XML = newfile

        os.rename(oldfile, newfile)
        xp = L3_XmlParser(self, 'DS03')
        if(xp.convert() == False):
            self.logger.fatal('error in converting datastrip metadata to level 3')
            self.exitError()
        xp = L3_XmlParser(self, 'DS03')
        ti = xp.getTree('Image_Data_Info', 'Tiles_Information')
        del ti.Tile_List.Tile[:]
        xp.export()  

        return sorted(os.listdir(L2A_UP_DIR + GRANULE))

    def postprocess(self):
        # copy log to QI data as a report:
        dirname, basename = os.path.split(self.L3_TILE_MTD_XML)
        report = basename.replace('.xml', '_Report.xml')
        report = dirname + '/QI_DATA/' + report

        if((os.path.isfile(self._fnLog)) == False):
            self.logger.fatal('Missing file: ' + self._fnLog)
            self.exitError()

        f = open(self._fnLog, 'a')
        f.write('</Sen2Cor_Level-3_Report_File>')
        f.close()
        copy_file(self._fnLog, report)

        return

    def setTimeEstimation(self, resolution):
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.read(self._processingEstimationFn)
        self._tEst60 = config.getfloat('time estimation','t_est_60')
        self._tEst20 = config.getfloat('time estimation','t_est_20')
        self._tEst10 = config.getfloat('time estimation','t_est_10')
        if(resolution == 60):
            self._tEstimation = self._tEst60
        elif(resolution == 20):
            self._tEstimation = self._tEst20
        elif(resolution == 10):
            self._tEstimation = self._tEst10
        return

    def writeTimeEstimation(self, resolution, tMeasure):
        config = ConfigParser.RawConfigParser()
        tMeasureAsString = str(tMeasure)
        config.add_section('time estimation')
        config.set('time estimation','t_est_60', self._tEst60)
        config.set('time estimation','t_est_20', self._tEst20)
        config.set('time estimation','t_est_10', self._tEst10)
        if(resolution == 60):
            config.set('time estimation','t_est_60', tMeasureAsString)
        elif(resolution == 20):
            config.set('time estimation','t_est_20', tMeasureAsString)
        elif(resolution == 10):
            config.set('time estimation','t_est_10', tMeasureAsString)

        with open(self._processingEstimationFn, 'w') as configFile:
            config.write(configFile)
        return

    def timestamp(self, procedure):
        tNow = datetime.now()
        tDelta = tNow - self._timestamp
        self._timestamp = tNow
        self.logger.info('Procedure: ' + procedure + ', elapsed time[s]: %0.3f' % tDelta.total_seconds())
        if(self.logger.getEffectiveLevel()  != logging.NOTSET):
            stdoutWrite('Procedure %s, elapsed time[s]: %0.3f\n' % (procedure, tDelta.total_seconds()))
        #else:
        increment = tDelta.total_seconds() / self._tEstimation
        self._tTotal += increment
        tTotalPercentage = float32(self._tTotal * 100.0)
        stdoutWrite('Progress[%%]: %03.2f : ' % tTotalPercentage)
        #stdout.flush()
        f = open(self._processingStatusFn, 'w')
        f.write(str(tTotalPercentage) + '\n')
        f.close()
        return

    def calcEarthSunDistance2(self, tile):
        year =  int(tile[25:29])
        month = int(tile[29:31])
        day = int(tile[31:33])
        doy = date(year,month,day)
        doy = int(doy.strftime('%j'))
        exc_earth = 0.01673 # earth-sun distance in A.U.
        dastr = 1.0 + exc_earth * sin(2 * pi * (doy - 93.5) / 365.)
        self._d2 = dastr * dastr
        return

    def parNotFound(self, parameter):
        self.logger.fatal('Configuration parameter %s not found in %s', parameter, self._configFn)
        stderrWrite('Configuration parameter <' + parameter + '> not found in ' + self._configFn)
        stderrWrite('Program is forced to terminate.')
        self.__exit()

    def exitError(self, reason = None):
        stderrWrite('Fatal error occurred, see report file for details.')
        if reason: stderrWrite('Reason: ' + reason)
        self.__exit()

    def _getDoc(self):
        from xml.etree import ElementTree as ET
        try:
            tree = ET.parse(self.configFn)
        except Exception, inst:
            self.logger.exception("Unexpected error opening %s: %s", self.configFn, inst)
            self.exitError('Error in XML document')
        doc = tree.getroot()
        return doc

    def getInt(self, label, key):
        doc = self._getDoc()
        parameter = label + '/' + key
        par = doc.find(parameter)
        if par is None: self.parNotFound(parameter)
        return int(par.text)

    def getFloat(self, label, key):
        doc = self._getDoc()
        parameter = label + '/' + key
        par = doc.find(parameter)
        if par is None: self.parNotFound(parameter)
        return float32(par.text)

    def getStr(self, label, key):
        doc = self._getDoc()
        parameter = label + '/' + key
        par = doc.find(parameter)
        if par is None: self.parNotFound(parameter)
        return par.text

    def getIntArray(self, node):
        nrows = len(node)
        if nrows < 0:
            return False

        ncols = len(node[0].split())
        a = zeros([nrows,ncols],dtype=int)

        for i in range(nrows):
            a[i,:] = array(node[i].split(),dtype(int))

        return a

    def getUintArray(self, node):
        nrows = len(node)
        if nrows < 0:
            return False

        ncols = len(node[0].split())
        a = zeros([nrows,ncols],dtype=uint)

        for i in range(nrows):
            a[i,:] = array(node[i].split(),dtype(uint))

        return a

    def getFloatArray(self, node):
        nrows = len(node)
        if nrows < 0:
            return False

        ncols = len(node[0].split())
        a = zeros([nrows,ncols],dtype=float32)

        for i in range(nrows):
            a[i,:] = array(node[i].split(),dtype(float32))

        return a

    def putArrayAsStr(self, a, node):
        if a.ndim == 1:
            nrows = a.shape[0]
            for i in nrows:
                node[i] = a[i],dtype=str

        elif a.ndim == 2:
            nrows = a.shape[0]
            ncols = a.shape[1]
            for i in range(nrows):
                aStr = array_str(a[i,:]).strip('[]')
                node[i] = aStr
        else:
            return False

    def getStringArray(self, node):
        nrows = len(node)
        if nrows < 0:
            return False

        ncols = len(node[0].split())
        a = zeros([nrows,ncols],dtype=str)

        for i in range(nrows):
            a[i,:] = array(node[i].split(),dtype(str))

        return a

