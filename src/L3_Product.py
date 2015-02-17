#!/usr/bin/env python
'''
Created on Feb 2, 2015
@author: umuellerwilm
'''
import os, fnmatch
from time import strftime
from datetime import datetime
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from lxml import objectify

from L3_Borg import Borg
from L3_XmlParser import L3_XmlParser
from L3_Library import stdoutWrite, stderrWrite

class L3_Product(Borg):
    _shared = {}
    def __init__(self, config):
        self.config = config 
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
        self._L2A_UP_ID = None        
        self._L2A_DS_ID = None
        self._L2A_TILE_ID = None

        self._L3_TARGET_MTD_XML = None
        self._L3_DS_MTD_XML = None
        self._L3_TILE_MTD_XML = None    
        self._L3_TARGET_ID = None        
        self._L3_DS_ID = None
        self._L3_TILE_ID = None
        self._nrTilesProcessed = 0

    def get_nr_tiles_processed(self):
        return self._nrTilesProcessed


    def set_nr_tiles_processed(self, value):
        self._nrTilesProcessed = value


    def del_nr_tiles_processed(self):
        del self._nrTilesProcessed


    def get_config(self):
        return self._config


    def set_config(self, value):
        self._config = value


    def del_config(self):
        del self._config


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


    def get_l_2_a_up_id(self):
        return self._L2A_UP_ID


    def get_l_2_a_ds_id(self):
        return self._L2A_DS_ID


    def get_l_2_a_tile_id(self):
        return self._L2A_TILE_ID


    def get_l_3_target_mtd_xml(self):
        return self._L3_TARGET_MTD_XML


    def get_l_3_ds_mtd_xml(self):
        return self._L3_DS_MTD_XML


    def get_l_3_tile_mtd_xml(self):
        return self._L3_TILE_MTD_XML


    def get_l_3_target_id(self):
        return self._L3_TARGET_ID


    def get_l_3_ds_id(self):
        return self._L3_DS_ID


    def get_l_3_tile_id(self):
        return self._L3_TILE_ID


    def get_l_3_target_dir(self):
        return self._L3_TARGET_DIR


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


    def set_l_2_a_up_id(self, value):
        self._L2A_UP_ID = value


    def set_l_2_a_ds_id(self, value):
        self._L2A_DS_ID = value


    def set_l_2_a_tile_id(self, value):
        self._L2A_TILE_ID = value


    def set_l_3_target_mtd_xml(self, value):
        self._L3_TARGET_MTD_XML = value


    def set_l_3_ds_mtd_xml(self, value):
        self._L3_DS_MTD_XML = value


    def set_l_3_tile_mtd_xml(self, value):
        self._L3_TILE_MTD_XML = value


    def set_l_3_target_id(self, value):
        self._L3_TARGET_ID = value


    def set_l_3_ds_id(self, value):
        self._L3_DS_ID = value


    def set_l_3_tile_id(self, value):
        self._L3_TILE_ID = value


    def set_l_3_target_dir(self, value):
        self._L3_TARGET_DIR = value


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


    def del_l_2_a_up_id(self):
        del self._L2A_UP_ID


    def del_l_2_a_ds_id(self):
        del self._L2A_DS_ID


    def del_l_2_a_tile_id(self):
        del self._L2A_TILE_ID


    def del_l_3_target_mtd_xml(self):
        del self._L3_TARGET_MTD_XML


    def del_l_3_ds_mtd_xml(self):
        del self._L3_DS_MTD_XML


    def del_l_3_tile_mtd_xml(self):
        del self._L3_TILE_MTD_XML


    def del_l_3_target_id(self):
        del self._L3_TARGET_ID


    def del_l_3_ds_id(self):
        del self._L3_DS_ID


    def del_l_3_tile_id(self):
        del self._L3_TILE_ID


    def del_l_3_target_dir(self):
        del self._L3_TARGET_DIR

    config = property(get_config, set_config, del_config, "config's docstring")
    nrTilesProcessed = property(get_nr_tiles_processed, set_nr_tiles_processed, del_nr_tiles_processed, "nrTilesProcessed's docstring")
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
    L2A_UP_ID = property(get_l_2_a_up_id, set_l_2_a_up_id, del_l_2_a_up_id, "L2A_UP_ID's docstring")
    L2A_DS_ID = property(get_l_2_a_ds_id, set_l_2_a_ds_id, del_l_2_a_ds_id, "L2A_DS_ID's docstring")
    L2A_TILE_ID = property(get_l_2_a_tile_id, set_l_2_a_tile_id, del_l_2_a_tile_id, "L2A_TILE_ID's docstring")
    L3_TARGET_MTD_XML = property(get_l_3_target_mtd_xml, set_l_3_target_mtd_xml, del_l_3_target_mtd_xml, "L3_TARGET_MTD_XML's docstring")
    L3_DS_MTD_XML = property(get_l_3_ds_mtd_xml, set_l_3_ds_mtd_xml, del_l_3_ds_mtd_xml, "L3_DS_MTD_XML's docstring")
    L3_TILE_MTD_XML = property(get_l_3_tile_mtd_xml, set_l_3_tile_mtd_xml, del_l_3_tile_mtd_xml, "L3_TILE_MTD_XML's docstring")
    L3_TARGET_ID = property(get_l_3_target_id, set_l_3_target_id, del_l_3_target_id, "L3_TARGET_ID's docstring")
    L3_DS_ID = property(get_l_3_ds_id, set_l_3_ds_id, del_l_3_ds_id, "L3_DS_ID's docstring")
    L3_TILE_ID = property(get_l_3_tile_id, set_l_3_tile_id, del_l_3_tile_id, "L3_TILE_ID's docstring")
    L3_TARGET_DIR = property(get_l_3_target_dir, set_l_3_target_dir, del_l_3_target_dir, "L3_TARGET_DIR's docstring")

    def existL3_TargetProduct(self):
        self.config.logger.info('Checking existence of L3 target product ...')
        L3_TARGET_MASK = '*L03_*'
        L2A_UP_ID = self.config.workDir
        dirlist = sorted(os.listdir(L2A_UP_ID))
        for L3_TARGET_ID in dirlist:
            if fnmatch.fnmatch(L3_TARGET_ID, L3_TARGET_MASK) == True:
                self.config.logger.info('L3 target product already exists.')
                self.L3_TARGET_ID = L3_TARGET_ID
                return self.reinitL3_TargetProduct()
            else:
                continue
        # no L3 target exists, will be created:
        self.config.logger.info('L3 target will be created.')
        return self.createL3_TargetProduct()

        return False                                    

    def createL3_TargetProduct(self):
        self.config.logger.info('Creating L3 target product ...')
        L2A_UP_MASK = '*2A_*'
        L2A_UP_DIR = self.config.workDir + '/' + self.L2A_UP_ID
        # detect the filename for the datastrip metadata:
        L2A_DS_DIR = L2A_UP_DIR + '/DATASTRIP/'
        if os.path.exists(L2A_DS_DIR) == False:
            stderrWrite('directory "%s" does not exist.\n' % L2A_DS_DIR)
            self.config.exitError()
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
            self.config.exitError()

        L2A_DS_DIR += dirname
        L2A_DS_MTD_XML = (dirname[:-7]+'.xml').replace('_MSI_', '_MTD_')
        self.L2A_DS_MTD_XML = L2A_DS_DIR + '/' + L2A_DS_MTD_XML
        xp = L3_XmlParser(self.config, 'DS2A')
        xp.validate()

        dirname, basename = os.path.split(L2A_UP_DIR)
        if(fnmatch.fnmatch(basename, L2A_UP_MASK) == False):
            stderrWrite(basename + ': identifier "*2A_*" is missing.')
            self.config.exitError()
            return False

        GRANULE = L2A_UP_DIR + '/GRANULE'
        if os.path.exists(GRANULE) == False:
            stderrWrite('directory "' + GRANULE + '" does not exist.')
            self.config.exitError()
            return False
        #
        # the product (directory) structure:
        #-------------------------------------------------------
        L3_TARGET_ID = basename
        L3_TARGET_ID = L3_TARGET_ID.replace('L2A_', 'L03_')
        L3_TARGET_ID = L3_TARGET_ID.replace(L3_TARGET_ID[47:62], self.config.minTime)
        L3_TARGET_ID = L3_TARGET_ID.replace(L3_TARGET_ID[63:78], self.config.maxTime)
        L3_TARGET_DIR = dirname + '/' + L3_TARGET_ID
        self.L3_TARGET_DIR = L3_TARGET_DIR
        self.L3_TARGET_ID = L3_TARGET_ID

        L2A_INSPIRE_XML = L2A_UP_DIR + '/INSPIRE.xml'
        L2A_MANIFEST_SAFE = L2A_UP_DIR + '/manifest.safe'

        L3_INSPIRE_XML = L3_TARGET_DIR + '/INSPIRE.xml'
        L3_MANIFEST_SAFE = L3_TARGET_DIR + '/manifest.safe'

        AUX_DATA = '/AUX_DATA'
        DATASTRIP = '/DATASTRIP'
        GRANULE = '/GRANULE'
        HTML = '/HTML'
        REP_INFO = '/rep_info'
 
        copy_tree(L2A_UP_DIR + AUX_DATA, L3_TARGET_DIR + AUX_DATA)
        copy_tree(L2A_UP_DIR + DATASTRIP, L3_TARGET_DIR + DATASTRIP)
        copy_tree(L2A_UP_DIR + HTML, L3_TARGET_DIR + HTML)
        copy_tree(L2A_UP_DIR + REP_INFO, L3_TARGET_DIR + REP_INFO)
        copy_file(L2A_INSPIRE_XML, L3_INSPIRE_XML)
        copy_file(L2A_MANIFEST_SAFE, L3_MANIFEST_SAFE)
        if(os.path.exists(L3_TARGET_DIR + GRANULE) == False):
            os.mkdir(L3_TARGET_DIR + GRANULE)

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
            self.config.exitError()

        # prepare L3 User Product metadata file
        fn_L2A = L2A_UP_DIR  + '/' + filename
        fn_L3 = filename[:4] + 'USER' + filename[8:]
        fn_L3 = fn_L3.replace('L2A_', 'L03_')
        fn_L3 = L3_TARGET_DIR + '/' + fn_L3
        self.L2A_UP_MTD_XML = fn_L2A
        xp = L3_XmlParser(self.config, 'UP2A')
        xp.validate()
        self.L3_TARGET_MTD_XML = fn_L3

        # copy L2A schemes from config_dir into rep_info:    
        xp = L3_XmlParser(self.config, 'GIPP')
        cs = xp.getRoot('Common_Section')
        upScheme2a = cs.UP_Scheme_2A.text
        tileScheme2a = cs.Tile_Scheme_2A.text
        dsScheme2a = cs.DS_Scheme_2A.text
        copy_file(self.config.get_config_dir() + upScheme2a, L3_TARGET_DIR + REP_INFO + '/' + upScheme2a)
        copy_file(self.config.get_config_dir() + tileScheme2a, L3_TARGET_DIR + REP_INFO + '/' + tileScheme2a)
        copy_file(self.config.get_config_dir() + dsScheme2a, L3_TARGET_DIR + REP_INFO + '/' + dsScheme2a)
        # copy L3 User Product metadata file:
        copy_file(fn_L2A, fn_L3)
        # remove old L2A entries from L3_TARGET_MTD_XML:
        xp = L3_XmlParser(self.config, 'UP03')
        if(xp.convert() == False):
            self.logger.fatal('error in converting user product metadata to level 3')
            stderrWrite('Error in converting user product metadata to level 3')
            self.config.exitError()
        xp = L3_XmlParser(self.config, 'UP03')
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
        L3_DS_DIR = self.L3_TARGET_DIR + DATASTRIP
        dirlist = sorted(os.listdir(L3_DS_DIR))
        found = False
        for dirname in dirlist:
            if(fnmatch.fnmatch(dirname, S2A_mask) == True):
                found = True
                break
        if found == False:
            stderrWrite('No subdirectory in datastrip')
            self.config.exitError()

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
            self.config.exitError()

        LXX_DS_MTD_XML = filename
        L3_DS_MTD_XML = LXX_DS_MTD_XML[:4] + 'USER' + LXX_DS_MTD_XML[8:]
        L3_DS_MTD_XML = L3_DS_MTD_XML.replace('L2A_', 'L03_')
        oldfile = L3_DS_DIR + '/' + LXX_DS_MTD_XML
        newfile = L3_DS_DIR + '/' + L3_DS_MTD_XML
        self.L3_DS_MTD_XML = newfile

        os.rename(oldfile, newfile)
        xp = L3_XmlParser(self.config, 'DS03')
        if(xp.convert() == False):
            stderrWrite('Error in converting datastrip metadata to level 3.')
            self.logger.fatal('error in converting datastrip metadata to level 3.')
            self.config.exitError()
        xp = L3_XmlParser(self.config, 'DS03')
        ti = xp.getTree('Image_Data_Info', 'Tiles_Information')
        del ti.Tile_List.Tile[:]
        xp.export()
        return True

    def reinitL3_TargetProduct(self):
        L3_DS_ID = None
        L3_TARGET_MASK = '*L03_*'
        dirlist = sorted(os.listdir(self.config.workDir))
        for L3_TARGET_ID in dirlist:
            if fnmatch.fnmatch(L3_TARGET_ID, L3_TARGET_MASK) == True:
                self.L3_TARGET_ID = L3_TARGET_ID
                self.L3_TARGET_DIR = self.config.workDir + '/' + L3_TARGET_ID
                break
        
        L3_DS_MASK = '*_L03_DS_*'
        L3_DS_DIR = self.config.workDir + '/' + L3_TARGET_ID + '/DATASTRIP'
        dirlist = sorted(os.listdir(L3_DS_DIR))
        for L3_DS_ID in dirlist:
            if fnmatch.fnmatch(L3_DS_ID, L3_DS_MASK) == True:
                self.L3_DS_ID = L3_DS_ID
                break
        
        if L3_DS_ID != None:
            L3_DS_MTD_XML = (L3_DS_ID[:-7]+'.xml').replace('_MSI_', '_MTD_')
            self.L3_DS_MTD_XML = L3_DS_DIR + '/' + L3_DS_ID + '/' + L3_DS_MTD_XML
            return True
        
        return False

    def createL3_Tile(self, tileId):
        L2A_TILE_ID = tileId
        L3_TILE_ID = L2A_TILE_ID.replace('L2A_', 'L03_')
        self.L3_TILE_ID = L3_TILE_ID
        workDir = self.config.workDir + '/'
        L2A_UP_ID = self.L2A_UP_ID + '/'
        L3_TARGET_DIR = self.L3_TARGET_DIR
        GRANULE = '/GRANULE/'
        QI_DATA = '/QI_DATA/'
        self.nrTilesProcessed = 1
        
        L2A_TILE_ID = workDir + L2A_UP_ID + GRANULE + L2A_TILE_ID
        L3_TILE_ID = L3_TARGET_DIR + GRANULE + L3_TILE_ID

        os.mkdir(L3_TILE_ID)
        os.mkdir(L3_TILE_ID + QI_DATA)
        self.config.logger.info('new working directory is: ' + L3_TILE_ID)

        filelist = sorted(os.listdir(L2A_TILE_ID))
        found = False
        L2A_UP_MASK = '*_L2A_*'
        for filename in filelist:
            if(fnmatch.fnmatch(filename, L2A_UP_MASK) == True):
                found = True
                break
        if found == False:
            self.config.logger.fatal('No metadata in tile')
            self.config.exitError()

        L2A_TILE_MTD_XML = L2A_TILE_ID + '/' + filename
        L3_TILE_MTD_XML = filename
        L3_TILE_MTD_XML = L3_TILE_MTD_XML.replace('L2A_', 'L03_')
        L3_TILE_MTD_XML = L3_TILE_ID + '/' + L3_TILE_MTD_XML
        copy_file(L2A_TILE_MTD_XML, L3_TILE_MTD_XML)
        self.L2A_TILE_MTD_XML = L2A_TILE_MTD_XML
        xp = L3_XmlParser(self.config, 'T2A')
        xp.validate()
        self.L3_TILE_MTD_XML = L3_TILE_MTD_XML

        #update tile and datastrip id in metadata file.
        if(self.config.resolution == 60):
            copy_file(L2A_TILE_MTD_XML, L3_TILE_MTD_XML)
            xp = L3_XmlParser(self.config, 'T03')
            if(xp.convert() == False):
                self.logger.fatal('error in converting tile metadata to level 3')
                self.exitError()
            
            #update tile id in ds metadata file.
            xp = L3_XmlParser(self.config, 'DS03')
            ti = xp.getTree('Image_Data_Info', 'Tiles_Information')
            Tile = objectify.Element('Tile', tileId = L3_TILE_ID)
            ti.Tile_List.append(Tile)
            xp.export()
            

        return
    
    def reinitL3_Tile(self, tileId):
        L3_MTD_MASK = 'S2A_*_MTD_L03_TL_*.xml'
        L3_TARGET_DIR = self.L3_TARGET_DIR + '/'
        GRANULE = '/GRANULE/'
        self.nrTilesProcessed += 1
        self.L3_TILE_ID = tileId
        L3_TILE_ID = L3_TARGET_DIR + GRANULE + tileId
        dirlist = sorted(os.listdir(L3_TILE_ID))
        for L3_TILE_MTD_XML in dirlist:
            if fnmatch.fnmatch(L3_TILE_MTD_XML, L3_MTD_MASK) == True:
                self.L3_TILE_MTD_XML = L3_TILE_ID + '/' + L3_TILE_MTD_XML
                break
        #To Do:
        #xp = L3_XmlParser(self.config, 'T03')
        
        #xp.validate()
        return

    def postprocess(self):
        # copy log to QI data as a report:
        dirname, basename = os.path.split(self.L3_TILE_MTD_XML)
        report = basename.replace('.xml', '_Report.xml')
        report = dirname + '/QI_DATA/' + report
        
        if((os.path.isfile(self.config.fnLog)) == False):
            self.logger.fatal('Missing file: ' + self.config.fnLog)
            self.config.exitError()

        f = open(self.config.fnLog, 'a')
        f.write('</Sen2Cor_Level-3_Report_File>')
        f.flush()
        f.close()
        copy_file(self.config.fnLog, report)
        return
 
