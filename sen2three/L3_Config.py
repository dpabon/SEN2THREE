#!/usr/bin/env python

from numpy import *
import sys, os, time
import logging
import ConfigParser
from lxml import etree, objectify
from time import strftime
from datetime import datetime, date
from distutils.file_util import copy_file

from L3_Borg import Borg
from L3_Library import stdoutWrite, stderrWrite
from L3_Product import L3_Product
from L3_XmlParser import L3_XmlParser

class L3_Config(Borg):
    _shared = {}
    def __init__(self, resolution, workDir = None):
        if(workDir):
            self._home = os.environ['SEN2THREE_HOME'] + '/'
            moduleDir = os.environ['SEN2THREE_BIN'] + '/'            
            self._workDir = workDir
            self._configDir = moduleDir + 'cfg/'
            self._configFn = self._home + 'cfg/L3_GIPP.xml'
            self._libDir = moduleDir + 'lib/'
            self._logDir = self._home + 'log/'
            if not os.path.exists(self._logDir):
                os.mkdir(self._logDir)
            self._processorVersion = None
            self._product = L3_Product(self)
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
            self._resolution = resolution
            self._ncols = -1
            self._nrows = -1
            self._nbnds = -1
            self._tTotal = 0.0
            self._solaz = None
            self._solaz_arr = None
            self._solze = None
            self._solze_arr = None
            self._vaa_arr = None
            self._vza_arr = None            
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
            self._displayData = False
            self._creationDate = None
            self._acquisitionDate = None
            self._classifier = None
            self._minTime = None
            self._maxTime = None
            self._algorithm = 'MOST_RECENT'
            self._radiometricPreference = 'AOT'
            self._cirrusRemoval = True
            self._shadowRemoval = True
            self._snowRemoval = True
            self._nrTilesProcessed = 0
            self._maxCloudProbability = None
            self._maxInvalidPixelsPercentage = None
            self._minAerosolOptical_thickness = None
            self._maxSolarZenithAngle = None
            self._classifier = None
            self._targetDirectory = None
            self._c0 = None
            self._c1 = None
            self._e0 = None
            self._d2 = None

    def get_target_directory(self):
        return self._targetDirectory


    def set_target_directory(self, value):
        self._targetDirectory = value


    def del_target_directory(self):
        del self._targetDirectory


    def get_processor_version(self):
        return self._processorVersion


    def set_processor_version(self, value):
        self._processorVersion = value


    def del_processor_version(self):
        del self._processorVersion


    def get_solaz(self):
        return self._solaz


    def get_solaz_arr(self):
        return self._solaz_arr


    def get_solze(self):
        return self._solze


    def get_solze_arr(self):
        return self._solze_arr


    def get_vaa_arr(self):
        return self._vaa_arr


    def get_vza_arr(self):
        return self._vza_arr


    def set_solaz(self, value):
        self._solaz = value


    def set_solaz_arr(self, value):
        self._solaz_arr = value


    def set_solze(self, value):
        self._solze = value


    def set_solze_arr(self, value):
        self._solze_arr = value


    def set_vaa_arr(self, value):
        self._vaa_arr = value


    def set_vza_arr(self, value):
        self._vza_arr = value


    def del_solaz(self):
        del self._solaz


    def del_solaz_arr(self):
        del self._solaz_arr


    def del_solze(self):
        del self._solze


    def del_solze_arr(self):
        del self._solze_arr


    def del_vaa_arr(self):
        del self._vaa_arr


    def del_vza_arr(self):
        del self._vza_arr

    
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


    def get_algorithm(self):
        return self._algorithm


    def get_cirrus_removal(self):
        return self._cirrusRemoval


    def get_shadow_removal(self):
        return self._shadowRemoval


    def get_snow_removal(self):
        return self._snowRemoval


    def get_nr_tiles_processed(self):
        return self._nrTilesProcessed


    def set_nr_tiles_processed(self, value):
        self._nrTilesProcessed = value


    def del_nr_tiles_processed(self):
        del self._nrTilesProcessed


    def get_max_cloud_probability(self):
        return self._maxCloudProbability


    def get_max_invalid_pixels_percentage(self):
        return self._maxInvalidPixelsPercentage


    def get_min_aerosol_optical_thickness(self):
        return self._minAerosolOptical_thickness


    def get_max_solar_zenith_angle(self):
        return self._maxSolarZenithAngle


    def get_max_viewing_angle(self):
        return self._maxViewingAngle


    def set_min_time(self, value):
        self._minTime = value


    def set_max_time(self, value):
        self._maxTime = value


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


    def set_min_aerosol_optical_thickness(self, value):
        self._minAerosolOptical_thickness = value


    def set_max_solar_zenith_angle(self, value):
        self._maxSolarZenithAngle = value


    def set_max_viewing_angle(self, value):
        self._maxViewingAngle = value


    def del_min_time(self):
        del self._minTime


    def del_max_time(self):
        del self._maxTime


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


    def del_min_aerosol_optical_thickness(self):
        del self._minAerosolOptical_thickness


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


    def get_fn_log(self):
        return self._fnLog


    def set_fn_log(self, value):
        self._fnLog = value


    def del_fn_log(self):
        del self._fnLog


    def get_display_data(self):
        return self._displayData


    def get_radiometric_preference(self):
        return self._radiometricPreference


    def set_display_data(self, value):
        self._displayData = value


    def set_radiometric_preference(self, value):
        self._radiometricPreference = value


    def del_display_data(self):
        del self._displayData


    def del_radiometric_preference(self):
        del self._radiometricPreference


    def get_d_2(self):
        return self._d2


    def get_c_0(self):
        return self._c0


    def get_c_1(self):
        return self._c1


    def get_e_0(self):
        return self._e0


    def set_d_2(self, value):
        self._d2 = value


    def set_c_0(self, value):
        self._c0 = value


    def set_c_1(self, value):
        self._c1 = value


    def set_e_0(self, value):
        self._e0 = value


    def del_d_2(self):
        del self._d2


    def del_c_0(self):
        del self._c0


    def del_c_1(self):
        del self._c1


    def del_e_0(self):
        del self._e0

    fnLog = property(get_fn_log, set_fn_log, del_fn_log, "fnLog's docstring")
    product = property(get_product, set_product, del_product, "product's docstring")
    processorVersion = property(get_processor_version, set_processor_version, del_processor_version, "processorVersion's docstring")
    minTime = property(get_min_time, set_min_time, del_min_time, "minTime's docstring")
    maxTime = property(get_max_time, set_max_time, del_max_time, "maxTime's docstring")
    algorithm = property(get_algorithm, set_algorithm, del_algorithm, "algorithm's docstring")
    cirrusRemoval = property(get_cirrus_removal, set_cirrus_removal, del_cirrus_removal, "cirrusRemoval's docstring")
    shadowRemoval = property(get_shadow_removal, set_shadow_removal, del_shadow_removal, "shadowRemoval's docstring")
    snowRemoval = property(get_snow_removal, set_snow_removal, del_snow_removal, "snowRemoval's docstring")
    nrTilesProcessed = property(get_nr_tiles_processed, set_nr_tiles_processed, del_nr_tiles_processed, "maxTilesProcessed's docstring")
    maxCloudProbability = property(get_max_cloud_probability, set_max_cloud_probability, del_max_cloud_probability, "maxCloudProbability's docstring")
    maxInvalidPixelsPercentage = property(get_max_invalid_pixels_percentage, set_max_invalid_pixels_percentage, del_max_invalid_pixels_percentage, "maxInvalidPixelsPercentage's docstring")
    minAerosolOptical_thickness = property(get_min_aerosol_optical_thickness, set_min_aerosol_optical_thickness, del_min_aerosol_optical_thickness, "minAerosolOptical_thickness's docstring")
    maxSolarZenithAngle = property(get_max_solar_zenith_angle, set_max_solar_zenith_angle, del_max_solar_zenith_angle, "maxSolarZenithAngle's docstring")
    maxViewingAngle = property(get_max_viewing_angle, set_max_viewing_angle, del_max_viewing_angle, "maxViewingAngle's docstring")
    resolution = property(get_resolution, set_resolution, del_resolution, "resolution's docstring")
    shared = property(get_shared, set_shared, del_shared, "shared's docstring")
    classifier = property(get_classifier, set_classifier, del_classifier, "classifier's docstring")
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
    displayData = property(get_display_data, set_display_data, del_display_data, "displayData's docstring")
    radiometricPreference = property(get_radiometric_preference, set_radiometric_preference, del_radiometric_preference, "radiometricPreference's docstring")
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
    d2 = property(get_d_2, set_d_2, del_d_2, "d2's docstring")
    c0 = property(get_c_0, set_c_0, del_c_0, "c0's docstring")
    c1 = property(get_c_1, set_c_1, del_c_1, "c1's docstring")
    e0 = property(get_e_0, set_e_0, del_e_0, "e0's docstring")
    loglevel = property(get_logLevel, set_logLevel)
    logger = property(get_logger, set_logger, del_logger, "logger's docstring")
    solaz = property(get_solaz, set_solaz, del_solaz, "solaz's docstring")
    solaz_arr = property(get_solaz_arr, set_solaz_arr, del_solaz_arr, "solaz_arr's docstring")
    solze = property(get_solze, set_solze, del_solze, "solze's docstring")
    solze_arr = property(get_solze_arr, set_solze_arr, del_solze_arr, "solze_arr's docstring")
    vaa_arr = property(get_vaa_arr, set_vaa_arr, del_vaa_arr, "vaa_arr's docstring")
    vza_arr = property(get_vza_arr, set_vza_arr, del_vza_arr, "vza_arr's docstring")
    targetDirectory = property(get_target_directory, set_target_directory, del_target_directory, "targetDirectory's docstring")    
    
    
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
        xp.export()
        # xp.validate()
        try:
            doc = objectify.parse(self._configFn)
            root = doc.getroot()
            cs = root.Common_Section
            self.loglevel = cs.Log_Level.text
            self._displayData = cs.Display_Data
            self._dnScale = cs.DN_Scale.pyval
            self._targetDirectory = cs.Target_Directory.text

            l3s = root.L3_Synthesis
            self._minTime = l3s.Min_Time.text
            self._maxTime = l3s.Max_Time.text
            self._algorithm = l3s.Algorithm.text
            self._radiometricPreference = l3s.Radiometric_Preference.text
            self._cirrusRemoval = l3s.Cirrus_Removal.pyval
            self._shadowRemoval = l3s.Shadow_Removal.pyval
            self._snowRemoval = l3s.Snow_Removal.pyval
            self._maxCloudProbability = l3s.Max_Cloud_Probability.pyval
            self._maxInvalidPixelsPercentage = l3s.Max_Invalid_Pixels_Percentage.pyval
            self._minAerosolOptical_thickness = l3s.Min_Aerosol_Optical_Thickness.pyval
            self._maxSolarZenithAngle = l3s.Max_Solar_Zenith_Angle.pyval
            
            cl = root.Scene_Classification.Classificators
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

    def init(self, processorVersion):
            self._processorVersion = processorVersion
            self.initLogger()
            self.readGipp()
            self.setTimeEstimation(self.resolution)

    def updateUserProduct(self, userProduct):
        self.product.L2A_UP_ID = userProduct
        if self.product.existL3_TargetProduct() == False:
            stderrWrite('directory "%s" L3 target product is missing\n.' % self.workDir)
            self.exitError()   
        return True

    def updateTile(self, tile, nrTilesProcessed):
        self.nrTilesProcessed = nrTilesProcessed
        self.product.L2A_TILE_ID = tile       
        self.calcEarthSunDistance2(tile)
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

    def checkTimeRange(self, userProduct):       
        def replace(string):
            for ch in ['-',':', 'Z']:
                if ch in string:
                    string=string.replace(ch, '')
            return string
        
        cfgMinTimeS = replace(self.minTime)
        cfgMaxTimeS = replace(self.maxTime)
        prdMinTimeS = userProduct[47:62]
        prdMaxTimeS = userProduct[63:78]
        cfgMinTime = time.mktime(datetime.strptime(cfgMinTimeS,'%Y%m%dT%H%M%S').timetuple())
        cfgMaxTime = time.mktime(datetime.strptime(cfgMaxTimeS,'%Y%m%dT%H%M%S').timetuple())        
        prdMinTime = time.mktime(datetime.strptime(prdMinTimeS,'%Y%m%dT%H%M%S').timetuple())
        prdMaxTime = time.mktime(datetime.strptime(prdMaxTimeS,'%Y%m%dT%H%M%S').timetuple())        
        self.minTime = cfgMinTimeS
        self.maxTime = cfgMaxTimeS
      
        if prdMinTime < cfgMinTime:
            return False
        elif prdMaxTime > cfgMaxTime:
            return False
        else:
            return True

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

    def readTileMetadata(self):
        xp = L3_XmlParser(self, 'T2A')
        ang = xp.getTree('Geometric_Info', 'Tile_Angles')
        azimuthAnglesList = ang.Sun_Angles_Grid.Azimuth.Values_List.VALUES
        solaz_arr = xp.getFloatArray(azimuthAnglesList)
        zenithAnglesList = ang.Sun_Angles_Grid.Zenith.Values_List.VALUES
        solze_arr = xp.getFloatArray(zenithAnglesList)
        # images may be not squared - this is the case for the current testdata used
        # angle arrays have to be adapted, otherwise the bilinear interpolation is misaligned.
        imgSizeList = xp.getTree('Geometric_Info', 'Tile_Geocoding')
        size = imgSizeList.Size
        sizelen = len(size)
        nrows = None
        ncols = None
        for i in range(sizelen):
            if int(size[i].attrib['resolution']) == self._resolution:
                nrows = int(size[i].NROWS)
                ncols = int(size[i].NCOLS)
                break

        if(nrows == None or ncols == None):
            self.exitError('no image dimension in metadata specified, please correct')

        if(nrows < ncols):
            last_row = int(solaz_arr[0].size * float(nrows)/float(ncols) + 0.5)
            saa = solaz_arr[0:last_row,:]
            sza = solze_arr[0:last_row,:]
        elif(ncols < nrows):
            last_col = int(solaz_arr[1].size * float(ncols)/float(nrows) + 0.5)
            saa = solaz_arr[:,0:last_col]
            sza = solze_arr[:,0:last_col]
        else:
            saa = solaz_arr
            sza = solze_arr

        if(saa.max() < 0):
            saa *= -1
        self.saaArray = clip(saa, 0, 360.0)

        sza = absolute(sza)
        self.solze_arr = clip(sza, 0, 70.0)

        self.nrows = nrows
        self.ncols = ncols
        solze = float32(ang.Mean_Sun_Angle.ZENITH_ANGLE.text)
        solaz = float32(ang.Mean_Sun_Angle.AZIMUTH_ANGLE.text)

        self._solze = absolute(solze)
        if self._solze > 70.0:
            self._solze = 70.0

        if solaz < 0:
            solaz *= -1
        if solaz > 360.0:
            solaz = 360.0
        self._solaz = solaz

        #
        # ATCOR employs the Lamberts reflectance law and assumes a constant viewing angle per tile (sub-scene)
        # as this is not given, this is a workaround, which have to be improved in a future version
        #
        viewAnglesList = ang.Mean_Viewing_Incidence_Angle_List.Mean_Viewing_Incidence_Angle
        arrlen = len(viewAnglesList)
        vaa = zeros(arrlen, float32)
        vza = zeros(arrlen, float32)
        for i in range(arrlen):
            vaa[i] = float32(viewAnglesList[i].AZIMUTH_ANGLE.text)
            vza[i] = float32(viewAnglesList[i].ZENITH_ANGLE.text)

        _min = vaa.min()
        _max = vaa.max()
        if _min < 0: _min += 360
        if _max < 0: _max += 360
        vaa_arr = array([_min,_min,_max,_max])
        self.vaa_arr = vaa_arr.reshape(2,2)

        _min = absolute(vza.min())
        _max = absolute(vza.max())
        if _min > 40.0: _min = 40.0
        if _max > 40.0: _max = 40.0
        vza_arr = array([_min,_min,_max,_max])
        self.vza_arr = vza_arr.reshape(2,2)
        return

    def postprocess(self):
        xp = L3_XmlParser(self, 'UP2A')
        auxdata = xp.getTree('L2A_Auxiliary_Data_Info', 'Aux_Data')
        gipp = auxdata.L2A_GIPP_List
        dirname, basename = os.path.split(self.product.L2A_TILE_MTD_XML)
        fn1r = basename.replace('_MTD_', '_GIP_')
        fn2r = fn1r.replace('.xml', '')
        gippFn = etree.Element('GIPP_FILENAME', type='GIP_Level-2Ap', version=self._processorVersion)
        gippFn.text = fn2r
        gipp.append(gippFn)
        xp.export()

        # copy log to QI data as a report:
        report = basename.replace('.xml', '_Report.xml')
        report = dirname + '/QI_DATA/' + report

        if((os.path.isfile(self._fnLog)) == False):
            self.tracer.fatal('Missing file: ' + self._fnLog)
            self.exitError()

        f = open(self._fnLog, 'a')
        f.write('</Sen2Cor_Level-2A_Report_File>')
        f.close()
        copy_file(self._fnLog, report)
               
        '''
        if os.path.exists(self._fnTrace):
            os.remove(self._fnTrace)
        if os.path.exists(self._fnLog):
            os.remove(self._fnLog)
        '''
        return

    def parNotFound(self, parameter):
        self.logger.fatal('Configuration parameter %s not found in %s', parameter, self._configFn)
        stderrWrite('Configuration parameter <%s> not found in %s\n' % (parameter, self._configFn))
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

    
    
