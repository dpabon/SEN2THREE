import L3_Config
import L3_UserProduct
import L3_Datastrip
import L3_Tile
import L2A_Tile
from numpy import *


class L3_XmlParser():
    def __init__(self, config, product):
        self._config = config
        self._xmlFn = None
        self._xmlName = None
        self._root = None
        if(product == 'TILE'):
            self._obj = L3_Tile
            self._xmlFn = config.L3_TILE_MTD_XML
            self._xmlName = 'Level-3_Tile_ID'
        elif(product == 'T2A'):
            self._obj = L2A_Tile
            self._xmlFn = config.L2A_TILE_MTD_XML
            self._xmlName = 'Level-2A_Tile_ID'          
        elif(product == 'UP'):
            self._obj = L3_UserProduct
            self._xmlFn = config.L3_UP_MTD_XML
            self._xmlName = 'Level-3_User_Product'
        elif(product == 'DS'):
            self._obj = L3_Datastrip
            self._xmlFn = config.L3_DS_MTD_XML
            self._xmlName = 'Level-3_DataStrip_ID'            
        else:
            self._config.tracer.fatal('wrong identifier for xml structure: ' + product)
            self._config.exitError() 
        return

    
    def getRoot(self):
        if self._root == None:
            self._root = self._obj.parse(self._xmlFn)
        return self._root

    root = property(getRoot, "root's docstring")


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


    def getStringArray(self, node):
        nrows = len(node)
        if nrows < 0:
            return False
        
        ncols = len(node[0].split())
        a = zeros([nrows,ncols],dtype=str)
        
        for i in range(nrows):
            a[i,:] = array(node[i].split(),dtype(str))

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
            print nrows, ncols
            for i in range(nrows):
                aStr = array_str(a[i,:]).strip('[]')
                print aStr
                node[i] = aStr
            return True
        else:
            return False

    
    def getViewingIncidenceAnglesArray(self, node, bandId, detectorId, type='Zenith'):
        nrows = len(node)
        for i in range(nrows):
            if((int(node[i].bandId) == bandId) and (int(node[i].detectorId) == detectorId)):
                if type == 'Zenith':
                    a = self.getFloatArray(node[i].Zenith.Values_List.VALUES)
                elif type == 'Azimuth':
                    a = self.getFloatArray(node[i].Azimuth.Values_List.VALUES)

                return a
        return False


    def setViewingIncidenceAnglesArray(self, node, arr, bandId, detectorId, type='Zenith'):
        nrows = len(node)
        for i in range(nrows):
            if((int(node[i].bandId) == bandId) and (int(node[i].detectorId) == detectorId)):
                if type == 'Zenith':
                    return self.setArrayAsStr(node[i].Zenith.Values_List.VALUES, arr)
                elif type == 'Azimuth':
                    return self.setArrayAsStr(node[i].Azimuth.Values_List.VALUES, arr)

        return False


    def export(self):
        outfile = open(self._xmlFn, 'w')
        outfile.write('<?xml version="1.0" ?>\n')
        self._root.export(outfile, 0, name_= self._xmlName, namespacedef_='', pretty_print=True)
        outfile.close()
        return
