#!/usr/bin/env python
'''
Created on Feb 2, 2015
@author: umuellerwilm
'''
import os, fnmatch, time
from time import strftime
from datetime import datetime
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file

from L3_Borg import Borg
from L3_XmlParser import L3_XmlParser
from L3_Library import stdoutWrite, stderrWrite

class L3_Product(Borg):
    _shared = {}
    def __init__(self, config):
        self._config = config 
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
 
        
    def checkTimeRange(self, L2A_UP_DIR):       
        def replace(string):
            for ch in ['-',':', 'Z']:
                if ch in string:
                    string=string.replace(ch, '')
            return string
        
        cfgMinTimeS = replace(self._config.minTime)
        cfgMaxTimeS = replace(self._config.maxTime)
        prdMinTimeS = L2A_UP_DIR[47:62]
        prdMaxTimeS = L2A_UP_DIR[63:78]
        cfgMinTime = time.mktime(datetime.strptime(cfgMinTimeS,'%Y%m%dT%H%M%S').timetuple())
        cfgMaxTime = time.mktime(datetime.strptime(cfgMaxTimeS,'%Y%m%dT%H%M%S').timetuple())        
        prdMinTime = time.mktime(datetime.strptime(prdMinTimeS,'%Y%m%dT%H%M%S').timetuple())
        prdMaxTime = time.mktime(datetime.strptime(prdMaxTimeS,'%Y%m%dT%H%M%S').timetuple())        
        self._config.minTime = cfgMinTimeS
        self._config.maxTime = cfgMaxTimeS
      
        if prdMinTime < cfgMinTime:
            return False
        elif prdMaxTime > cfgMaxTime:
            return False
        else:
            return True

    def exists(self):
        self._config.logger.info('Checking existence of L3 target product ...')
        L3_TARGET_MASK = '*L03_*'
        dirlist = sorted(os.listdir(self._config.workDir))
        for L3_TARGET_PRODUCT in dirlist:     
            if fnmatch.fnmatch(L3_TARGET_PRODUCT, L3_TARGET_MASK) == True:
                self._config.logger.info('L3 target product already exists.')
                return True
            
        L2A_UP_MASK = '*2A_*'
        for L2A_UP_DIR in dirlist:
            if fnmatch.fnmatch(L2A_UP_DIR, L2A_UP_MASK) == True:
                if self.checkTimeRange(L2A_UP_DIR) == True:
                    self._L2A_UP_ID = self._config.workDir + '/' + L2A_UP_DIR
                    return self.createL3_TargetProduct()
                
            
        stderrWrite('L2A user products: all generation times out of bounds, check configuration.\n')
        self._config.exitError()
        return False                                    

    def createL3_TargetProduct(self):
        self._config.logger.info('Creating L3 target product ...')
        L2A_UP_MASK = '*2A_*'
        L2A_UP_DIR = self._L2A_UP_ID
        # detect the filename for the datastrip metadata:
        L2A_DS_DIR = L2A_UP_DIR + '/DATASTRIP/'
        if os.path.exists(L2A_DS_DIR) == False:
            stderrWrite('directory "%s" does not exist.\n' % L2A_DS_DIR)
            self._config.exitError()
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
            self._config.exitError()

        L2A_DS_DIR += dirname
        L2A_DS_MTD_XML = (dirname[:-7]+'.xml')
        self.L2A_DS_MTD_XML = L2A_DS_DIR + '/' + L2A_DS_MTD_XML

        dirname, basename = os.path.split(L2A_UP_DIR)
        if(fnmatch.fnmatch(basename, L2A_UP_MASK) == False):
            stderrWrite(basename + ': identifier "*2A_*" is missing.')
            self._config.exitError()
            return False

        GRANULE = L2A_UP_DIR + '/GRANULE'
        if os.path.exists(GRANULE) == False:
            stderrWrite('directory "' + GRANULE + '" does not exist.')
            self._config.exitError()
            return False
        #
        # the product (directory) structure:
        #-------------------------------------------------------
        L3_TARGET_ID = basename
        L3_TARGET_ID = L3_TARGET_ID.replace('L2A_', 'L03_')
        L3_TARGET_ID = L3_TARGET_ID.replace(L3_TARGET_ID[47:62], self._config.minTime)
        L3_TARGET_ID = L3_TARGET_ID.replace(L3_TARGET_ID[63:78], self._config.maxTime)
        L3_TARGET_DIR = dirname + '/' + L3_TARGET_ID
        self._L3_TARGET_DIR = L3_TARGET_DIR
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
        #firstInit = False

        #if(os.path.exists(L3_TARGET_DIR + GRANULE) == False):
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
            self._config.exitError()

        # prepare L3 User Product metadata file
        fn_L2A = L2A_UP_DIR  + '/' + filename
        fn_L3 = filename[:4] + 'USER' + filename[8:]
        fn_L3 = fn_L3.replace('L2A_', 'L03_')
        fn_L3 = L3_TARGET_DIR + '/' + fn_L3
        self.L2A_UP_MTD_XML = fn_L2A        
        self.L3_TARGET_MTD_XML = fn_L3

        # copy L2A schemes from config_dir into rep_info:    
        xp = L3_XmlParser(self._config, 'GIPP')
        cs = xp.getRoot('Common_Section')
        upScheme2a = cs.UP_Scheme_2A.text
        tileScheme2a = cs.Tile_Scheme_2A.text
        dsScheme2a = cs.DS_Scheme_2A.text
        copy_file(self._config.get_config_dir() + upScheme2a, L3_TARGET_DIR + REP_INFO + '/' + upScheme2a)
        copy_file(self._config.get_config_dir() + tileScheme2a, L3_TARGET_DIR + REP_INFO + '/' + tileScheme2a)
        copy_file(self._config.get_config_dir() + dsScheme2a, L3_TARGET_DIR + REP_INFO + '/' + dsScheme2a)
        # copy L3 User Product metadata file:
        copy_file(fn_L2A, fn_L3)
        # remove old L2A entries from L3_TARGET_MTD_XML:
        xp = L3_XmlParser(self._config, 'UP03')
        if(xp.convert() == False):
            self.logger.fatal('error in converting user product metadata to level 3')
            self._config.exitError()
        xp = L3_XmlParser(self._config, 'UP03')
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
        L3_DS_DIR = self._L3_TARGET_DIR + DATASTRIP
        dirlist = sorted(os.listdir(L3_DS_DIR))
        found = False
        for dirname in dirlist:
            if(fnmatch.fnmatch(dirname, S2A_mask) == True):
                found = True
                break
        if found == False:
            stderrWrite('No subdirectory in datastrip')
            self._config.exitError()

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
            self._config.exitError()

        LXX_DS_MTD_XML = filename
        L3_DS_MTD_XML = LXX_DS_MTD_XML[:4] + 'USER' + LXX_DS_MTD_XML[8:]
        L3_DS_MTD_XML = L3_DS_MTD_XML.replace('L2A_', 'L03_')

        oldfile = L3_DS_DIR + '/' + LXX_DS_MTD_XML
        newfile = L3_DS_DIR + '/' + L3_DS_MTD_XML
        self.L3_DS_MTD_XML = newfile

        os.rename(oldfile, newfile)
        xp = L3_XmlParser(self._config, 'DS03')
        if(xp.convert() == False):
            self.logger.fatal('error in converting datastrip metadata to level 3')
            self._config.exitError()
        xp = L3_XmlParser(self._config, 'DS03')
        ti = xp.getTree('Image_Data_Info', 'Tiles_Information')
        del ti.Tile_List.Tile[:]
        xp.export()

    def postprocess(self):
        # copy log to QI data as a report:
        dirname, basename = os.path.split(self.L3_TILE_MTD_XML)
        report = basename.replace('.xml', '_Report.xml')
        report = dirname + '/QI_DATA/' + report

        if((os.path.isfile(self._fnLog)) == False):
            self.logger.fatal('Missing file: ' + self._fnLog)
            self._config.exitError()

        f = open(self._fnLog, 'a')
        f.write('</Sen2Cor_Level-3_Report_File>')
        f.close()
        copy_file(self._fnLog, report)

        return
