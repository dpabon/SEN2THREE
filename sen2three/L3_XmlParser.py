#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from numpy import *
import os, sys
from lxml import etree, objectify
from L3_Library import stdoutWrite, stderrWrite
from L3_Borg import Borg

class L3_XmlParser(Borg):
    ''' A parser for the assignment of xml based metadata to python configuration objects and vice versa.
        Performs also a validation of the metadata against the corresponding scheme.

            :param productStr: the product string for the given metadata (via __init__).
            :type productStr: a string.

    '''

    def __init__(self, config, productStr):
        self._config = config
        self._productStr = productStr
        self._xmlFn = None
        self._xmlName = None
        self._root = None
        self._tree = None
        self._scheme = None
        try:
            doc = objectify.parse(config.configFn)
            root = doc.getroot()
            cs = root.Common_Section
            upScheme2a = cs.UP_Scheme_2A.text
            upScheme3 = cs.UP_Scheme_3.text            
            tileScheme2a = cs.Tile_Scheme_2A.text
            tileScheme3 = cs.Tile_Scheme_3.text            
            dsScheme2a = cs.DS_Scheme_2A.text
            dsScheme3 = cs.DS_Scheme_3.text
            gippScheme = cs.GIPP_Scheme.text       
        except:
            config.logger.fatal('Error in parsing configuration file.')
            config.exitError();

        if(productStr == 'UP2A'):
            self._xmlFn = config.L2A_UP_MTD_XML
            self._scheme = upScheme2a
        elif(productStr == 'UP03'):
            self._xmlFn = config.L3_TARGET_MTD_XML
            self._scheme = upScheme3            
        elif(productStr == 'DS2A'):
            self._xmlFn = config.L2A_DS_MTD_XML
            self._scheme = dsScheme2a
        elif(productStr == 'DS03'):
            self._xmlFn = config.L3_DS_MTD_XML
            self._scheme = dsScheme3            
        elif(productStr == 'T2A'):
            self._xmlFn = config.L2A_TILE_MTD_XML
            self._scheme = tileScheme2a
        elif(productStr == 'T03'):
            self._xmlFn = config.L3_TILE_MTD_XML
            self._scheme = tileScheme3
        elif(productStr == 'GIPP'):
            self._xmlFn = config.configFn
            self._scheme = gippScheme
        else:
            config.logger.fatal('wrong product identifier for xml structure: ' + productStr)
            config.exitError()
        
        self.setRoot();
        return

    def getRoot(self, key=None):
        ''' Gets the root of an xml tree, addressed by the corresponding key.

            :param key: the search key
            :type key: a string

            :return: the tree
            :rtype: an element tree

        '''
        try:
            if key == None:
                return self._root
            else:
                root = self._root[key]
                return root
        except:
            return False

    def setRoot(self):
        ''' Sets the root of an xml tree.

            :return: true if succesful
            :rtype: bool

        '''

        if self._root is not None:
            return True
        try:
            doc = objectify.parse(self._xmlFn)
            self._root = doc.getroot()
            return True
        except:
            return False

    def getTree(self, key, subkey):
        ''' Gets the subtree of an xml tree, addressed by the corresponding key and subkey.

            :param key: the search key
            :type key: a string
            :param subkey: the search subkey
            :type subkey: a string
            :return: the tree
            :rtype: an element tree

        '''
        try:
            tree = self._root[key]    
            return tree['{}' + subkey]
        except:
            return False

    def setTree(self, key, subkey):
        ''' Sets the subtree of an xml tree, addressed by the corresponding key and subkey.

            :param key: the search key
            :type key: a string
            :param subkey: the search subkey
            :type subkey: a string
            :return: true if succesful
            :rtype: bool

        '''
        try:
            root = self._root[key]
        except:
            return False
        try:
            self._tree = root['{}' + subkey]
            return True
        except:
            self._tree = root
            if(self.append(subkey, '') == True):
                try:
                    self._tree = root['{}' + subkey]
                    self.export()
                    return True        
                except:
                    return False
        return False

    def validate(self):
        """ Validator for the metadata.

            :return: true, if metadata are valid.
            :rtype: boolean

        """
        fn = os.path.basename(self._xmlFn)
        self._config.logger.info('validating metadata file %s against scheme' % fn)
        try:
            schema = etree.XMLSchema(file = os.path.join(self._config.configDir, self._scheme))
            parser = etree.XMLParser(schema = schema)
            objectify.parse(self._xmlFn, parser)
            self._config.logger.info('metadata file is valid')
            ret = True
        except etree.XMLSyntaxError, err:
            stdoutWrite('Metadata file is invalid, see report file for details.\n')
            self._config.logger.error('Schema file: %s' % self._scheme)
            self._config.logger.error('Details: %s' % str(err))
            ret = False
        except:
            stdoutWrite('Unspecific Error in metadata.\n')
            self._config.logger.error('unspecific error in metadata')
            ret = False

        return ret


    def append(self, key, value):
        try:
            e = etree.Element(key)
            e.text = value
            self._tree.append(e)
            return True
        except:
            return False

    def export(self):
        import codecs
        outfile = codecs.open(self._xmlFn, 'w', 'utf-8')
        outfile.write('<?xml version="1.0"  encoding="UTF-8"?>\n')
        objectify.deannotate(self._root, xsi_nil=True, cleanup_namespaces=True)
        outstr = etree.tostring(self._root, pretty_print=True)
        outfile.write(outstr)        
        outfile.close()
        return self.setRoot()

    def convert(self):
        import codecs
        outfile = codecs.open(self._xmlFn, 'w', 'utf-8')
        outfile.write('<?xml version="1.0"  encoding="UTF-8"?>\n')
        objectify.deannotate(self._root, xsi_nil=True, cleanup_namespaces=True)
        outstr = etree.tostring(self._root, pretty_print=True)
        
        if '03' in self._productStr:
            outstr = outstr.replace('Level-2A', 'Level-3')
            outstr = outstr.replace('L2A_Product_Info>', 'L3_Product_Info>')
            outstr = outstr.replace('L2A_SCENE', 'L3_SCENE')
            outstr = outstr.replace('L2A_Scene', 'L3_Scene')
            outstr = outstr.replace('L2A_Product_Organisation>', 'L3_Product_Organisation>')
            outstr = outstr.replace('L2A_Product_Image_Characteristics>', 'L3_Product_Image_Characteristics>')
            outstr = outstr.replace('TILE_ID_2A>', 'TILE_ID_3>')
            outstr = outstr.replace('L2A_Auxiliary_Data_Info', 'L3_Auxiliary_Data_Info')
            outstr = outstr.replace('L2A_Quality_Indicators_Info', 'L3_Quality_Indicators_Info')
            outstr = outstr.replace('DATASTRIP_ID_2A>', 'DATASTRIP_ID_3>')
            if self._productStr == 'UP03':
                outstr = outstr.replace('</PROCESSING_BASELINE>', '</PROCESSING_BASELINE>\n<PROCESSING_ALGORITHM/>\n<RADIOMETRIC_PREFERENCE/>')
 
        outfile.write(outstr)
        outfile.close()
        return self.setRoot()

    def getIntArray(self, node):
        nrows = len(node)
        if nrows < 0:
            return False

        ncols = len(node[0].text.split())
        a = zeros([nrows,ncols],dtype=int)        

        for i in range(nrows):
            a[i,:] = array(node[i].text.split(),dtype(int))
        
        return a

    def getUintArray(self, node):
        nrows = len(node)
        if nrows < 0:
            return False
        
        ncols = len(node[0].text.split())
        a = zeros([nrows,ncols],dtype=uint)
        
        for i in range(nrows):
            a[i,:] = array(node[i].text.split(),dtype(uint))
            
        return a

    def getFloatArray(self, node):
        nrows = len(node)
        if nrows < 0:
            return False
        
        ncols = len(node[0].text.split())
        a = zeros([nrows,ncols],dtype=float32)
        
        for i in range(nrows):
            a[i,:] = array(node[i].text.split(),dtype(float32))
            
        return a

    def getStringArray(self, node):
        nrows = len(node)
        if nrows < 0:
            return False
        
        ncols = len(node[0].text.split())
        a = zeros([nrows,ncols],dtype=str)
        
        for i in range(nrows):
            a[i,:] = array(node[i].text.split(),dtype(str))

        return a

    def setArrayAsStr(self, node, a):
        set_printoptions(precision=6)
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
            return True
        else:
            return False

    def getViewingIncidenceAnglesArray(self, node, bandId, detectorId, _type='Zenith'):
        nrows = len(node)
        for i in range(nrows):
            if((int(node[i].bandId) == bandId) and (int(node[i].detectorId) == detectorId)):
                if _type == 'Zenith':
                    a = self.getFloatArray(node[i].Zenith.Values_List.VALUES)
                elif _type == 'Azimuth':
                    a = self.getFloatArray(node[i].Azimuth.Values_List.VALUES)

                return a
        return False

    def setViewingIncidenceAnglesArray(self, node, arr, bandId, detectorId, _type='Zenith'):
        nrows = len(node)
        for i in range(nrows):
            if((int(node[i].bandId) == bandId) and (int(node[i].detectorId) == detectorId)):
                if _type == 'Zenith':
                    return self.setArrayAsStr(node[i].Zenith.Values_List.VALUES, arr)
                elif _type == 'Azimuth':
                    return self.setArrayAsStr(node[i].Azimuth.Values_List.VALUES, arr)

        return False

    