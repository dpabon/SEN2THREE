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
            self._configFn = self._configDir + 'L03_GIPP.xml'
            self._calibrationFn = ''
            self._solarIrradianceFn = ''
            self._elevationMapFn = ''
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
            self._dnScale = 4095.0
            self._adj_km = 1.0
            self._d2 = None
            self._dem_unit = 0 # [meter] is default DEM heigh unit unit
            self._orbitPath = None
            self._orbitRow = None
            self._targetPath = None
            self._targetRow = None
            self._sceneStartTime = None
            self._sceneStopTime = None
            self._solaz = None
            self._solaz_arr = None
            self._solze = None
            self._solze_arr = None
            self._vaa_arr = None
            self._vza_arr = None
            self._visibility = 30.0
            self._wl940a = array([0.895, 1.000])     # range of moderate wv absorption region around  940 nm
            self._wl1130a = array([1.079, 1.180])    # range of moderate wv absorption region around 1130 nm
            self._wl1400a = array([1.330, 1.490])    # range for interpolation
            self._wl1900a = array([1.780, 1.970])    # range for interpolation
            self._wv_thr_cirrus = 0.60
            self._timestamp = datetime.now()
            self._c0 = None
            self._c1 = None
            self._e0 = None
            self._d2 = None
            self._wvlsen = None
            self._fwhm = None
            self._acOnly = False
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
            return

    def get_creation_date(self):
        return self._creationDate

    def set_creation_date(self, value):
        self._creationDate = value

    def del_creation_date(self):
        del self._creationDate

    def get_l3_boa_quantification_value(self):
        return self._L3_BOA_QUANTIFICATION_VALUE

    def get_l3_wv_quantification_value(self):
        return self._L3_WV_QUANTIFICATION_VALUE

    def get_l3_aot_quantification_value(self):
        return self._L3_AOT_QUANTIFICATION_VALUE

    def set_l3_boa_quantification_value(self, value):
        self._L3_BOA_QUANTIFICATION_VALUE = value

    def set_l3_wv_quantification_value(self, value):
        self._L3_WV_QUANTIFICATION_VALUE = value

    def set_l3_aot_quantification_value(self, value):
        self._L3_AOT_QUANTIFICATION_VALUE = value

    def del_l3_boa_quantification_value(self):
        del self._L3_BOA_QUANTIFICATION_VALUE

    def del_l3_wv_quantification_value(self):
        del self._L3_WV_QUANTIFICATION_VALUE

    def del_l3_aot_quantification_value(self):
        del self._L3_AOT_QUANTIFICATION_VALUE

    def get_l3_up_dir(self):
        return self._L3_UP_DIR

    def set_l3_up_dir(self, value):
        self._L3_UP_DIR = value

    def del_l3_up_dir(self):
        del self._L3_UP_DIR

    def get_l3_up_id(self):
        return self._L3_UP_ID

    def set_l3_up_id(self, value):
        self._L3_UP_ID = value

    def del_l3_up_id(self):
        del self._L3_UP_ID

    def get_l3_ds_id(self):
        return self._L3_DS_ID

    def get_l3_tile_id(self):
        return self._L3_TILE_ID

    def get_l3_tile_mtd_xml(self):
        return self._L2A_TILE_MTD_XML

    def get_l3_inspire_xml(self):
        return self._L3_INSPIRE_XML

    def get_l3_manifest_safe(self):
        return self._L3_MANIFEST_SAFE

    def get_l3_up_mtd_xml(self):
        return self._L3_UP_MTD_XML

    def get_l3_ds_mtd_xml(self):
        return self._L3_DS_MTD_XML

    def set_l3_tile_mtd_xml(self, value):
        self._L2A_TILE_MTD_XML = value

    def set_l3_ds_id(self, value):
        self._L3_DS_ID = value

    def set_l3_tile_id(self, value):
        self._L3_TILE_ID = value

    def set_l3_inspire_xml(self, value):
        self._L3_INSPIRE_XML = value

    def set_l3_manifest_safe(self, value):
        self._L3_MANIFEST_SAFE = value

    def set_l3_up_mtd_xml(self, value):
        self._L3_UP_MTD_XML = value

    def set_l3_ds_mtd_xml(self, value):
        self._L3_DS_MTD_XML = value

    def del_l3_ds_id(self):
        del self._L3_DS_ID

    def del_l3_tile_id(self):
        del self._L3_TILE_ID

    def del_l3_tile_mtd_xml(self):
        del self._L2A_TILE_MTD_XML

    def del_l3_inspire_xml(self):
        del self._L3_INSPIRE_XML

    def del_l3_manifest_safe(self):
        del self._L3_MANIFEST_SAFE

    def del_l3_up_mtd_xml(self):
        del self._L3_UP_MTD_XML

    def del_l3_ds_mtd_xml(self):
        del self._L3_DS_MTD_XML

    def get_entity_id(self):
        return self._entityId

    def get_acquisition_date(self):
        return self._acquisitionDate

    def get_orbit_path(self):
        return self._orbitPath

    def get_orbit_row(self):
        return self._orbitRow

    def get_target_path(self):
        return self._targetPath

    def get_target_row(self):
        return self._targetRow

    def get_station_sgs(self):
        return self._stationSgs

    def get_scene_start_time(self):
        return self._sceneStartTime

    def get_scene_stop_time(self):
        return self._sceneStopTime

    def set_entity_id(self, value):
        self._entityId = value

    def set_acquisition_date(self, value):
        self._acquisitionDate = value

    def set_orbit_path(self, value):
        self._orbitPath = value

    def set_orbit_row(self, value):
        self._orbitRow = value

    def set_target_path(self, value):
        self._targetPath = value

    def set_target_row(self, value):
        self._targetRow = value

    def set_station_sgs(self, value):
        self._stationSgs = value

    def set_scene_start_time(self, value):
        self._sceneStartTime = value

    def set_scene_stop_time(self, value):
        self._sceneStopTime = value

    def del_entity_id(self):
        del self._entityId

    def del_acquisition_date(self):
        del self._acquisitionDate

    def del_orbit_path(self):
        del self._orbitPath

    def del_orbit_row(self):
        del self._orbitRow

    def del_target_path(self):
        del self._targetPath

    def del_target_row(self):
        del self._targetRow

    def del_station_sgs(self):
        del self._stationSgs

    def del_scene_start_time(self):
        del self._sceneStartTime

    def del_scene_stop_time(self):
        del self._sceneStopTime

    def get_dn_scale(self):
        return self._dnScale

    def set_dn_scale(self, value):
        self._dnScale = value

    def del_dn_scale(self):
        del self._dnScale

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

    def get_processor_name(self):
        return self._processorName

    def get_processor_version(self):
        return self._processorVersion

    def get_processor_date(self):
        return self._processorDate

    def set_processor_name(self, value):
        self._processorName = value

    def set_processor_version(self, value):
        self._processorVersion = value

    def set_processor_date(self, value):
        self._processorDate = value

    def del_processor_name(self):
        del self._processorName

    def del_processor_version(self):
        del self._processorVersion

    def del_processor_date(self):
        del self._processorDate

    def get_ncols(self):
        return self._ncols

    def get_nrows(self):
        return self._nrows

    def get_nbnds(self):
        return self._nbnds

    def get_zenith_angle(self):
        return self._zenith_angle

    def get_azimuth_angle(self):
        return self._azimuth_angle

    def get_gipp(self):
        return self._GIPP

    def get_ecmwf(self):
        return self._ECMWF

    def set_ncols(self, value):
        self._ncols = value

    def set_nrows(self, value):
        self._nrows = value

    def set_nbnds(self, value):
        self._nbnds = value

    def set_zenith_angle(self, value):
        self._zenith_angle = value

    def set_azimuth_angle(self, value):
        self._azimuth_angle = value

    def set_gipp(self, value):
        self._GIPP = value

    def set_ecmwf(self, value):
        self._ECMWF = value

    def del_ncols(self):
        del self._ncols

    def del_nrows(self):
        del self._nrows

    def del_nbnds(self):
        del self._nbnds

    def del_zenith_angle(self):
        del self._zenith_angle

    def del_azimuth_angle(self):
        del self._azimuth_angle

    def del_gipp(self):
        del self._GIPP

    def del_ecmwf(self):
        del self._ECMWF

    def __exit__(self):
        sys.exit(-1)

    def get_output_fn(self):
        return self._outputFn

    def set_output_fn(self, value):
        self._outputFn = self._dataDir + value

    def del_output_fn(self):
        del self._outputFn

    def get_solar_irradiance_fn(self):
        return self._solarIrradianceFn

    def set_solar_irradiance_fn(self, value):
        self._solarIrradianceFn = value


    def del_solar_irradiance_fn(self):
        del self._solarIrradianceFn


    def get_shadow_map_fn(self):
        return self._shadowMapFn


    def set_shadow_map_fn(self, value):
        self._shadowMapFn =  self._dataDir + value


    def del_shadow_map_fn(self):
        del self._shadowMapFn


    def get_sensor_fn(self):
        return self._sensorFn


    def set_sensor_fn(self, value):
        self._sensorFn = value


    def del_sensor_fn(self):
        del self._sensorFn


    def get_home(self):
        return self._home


    def get_work_dir(self):
        return self._workDir


    def get_data_dir(self):
        return self._dataDir


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


    def get_input_fn(self):
        return self._inputFn


    def get_aot_fn(self):
        return self._aotFn


    def get_aspect_fn(self):
        return self._aspectFn


    def get_atm_data_fn(self):
        return self._atmDataFn


    def get_calibr_fn(self):
        return self._calibrationFn


    def get_class_map_fn(self):
        return self._classMapFn


    def get_cloud_qi_map_fn(self):
        return self._cloudQiMapFn


    def get_ddv_fn(self):
        return self._ddvFn


    def get_elevation_map_fn(self):
        return self._elevationMapFn


    def get_hcw_fn(self):
        return self._hcwFn


    def get_ilumination_fn(self):
        return self._iluminationFn


    def get_sky_view_fn(self):
        return self._skyViewFn


    def get_slope_fn(self):
        return self._slopeFn

    def get_snow_qi_map_fn(self):
        return self._snowQiMapFn

    def get_vis_index_fn(self):
        return self._visIndexFn

    def get_water_vapor_fn(self):
        return self._waterVaporFn

    def get_logger(self):
        return self._logger

    def get_cellsize(self):
        return self._cellsize

    def get_dem_unit(self):
        return self._dem_unit

    def get_pixelsize(self):
        return self._pixelsize

    def get_resolution(self):
        return self._resolution

    def set_home(self, value):
        self._home = value

    def set_work_dir(self, value):
        self._workDir = value

    def set_data_dir(self, value):
        self._dataDir = self.home + value + '/'

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

    def set_input_fn(self, value):
        self._inputFn = self._dataDir + value

    def set_aot_fn(self, value):
        self._aotFn =  self._dataDir + value

    def set_aspect_fn(self, value):
        self._aspectFn =  self._dataDir + value

    def set_atm_data_fn(self, value):
        self._atmDataFn = value

    def set_calibr_fn(self, value):
        self._calibrationFn = value

    def set_class_map_fn(self, value):
        self._classMapFn =  self._dataDir + value

    def set_cloud_qi_map_fn(self, value):
        self._cloudQiMapFn =  self._dataDir + value

    def set_ddv_fn(self, value):
        self._ddvFn =  self._dataDir + value

    def set_elevation_map_fn(self, value):
        self._elevationMapFn =  self._dataDir + value

    def set_hcw_fn(self, value):
        self._hcwFn =  self._dataDir + value

    def set_ilumination_fn(self, value):
        self._iluminationFn =  self._dataDir + value

    def set_sky_view_fn(self, value):
        self._skyViewFn =  self._dataDir + value

    def set_slope_fn(self, value):
        self._slopeFn =  self._dataDir + value

    def set_snow_qi_map_fn(self, value):
        self._snowQiMapFn =  self._dataDir + value

    def set_vis_index_fn(self, value):
        self._visIndexFn =  self._dataDir + value

    def set_water_vapor_fn(self, value):
        self._waterVaporFn =  self._dataDir + value

    def set_logger(self, value):
        self._logger = value

    def set_date(self, value):
        self._date = value

    def set_dem_unit(self, value):
        self._dem_unit = value

    def set_resolution(self, value):
        self._resolution = value
        self._pixelsize = value
        self._cellsize = value

    def set_ratio_blu_red(self, value):
        self._ratio_blu_red = value

    def del_home(self):
        del self._home

    def del_work_dir(self):
        del self._workDir

    def del_data_dir(self):
        del self._dataDir

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

    def del_input_fn(self):
        del self._inputFn

    def del_aot_fn(self):
        del self._aotFn

    def del_aspect_fn(self):
        del self._aspectFn

    def del_atm_data_fn(self):
        del self._atmDataFn

    def del_calibr_fn(self):
        del self._calibrationFn

    def del_class_map_fn(self):
        del self._classMapFn

    def del_cloud_qi_map_fn(self):
        del self._cloudQiMapFn

    def del_ddv_fn(self):
        del self._ddvFn

    def del_elevation_map_fn(self):
        del self._elevationMapFn

    def del_hcw_fn(self):
        del self._hcwFn

    def del_ilumination_fn(self):
        del self._iluminationFn

    def del_sky_view_fn(self):
        del self._skyViewFn

    def del_slope_fn(self):
        del self._slopeFn

    def del_snow_qi_map_fn(self):
        del self._snowQiMapFn

    def del_vis_index_fn(self):
        del self._visIndexFn

    def del_water_vapor_fn(self):
        del self._waterVaporFn

    def del_logger(self):
        del self._logger

    def del_cellsize(self):
        del self._cellsize

    def del_date(self):
        del self._date

    def del_dem_unit(self):
        del self._dem_unit

    def del_pixelsize(self):
        del self._pixelsize

    def del_resolution(self):
        del self._resolution

    # Properties:
    processorName = property(get_processor_name, set_processor_name, del_processor_name, "processorName's docstring")
    processorVersion = property(get_processor_version, set_processor_version, del_processor_version, "processorVersion's docstring")
    processorDate = property(get_processor_date, set_processor_date, del_processor_date, "processorDate's docstring")
    home = property(get_home, set_home, del_home, "home's docstring")
    workDir = property(get_work_dir, set_work_dir, del_work_dir, "workDir's docstring")
    dataDir = property(get_data_dir, set_data_dir, del_data_dir, "dataDir's docstring")
    configDir = property(get_config_dir, set_config_dir, del_config_dir, "configDir's docstring")
    binDir = property(get_bin_dir, set_bin_dir, del_bin_dir, "binDir's docstring")
    libDir = property(get_lib_dir, set_lib_dir, del_lib_dir, "libDir's docstring")
    logDir = property(get_log_dir, set_log_dir, del_log_dir, "logDir's docstring")
    configFn = property(get_config_fn, set_config_fn, del_config_fn, "configFn's docstring")
    logger = property(get_logger, set_logger, del_logger, "logger's docstring")
    dem_unit = property(get_dem_unit, set_dem_unit, del_dem_unit, "dem_unit's docstring")
    resolution = property(get_resolution, set_resolution, del_resolution, "resolution's docstring")
    zenith_angle = property(get_zenith_angle, set_zenith_angle, del_zenith_angle, "zenith_angle's docstring")
    azimuth_angle = property(get_azimuth_angle, set_azimuth_angle, del_azimuth_angle, "azimuth_angle's docstring")
    GIPP = property(get_gipp, set_gipp, del_gipp, "GIPP's docstring")
    ECMWF = property(get_ecmwf, set_ecmwf, del_ecmwf, "ECMWF's docstring")
    dnScale = property(get_dn_scale, set_dn_scale, del_dn_scale, "dnScale's docstring")
    sceneStartTime = property(get_scene_start_time, set_scene_start_time, del_scene_start_time, "sceneStartTime's docstring")
    sceneStopTime = property(get_scene_stop_time, set_scene_stop_time, del_scene_stop_time, "sceneStopTime's docstring")
    L2A_TILE_MTD_XML = property(get_l3_tile_mtd_xml, set_l3_tile_mtd_xml, del_l3_tile_mtd_xml, "L2A_TILE_MTD_XML's docstring")
    L3_INSPIRE_XML = property(get_l3_inspire_xml, set_l3_inspire_xml, del_l3_inspire_xml, "L3_INSPIRE_XML's docstring")
    L3_MANIFEST_SAFE = property(get_l3_manifest_safe, set_l3_manifest_safe, del_l3_manifest_safe, "L3_MANIFEST_SAFE's docstring")
    L3_UP_MTD_XML = property(get_l3_up_mtd_xml, set_l3_up_mtd_xml, del_l3_up_mtd_xml, "L3_USER_PRODUCT_MTD_XML's docstring")
    L3_DS_MTD_XML = property(get_l3_ds_mtd_xml, set_l3_ds_mtd_xml, del_l3_ds_mtd_xml, "L3_DS_MTD_XML's docstring")
    L3_TILE_MTD_XML = property(get_l3_tile_mtd_xml, set_l3_tile_mtd_xml, del_l3_tile_mtd_xml, "L3_TILE_MTD_XML's docstring")
    L3_TILE_ID = property(get_l3_tile_id, set_l3_tile_id, del_l3_tile_id, "L3_TILE_ID's docstring")
    L3_DS_ID = property(get_l3_ds_id, set_l3_ds_id, del_l3_ds_id, "L3_TILE_ID's docstring")
    L3_UP_ID = property(get_l3_up_id, set_l3_up_id, del_l3_up_id, "L3_UP_ID's docstring")
    L3_UP_DIR = property(get_l3_up_dir, set_l3_up_dir, del_l3_up_dir, "L3_UP_DIR's docstring")
    acquisitionDate = property(get_acquisition_date, set_acquisition_date, del_acquisition_date, "acquisitionDate's docstring")
    creationDate = property(get_creation_date, set_creation_date, del_creation_date, "creationDate's docstring")

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
    
    def initLog(self):
        dt = datetime.now()
        self.creationDate = strftime('%Y%m%dT%H%M%S', dt.timetuple())
        logname = 'L2A_' + self.creationDate
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

    def createL3_UserProduct(self):
        L2A_UP_MASK = '*2A_*'
        L2A_UP_DIR = self.workDir
        if os.path.exists(L2A_UP_DIR) == False:
            stderrWrite('directory "' + L2A_UP_DIR + '" does not exist.')
            self.exitError()
            return False

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
        firstInit = False

        if(os.path.exists(L3_UP_DIR + GRANULE) == False):
            copy_tree(L2A_UP_DIR + AUX_DATA, L3_UP_DIR + AUX_DATA)
            copy_tree(L2A_UP_DIR + DATASTRIP, L3_UP_DIR + DATASTRIP)
            copy_tree(L2A_UP_DIR + HTML, L3_UP_DIR + HTML)
            copy_tree(L2A_UP_DIR + REP_INFO, L3_UP_DIR + REP_INFO)
            copy_file(L2A_INSPIRE_XML, L3_INSPIRE_XML)
            copy_file(L2A_MANIFEST_SAFE, L3_MANIFEST_SAFE)
            os.mkdir(L3_UP_DIR + GRANULE)
            firstInit = True

        self.L2A_INSPIRE_XML = L2A_INSPIRE_XML
        self.L3_INSPIRE_XML = L3_INSPIRE_XML
        self.L2A_MANIFEST_SAFE = L2A_MANIFEST_SAFE
        self.L3_MANIFEST_SAFE = L3_MANIFEST_SAFE

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
        if firstInit == True:
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
            xp = L3_XmlParser(self, 'UP2A')
            if(xp.convert() == False):
                self.tracer.fatal('error in converting user product metadata to level 3')
                self.exitError()
            xp = L3_XmlParser(self, 'UP2A')
            pi = xp.getTree('General_Info', 'L2A_Product_Info')
            del pi.L3_Product_Organisation.Granule_List[:]            
            # update L2A entries from L2A_UP_MTD_XML:
            pi.PRODUCT_URI = 'http://www.telespazio-vega.de'
            pi.PROCESSING_LEVEL = 'Level-3p'
            pi.PRODUCT_TYPE = 'S2MSI03p'
            dt = datetime.utcnow()
            pi.GENERATION_TIME = strftime('%Y-%m-%dT%H:%M:%SZ', dt.timetuple())
            pi.PREVIEW_IMAGE_URL = 'http://www.telespazio-vega.de'
            qo = pi.Query_Options
            #qo.PREVIEW_IMAGE = True
            #qo.METADATA_LEVEL = 'Standard'
            qo.Aux_List.attrib['productLevel'] = 'Level-3p'
            xp.export()

        #create datastrip ID:
        self._L3_DS_DIR = self._L3_UP_DIR + DATASTRIP
        dirlist = sorted(os.listdir(self._L3_DS_DIR))
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
        L3_DS_ID = L3_DS_ID.replace('L2A_', 'L3_')
        self.L3_DS_ID = L3_DS_ID

        olddir = self._L3_DS_DIR + '/' + L2A_DS_ID
        newdir = self._L3_DS_DIR + '/' + L3_DS_ID

        if firstInit == True:
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

        oldfile = self._L3_DS_DIR + '/' + L3_DS_MTD_XML
        newfile = self._L3_DS_DIR + '/' + L3_DS_MTD_XML
        self.L3_DS_MTD_XML = newfile

        if firstInit == True:
            os.rename(oldfile, newfile)
            xml = L3_XmlParser(self, 'DS')
            del xml.root.Image_Data_Info.Tiles_Information.Tile_List.Tile[:]
            xml.export()

        return sorted(os.listdir(L3_UP_DIR + GRANULE))

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
        from sys import stdout
        tNow = time()
        tDelta = tNow - self._timestamp
        self._timestamp = tNow
        self.logger.info('Procedure: ' + procedure + ', elapsed time[s]: %0.3f' % tDelta)
        if(self.logger.getEffectiveLevel()  != logging.NOTSET):
            print 'Procedure: ' + procedure + ', elapsed time[s]: %0.3f' % tDelta
        else:
            increment = tDelta / self._tEstimation
            self._tTotal += increment
            tTotalPercentage = float32(self._tTotal * 100.0)
            stdout.write('\rProgress [%%]: %3.2f ' % tTotalPercentage)
            stdout.flush()
            f = open(self._processingStatusFn, 'w')
            f.write(str(tTotalPercentage) + '\n')
            f.close()
        return

    def calcEarthSunDistance2(self, tile):
        year =  int(tile[25:29])
        month = int(tile[29:31])
        day = int(tile[31:33])
        doy = datetime.date(year,month,day)
        doy = int(doy.strftime('%j'))
        exc_earth = 0.01673 # earth-sun distance in A.U.
        dastr = 1.0 + exc_earth * sin(2 * pi * (doy - 93.5) / 365.)
        self._d2 = dastr * dastr
        return

    def parNotFound(self, parameter):
        self.logger.fatal('Configuration parameter %s not found in %s', parameter, self._configFn)
        print 'Configuration parameter <' + parameter + '> not found in ' + self._configFn
        print 'Program is forced to terminate.'
        self.__exit__()

    def exitError(self, reason = None):
        print 'Fatal error occurred, see logfile for details.'
        if reason: print 'Reason: ' + reason
        self.__exit__()

    def openXML(self, filename):
        try:
            tree = ET.parse(filename)
        except Exception, inst:
            self.logger.exception("Unexpected error opening %s: %s", filename, inst)
            self.exitError()
            return False
        return tree

    def readPreferences(self):
        doc = self._getDoc()
    ### Common_Section:
        parameter = ('Common_Section')
        par = doc.find(parameter)
        if par is None: self.parNotFound(parameter)

        parameter = ('Common_Section/DN_Scale')
        par = doc.find(parameter)
        if par is None: self.parNotFound(parameter)
        self.dnScale = float32(par.text)

        parameter = ('Common_Section/Trace_Level')
        par = doc.find(parameter)
        if par is None: self.parNotFound(parameter)
        self.traceLevel = par.text
        return

    def _get_subNodes(self, node, valtype):
        count = int(node.attrib['count'])
        if(valtype == 'int'):
            arr = zeros([count], int)
        elif(valtype == 'float'):
            arr = zeros([count], float32)
        else:
            self.logger.error('wrong type declatarion: ' + type)
            self.parNotFound('wrong type declatarion: ' + type)

        i = 0
        for sub in node:
            if(valtype == 'int'):
                arr[i] = int(sub.text)
            else:
                arr[i] = float32(sub.text)
            i += 1
        return arr

    def _getDoc(self):
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
            print nrows, ncols
            for i in range(nrows):
                aStr = array_str(a[i,:]).strip('[]')
                print aStr
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
