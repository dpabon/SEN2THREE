#!/usr/bin/env python

from numpy import *
import sys, os
import logging
import ConfigParser
from lxml import objectify
from time import strftime
from datetime import datetime, date
from L3_Borg import Borg
from L3_Library import stdoutWrite, stderrWrite
from L3_Product import L3_Product
from L3_XmlParser import L3_XmlParser

class L3_Config(Borg):
    _shared = {}
    def __init__(self, workDir = None):
        self._processorName = 'Sentinel-2 Level 3 Prototype Processor (SEN2THREE)'
        self._processorVersion = '0.0.1'
        self._processorDate = '2015.01.01'

        if(workDir):
            self._home = os.environ['S2L3APPHOME'] + '/'
            self._workDir = workDir
            self._product = L3_Product(self)
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
            self._logger = None
            self._fnLog = None
            self._creationDate = None
            self._acquisitionDate = None
            self._classifier = None
            self._minTime = None
            self._maxTime = None
            self._priority = None
            self._algorithm = None
            self._cirrusRemoval = None
            self._shadowRemoval = None
            self._snowRemoval = None
            self._maxCloudProbability = None
            self._maxInvalidPixelsPercentage = None
            self._maxAerosolOptical_hickness = None
            self._maxSolarZenithAngle = None
            self._maxViewingAngle = None
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
    

    def __exit__(self):
        sys.exit(-1)


    def get_logger(self):
        return self._logger


    def set_logger(self, value):
        self._logger = value


    def del_logger(self):
        del self._logger


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


    def get_creation_date(self):
        return self._creationDate


    def get_acquisition_date(self):
        return self._acquisitionDate


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


    def set_creation_date(self, value):
        self._creationDate = value


    def set_acquisition_date(self, value):
        self._acquisitionDate = value


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


    def del_creation_date(self):
        del self._creationDate


    def del_acquisition_date(self):
        del self._acquisitionDate


    def del_l_3_up_dir(self):
        del self._L3_UP_DIR
        

    def get_resolution(self):
        return self._resolution


    def set_resolution(self, value):
        self._resolution = value


    def del_resolution(self):
        del self._resolution


    def get_classifier(self):
        return self._classifier


    def set_classifier(self, value):
        self._classifier = value


    def del_classifier(self):
        del self._classifier


    def get_min_time(self):
        return self._minTime


    def get_max_time(self):
        return self._maxTime


    def get_priority(self):
        return self._priority


    def get_algorithm(self):
        return self._algorithm


    def get_cirrus_removal(self):
        return self._cirrusRemoval


    def get_shadow_removal(self):
        return self._shadowRemoval


    def get_snow_removal(self):
        return self._snowRemoval


    def get_max_cloud_probability(self):
        return self._maxCloudProbability


    def get_max_invalid_pixels_percentage(self):
        return self._maxInvalidPixelsPercentage


    def get_max_aerosol_optical_hickness(self):
        return self._maxAerosolOptical_hickness


    def get_max_solar_zenith_angle(self):
        return self._maxSolarZenithAngle


    def get_max_viewing_angle(self):
        return self._maxViewingAngle


    def set_min_time(self, value):
        self._minTime = value


    def set_max_time(self, value):
        self._maxTime = value


    def set_priority(self, value):
        self._priority = value


    def set_algorithm(self, value):
        self._algorithm = value


    def set_cirrus_removal(self, value):
        self._cirrusRemoval = value


    def set_shadow_removal(self, value):
        self._shadowRemoval = value


    def set_snow_removal(self, value):
        self._snowRemoval = value


    def set_max_cloud_probability(self, value):
        self._maxCloudProbability = value


    def set_max_invalid_pixels_percentage(self, value):
        self._maxInvalidPixelsPercentage = value


    def set_max_aerosol_optical_hickness(self, value):
        self._maxAerosolOptical_hickness = value


    def set_max_solar_zenith_angle(self, value):
        self._maxSolarZenithAngle = value


    def set_max_viewing_angle(self, value):
        self._maxViewingAngle = value


    def del_min_time(self):
        del self._minTime


    def del_max_time(self):
        del self._maxTime


    def del_priority(self):
        del self._priority


    def del_algorithm(self):
        del self._algorithm


    def del_cirrus_removal(self):
        del self._cirrusRemoval


    def del_shadow_removal(self):
        del self._shadowRemoval


    def del_snow_removal(self):
        del self._snowRemoval


    def del_max_cloud_probability(self):
        del self._maxCloudProbability


    def del_max_invalid_pixels_percentage(self):
        del self._maxInvalidPixelsPercentage


    def del_max_aerosol_optical_hickness(self):
        del self._maxAerosolOptical_hickness


    def del_max_solar_zenith_angle(self):
        del self._maxSolarZenithAngle


    def del_max_viewing_angle(self):
        del self._maxViewingAngle
    
    
    def get_product(self):
        return self._product


    def set_product(self, value):
        self._product = value


    def del_product(self):
        del self._product

    product = property(get_product, set_product, del_product, "product's docstring")
    minTime = property(get_min_time, set_min_time, del_min_time, "minTime's docstring")
    maxTime = property(get_max_time, set_max_time, del_max_time, "maxTime's docstring")
    priority = property(get_priority, set_priority, del_priority, "priority's docstring")
    algorithm = property(get_algorithm, set_algorithm, del_algorithm, "algorithm's docstring")
    cirrusRemoval = property(get_cirrus_removal, set_cirrus_removal, del_cirrus_removal, "cirrusRemoval's docstring")
    shadowRemoval = property(get_shadow_removal, set_shadow_removal, del_shadow_removal, "shadowRemoval's docstring")
    snowRemoval = property(get_snow_removal, set_snow_removal, del_snow_removal, "snowRemoval's docstring")
    maxCloudProbability = property(get_max_cloud_probability, set_max_cloud_probability, del_max_cloud_probability, "maxCloudProbability's docstring")
    maxInvalidPixelsPercentage = property(get_max_invalid_pixels_percentage, set_max_invalid_pixels_percentage, del_max_invalid_pixels_percentage, "maxInvalidPixelsPercentage's docstring")
    maxAerosolOptical_hickness = property(get_max_aerosol_optical_hickness, set_max_aerosol_optical_hickness, del_max_aerosol_optical_hickness, "maxAerosolOptical_hickness's docstring")
    maxSolarZenithAngle = property(get_max_solar_zenith_angle, set_max_solar_zenith_angle, del_max_solar_zenith_angle, "maxSolarZenithAngle's docstring")
    maxViewingAngle = property(get_max_viewing_angle, set_max_viewing_angle, del_max_viewing_angle, "maxViewingAngle's docstring")
    resolution = property(get_resolution, set_resolution, del_resolution, "resolution's docstring")
    shared = property(get_shared, set_shared, del_shared, "shared's docstring")
    classifier = property(get_classifier, set_classifier, del_classifier, "classifier's docstring")
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
    creationDate = property(get_creation_date, set_creation_date, del_creation_date, "creationDate's docstring")
    acquisitionDate = property(get_acquisition_date, set_acquisition_date, del_acquisition_date, "acquisitionDate's docstring")
    loglevel = property(get_logLevel, set_logLevel)
    logger = property(get_logger, set_logger, del_logger, "logger's docstring")
    
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

    def init(self, resolution, tile):
        self.initLogger()
        self.readGipp()
        self._resolution = resolution
        self.setTimeEstimation(resolution)
        self.calcEarthSunDistance2(tile)
        self._logger.debug('Module L3_Process initialized')
        if self.product.exists() == False:
            stderrWrite('directory "%s" target product is missing\n.' % self.workDir)
            self.exitError()   
        return True

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
        self.__exit__()

    def exitError(self, reason = None):
        stderrWrite('Fatal error occurred, see report file for details.')
        if reason: stderrWrite('Reason: ' + reason)
        self.__exit__()

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

