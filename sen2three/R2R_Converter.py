#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
processorName = 'Sentinel-2 Reflectance to Radiance Converter'
processorVersion = '0.9.0'
processorDate = '2015.06.15'
productVersion = '12'

from tables import *
import sys, os
import fnmatch
from time import time

from L3_Config import L3_Config
from L2A_Tables import L2A_Tables
from L3_Tables import L3_Tables
from L3_Product import L3_Product
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from L3_Library import stdoutWrite, stderrWrite


class R2R_Converter(object):
    def __init__(self, config):
        self._config = config

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

    
    def convert(self):
        self.config.logger.info('Converting reflectance to radiance')
        return

def main(args=None):
    import argparse
    descr = processorName +', '+ processorVersion +', created: '+ processorDate + \
        ', supporting Level-1C product version: ' + productVersion + '.'
     
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('directory', help='Directory where the reflectance input files are located')
    args = parser.parse_args()

    # SIITBX-49: directory should not end with '/':
    directory = args.directory
    if directory[-1] == '/':
        directory = directory[:-1]

    # check if directory argument starts with a relative path. If not, expand: 
    if(os.path.isabs(directory)) == False:
        cwd = os.getcwd()
        directory = os.path.join(cwd, directory)
    elif os.path.exists(args.directory) == False:
        stderrWrite('directory "%s" does not exist\n.' % args.directory)
        return False

    config = L3_Config('60', directory)
    config.init(processorVersion)
    result = False

    HelloWorld = processorName +', '+ processorVersion +', created: '+ processorDate
    stdoutWrite('\n%s started ...\n' % HelloWorld)    
    processor = R2R_Converter(config)
    upList = sorted(os.listdir(directory))
    L1C_mask = 'S2?_*L1C_*'
    L2A_mask = 'S2?_*L2A_*'
    for UP_ID in upList:
        if(fnmatch.fnmatch(UP_ID, L1C_mask) == False):     
            continue
        if(fnmatch.fnmatch(UP_ID, L2A_mask) == False):     
            continue

        upFullPath = os.path.join(directory, UP_ID)
        upRad = config.targetDirectory
        if upRad == 'DEFAULT':
            upRad = upFullPath + '_rad'
        copy_tree(upFullPath, upRad)
        result = processor.convert(upRad)
        if(result == False):
            stderrWrite('Application terminated with errors, see log file and traces.\n')
            return False
                
    stdoutWrite('\nApplication terminated successfully.\n')
    return result

if __name__ == "__main__":
    sys.exit(main() or 0)
