#!/usr/bin/env python
'''
Created on Feb 24, 2012
@author: umuellerwilm
'''
import fnmatch
import subprocess
import threading
import sys, os
import glob
import L3_UserProduct
import L3_Tile
from numpy import *
from tables import *
import numexpr as ne
from tables.description import *
from distutils.dir_util import copy_tree, mkpath
from distutils.file_util import copy_file
from L3_Config import L3_Config
from L3_Library import rectBivariateSpline
from L3_Library import showImage
from L3_XmlParser import L3_XmlParser
from L3_Borg import Borg
from PIL import *

try:
    from osgeo import gdal,osr
    from osgeo.gdalconst import *
    gdal.TermProgress = gdal.TermProgress_nocb
except ImportError:
    import gdal,osr
    from gdalconst import *


class Particle(IsDescription):
    bandName = StringCol(8)
    projectionRef = StringCol(512)
    geoTransformation = Int32Col(shape=6)
    rasterXSize = UInt16Col()
    rasterYSize = UInt16Col()
    rasterCount = UInt8Col()


class gdalThreadRead(threading.Thread):
    def __init__(self, index, tables):
        self._index = index
        self._tables = tables


class gdalThreadWrite(threading.Thread):
    def __init__(self, index, tables):
        self._index = index
        self._tables = tables
    
    
    def run(self):


class L3_Tables(Borg):
    def __init__(self, config, L2A_TILE_ID):
        self.config = config
        L2A_UP_MASK = '*2A_*'
        if(fnmatch.fnmatch(config.workDir, L2A_UP_MASK) == False):
            self.config.tracer.fatal('identifier "*2A_*" is missing for the Level-2A_User_Product')
            self.config.exitError()
            return False

        AUX_DATA = '/AUX_DATA'
        IMG_DATA = '/IMG_DATA'
        QI_DATA = '/QI_DATA'
        GRANULE = '/GRANULE/'

        if os.name == 'posix':
            self._DEV0 = ' > /dev/null'
        else:
            self._DEV0 = ' > NUL'

        # Resolution:
        self._resolution = int(self.config.resolution)
        if(self._resolution == 10):
            self._bandIndex = [1,2,3,7]
            self._nBands = 4
            bandDir = '/R10m'
        elif(self._resolution == 20):
            self._bandIndex = [1,2,3,4,5,6,8,11,12]
            self._nBands = 9
            bandDir = '/R20m'
        elif(self._resolution == 60):
            self._bandIndex = [0,1,2,3,4,5,6,8,9,11,12]
            self._nBands = 11
            bandDir = '/R60m'

        BANDS = bandDir
        Creation_Date = self.config.creationDate

        # generate new Tile ID:
        L3_TILE_ID = L2A_TILE_ID[:4] + 'USER' + L2A_TILE_ID[8:]
        L3_TILE_ID = L3_TILE_ID[:25] + Creation_Date + L3_TILE_ID[40:]
        L3_TILE_ID = L3_TILE_ID.replace('L2A_', 'L03_')
        self.config.L3_TILE_ID = L3_TILE_ID
        L3_TILE_ID_SHORT = '/' + L3_TILE_ID[:55]
        L2A_TILE_ID = config.workDir + GRANULE + L2A_TILE_ID
        L3_TILE_ID = config.L3_UP_DIR + GRANULE + L3_TILE_ID

        if(os.path.exists(L3_TILE_ID) == False):
            os.mkdir(L3_TILE_ID)
            os.mkdir(L3_TILE_ID + QI_DATA)

        self.config.logger.info('new working directory is: ' + L3_TILE_ID)

        filelist = sorted(os.listdir(L2A_TILE_ID))
        found = False
        for filename in filelist:
            if(fnmatch.fnmatch(filename, L2A_UP_MASK) == True):
                found = True
                break
        if found == False:
            self.config.tracer.fatal('No metadata in tile')
            self.config.exitError()

        L2A_TILE_MTD_XML = L2A_TILE_ID + '/' + filename
        L3_TILE_MTD_XML = filename
        L3_TILE_MTD_XML = L3_TILE_MTD_XML[:4] + 'USER' + L3_TILE_MTD_XML[8:]
        L3_TILE_MTD_XML = L3_TILE_MTD_XML[:25] + Creation_Date + L3_TILE_MTD_XML[40:]
        L3_TILE_MTD_XML = L3_TILE_MTD_XML.replace('L2A_', 'L03_')
        L3_TILE_MTD_XML = L3_TILE_ID + '/' + L3_TILE_MTD_XML
        copy_file(L2A_TILE_MTD_XML, L3_TILE_MTD_XML)
        config.L2A_TILE_MTD_XML = L2A_TILE_MTD_XML
        config.L3_TILE_MTD_XML = L3_TILE_MTD_XML

        #update tile and datastrip id in metadata file.
        tileId = self.config.L3_TILE_ID
        dataStrip = L3_XmlParser(config, 'DS')
        if(self._resolution == 60):
            dataStrip.root.Image_Data_Info.Tiles_Information.Tile_List.add_Tile(tileId)
            dataStrip.export()

        L2A_ImgDataDir = L2A_TILE_ID + IMG_DATA
        self._L3_ImgDataDir = L3_TILE_ID + IMG_DATA

        self._L2A_bandDir = L2A_ImgDataDir + BANDS
        self._L3_bandDir = self._L3_ImgDataDir + BANDS

        if(os.path.exists(self._L3_bandDir) == False):
            mkpath(self._L3_bandDir)

        self._L2A_QualityMasksDir = L2A_TILE_ID + QI_DATA
        self._L3_QualityDataDir = L3_TILE_ID + QI_DATA
        self._L3_AuxDataDir = L3_TILE_ID + AUX_DATA

        if(os.path.exists(self._L3_AuxDataDir) == False):
            mkpath(self._L3_AuxDataDir)
            # copy configuration to AUX dir:
            dummy, basename = os.path.split(config.L3_TILE_MTD_XML)
            fnAux = basename.replace('_MTD_', '_GIP_')
            target = self._L3_AuxDataDir + '/' + fnAux
            copy_file(config.configFn, target)

        if(os.path.exists(self._L3_QualityDataDir) == False):
            mkpath(self._L3_QualityDataDir)

        if(self.config.traceLevel == 'DEBUG'):
            self._testdir = L3_TILE_ID + '/TESTS_' + str(self._resolution) + '/'
            if(os.path.exists(self._testdir) == False):
                mkpath(self._testdir)
        #
        # the File structure:
        #-------------------------------------------------------
        pre = L3_TILE_ID_SHORT[:9]
        post = L3_TILE_ID_SHORT[13:]
        self._L3_Tile_BND_File = self._L3_bandDir + L3_TILE_ID_SHORT + '_BXX_' + str(self._resolution) + 'm.jp2'
        self._L3_Tile_CLD_File = self._L3_QualityDataDir + pre + '_CLD' + post + '_' + str(self._resolution) + 'm.jp2'
        self._L3_Tile_SNW_File = self._L3_QualityDataDir + pre + '_SNW' + post + '_' + str(self._resolution) + 'm.jp2'
        self._L3_Tile_PVI_File = self._L3_QualityDataDir + pre + '_PVI' + post + '.jp2'
        self._L3_Tile_SCL_File = self._L3_ImgDataDir     + pre + '_SCL' + post + '_' + str(self._resolution) + 'm.jp2'

        self._ImageDataBase = self._L3_bandDir + '/.database.h5'
        self._TmpFile = self._L3_bandDir + '/.tmpfile_'

        # Geodata from image metadata:
        self._cornerCoordinates = None
        self._geoTransformation = None
        self._geoExtent = None
        self._projectionRef = None

        # Band Names:
        self._bandNames = ['B01','B02','B03','B04','B05','B06','B07','B08','B8A',\
                        'B09','B10','B11','B12','DEM','SCL','SNW','CLD','AOT',\
                        'WVP','VIS','SCM','PRV','ILU','SLP','ASP','HAZ','SDW',\
                        'DDV','HCW','ELE']

        # the mapping of the channels and bands
        self._B01 = 0
        self._B02 = 1
        self._B03 = 2
        self._B04 = 3
        self._B05 = 4
        self._B06 = 5
        self._B07 = 6
        self._B08 = 7
        self._B8A = 8
        self._B09 = 9
        self._B10 = 10
        self._B11 = 11
        self._B12 = 12
        self._DEM = 13
        self._SCL = 14
        self._SNW = 15
        self._CLD = 16
        self._AOT = 17
        self._WVP = 18
        self._VIS = 19
        self._SCM = 20
        self._PRV = 21
        self._ILU = 22
        self._SLP = 23
        self._ASP = 24
        self._HAZ = 25
        self._SDW = 26
        self._DDV = 27
        self._HCW = 28
        self._ELE = 29

        self.config.tracer.debug('Module L3_Tables initialized with resolution %d' % self._resolution)

        return


    def get_corner_coordinates(self):
        return self._cornerCoordinates


    def get_geo_extent(self):
        return self._geoExtent


    def get_projection(self):
        return self._projection


    def set_corner_coordinates(self, value):
        self._cornerCoordinates = value


    def set_geo_extent(self, value):
        self._geoExtent = value


    def set_projection(self, value):
        self._projection = value


    def del_corner_coordinates(self):
        del self._cornerCoordinates


    def del_geo_extent(self):
        del self._geoExtent


    def del_projection(self):
        del self._projection


    def getBandNameFromIndex(self, index):
        return self._bandNames[index]


    def get_band_index(self):
        return self._bandIndex


    def get_n_bands(self):
        return self._nBands


    def get_db_name(self):
        return self._dbName


    def set_band_index(self, value):
        self._bandIndex = value


    def set_n_bands(self, value):
        self._nBands = value


    def set_db_name(self, value):
        self._dbName = value


    def del_band_index(self):
        del self._bandIndex


    def del_n_bands(self):
        del self._nBands


    def del_db_name(self):
        del self._dbName


        # end mapping of channels and bands

    def __exit__(self):
        sys.exit(-1)


    def __del__(self):
        self.config.tracer.debug('Module L3_Tables deleted')


    def get_config(self):
        return self._config


    def set_config(self, value):
        self._config = value


    def del_config(self):
        del self._config


    def get_b01(self):
        return self._B01


    def get_b02(self):
        return self._B02


    def get_b03(self):
        return self._B03


    def get_b04(self):
        return self._B04


    def get_b05(self):
        return self._B05


    def get_b06(self):
        return self._B06


    def get_b07(self):
        return self._B07


    def get_b08(self):
        return self._B08


    def get_b8a(self):
        return self._B8A


    def get_b09(self):
        return self._B09


    def get_b10(self):
        return self._B10


    def get_b11(self):
        return self._B11


    def get_b12(self):
        return self._B12


    def get_scl(self):
        return self._SCL


    def get_qsn(self):
        return self._SNW


    def get_qcl(self):
        return self._CLD


    def get_prv(self):
        return self._PRV


    def set_b01(self, value):
        self._B01 = value


    def set_b02(self, value):
        self._B02 = value


    def set_b03(self, value):
        self._B03 = value


    def set_b04(self, value):
        self._B04 = value


    def set_b05(self, value):
        self._B05 = value


    def set_b06(self, value):
        self._B06 = value


    def set_b07(self, value):
        self._B07 = value


    def set_b08(self, value):
        self._B08 = value


    def set_b8a(self, value):
        self._B8A = value


    def set_b09(self, value):
        self._B09 = value


    def set_b10(self, value):
        self._B10 = value


    def set_b11(self, value):
        self._B11 = value


    def set_b12(self, value):
        self._B12 = value


    def set_dem(self, value):
        self._DEM = value


    def set_scl(self, value):
        self._SCL = value


    def set_qsn(self, value):
        self._SNW = value


    def set_qcl(self, value):
        self._CLD = value


    def set_prv(self, value):
        self._PRV = value


    def del_b01(self):
        del self._B01


    def del_b02(self):
        del self._B02


    def del_b03(self):
        del self._B03


    def del_b04(self):
        del self._B04


    def del_b05(self):
        del self._B05


    def del_b06(self):
        del self._B06


    def del_b07(self):
        del self._B07


    def del_b08(self):
        del self._B08


    def del_b8a(self):
        del self._B8A


    def del_b09(self):
        del self._B09


    def del_b10(self):
        del self._B10


    def del_b11(self):
        del self._B11


    def del_b12(self):
        del self._B12


    def del_scl(self):
        del self._SCL


    def del_qsn(self):
        del self._SNW


    def del_qcl(self):
        del self._CLD


    def del_prv(self):
        del self._PRV


    B01 = property(get_b01, set_b01, del_b01, "B01's docstring")
    B02 = property(get_b02, set_b02, del_b02, "B02's docstring")
    B03 = property(get_b03, set_b03, del_b03, "B03's docstring")
    B04 = property(get_b04, set_b04, del_b04, "B04's docstring")
    B05 = property(get_b05, set_b05, del_b05, "B05's docstring")
    B06 = property(get_b06, set_b06, del_b06, "B06's docstring")
    B07 = property(get_b07, set_b07, del_b07, "B07's docstring")
    B08 = property(get_b08, set_b08, del_b08, "B08's docstring")
    B8A = property(get_b8a, set_b8a, del_b8a, "B8A's docstring")
    B09 = property(get_b09, set_b09, del_b09, "B09's docstring")
    B10 = property(get_b10, set_b10, del_b10, "B10's docstring")
    B11 = property(get_b11, set_b11, del_b11, "B11's docstring")
    B12 = property(get_b12, set_b12, del_b12, "B12's docstring")
    SCL = property(get_scl, set_scl, del_scl, "SCL's docstring")
    SNW = property(get_qsn, set_qsn, del_qsn, "SNW's docstring")
    CLD = property(get_qcl, set_qcl, del_qcl, "CLD's docstring")
    PRV = property(get_prv, set_prv, del_prv, "PRV's docstring")
    config = property(get_config, set_config, del_config, "config's docstring")
    bandIndex = property(get_band_index, set_band_index, del_band_index, "bandIndex's docstring")
    nBands = property(get_n_bands, set_n_bands, del_n_bands, "nBands's docstring")
    dbName = property(get_db_name, set_db_name, del_db_name, "dbName's docstring")
    cornerCoordinates = property(get_corner_coordinates, set_corner_coordinates, del_corner_coordinates, "cornerCoordinates's docstring")
    geoExtent = property(get_geo_extent, set_geo_extent, del_geo_extent, "geoExtent's docstring")
    projection = property(get_projection, set_projection, del_projection, "projection's docstring")

    def ReprojectCoords(self,coords,src_srs,tgt_srs):
        ''' Reproject a list of x,y coordinates.
            @type geom:     C{tuple/list}
            @param geom:    List of [[x,y],...[x,y]] coordinates
            @type src_srs:  C{osr.SpatialReference}
            @param src_srs: OSR SpatialReference object
            @type tgt_srs:  C{osr.SpatialReference}
            @param tgt_srs: OSR SpatialReference object
            @rtype:         C{tuple/list}
            @return:        List of transformed [[x,y],...[x,y]] coordinates
        '''
        trans_coords=[]
        transform = osr.CoordinateTransformation( src_srs, tgt_srs)
        for x,y in coords:
            x,y,z = transform.TransformPoint(x,y)
            trans_coords.append([x,y])
        return trans_coords


    def GetExtent(self, gt,cols,rows):
        ''' Return list of corner coordinates from a geotransform

            @type gt:   C{tuple/list}
            @param gt: geotransform
            @type cols:   C{int}
            @param cols: number of columns in the dataset
            @type rows:   C{int}
            @param rows: number of rows in the dataset
            @rtype:    C{[float,...,float]}
            @return:   coordinates of each corner
        '''
        ext=[]
        xarr=[0,cols]
        yarr=[0,rows]

        for px in xarr:
            for py in yarr:
                x=gt[0]+(px*gt[1])+(py*gt[2])
                y=gt[3]+(px*gt[4])+(py*gt[5])
                ext.append([x,y])
            yarr.reverse()
        return ext


    def J2KtoH5(self):
        # convert JPEG-2000 input files to H5 file format
        # initialize H5 database for usage:
        workDir = self._L2A_bandDir 
        os.chdir(workDir)
        database = self._ImageDataBase
        command = 'gdal_translate '
        option1 = ' -ot UInt16 -outsize '
        rasterX = None
        threads = []

        if(os.path.isfile(database)):
            os.remove(database)
            #self.config.tracer.info('database found and reused')
            #return

            self.config.tracer.info('Old database removed')
        self.config.timestamp('L3_Tables: start import')

        dirs = sorted(os.listdir(workDir))
        channels = self._bandIndex
        for i in channels:
            for filename in dirs:
                bandName = self.getBandNameFromIndex(i)
                filemask = '*_L2A_*_%3s_?0m.jp2' % bandName
                if fnmatch.fnmatch(filename, filemask):
                    if(rasterX == None):
                        # get the target resolution and metadata for the resampled bands below:
                        indataset = gdal.Open(filename, GA_ReadOnly)
                        rasterX = indataset.RasterXSize
                        rasterY = indataset.RasterYSize
                        xmlParser = L3_XmlParser(self.config, 'TILE')
                        ulx = xmlParser.root.Geometric_Info.Tile_Geocoding.Geoposition[0].ULX
                        uly = xmlParser.root.Geometric_Info.Tile_Geocoding.Geoposition[0].ULY
                        res = float32(self.config.resolution)
                        self._geoTransformation = [ulx,res,0.0,uly,0.0,-res]
                        projectionRef = indataset.GetProjectionRef()
                        extent = self.GetExtent(self._geoTransformation, rasterX, rasterY)
                        self._cornerCoordinates = asarray(extent)
                        src_srs = osr.SpatialReference()
                        src_srs.ImportFromWkt(indataset.GetProjection())
                        tgt_srs = src_srs.CloneGeogCS()
                        if(tgt_srs != None):
                            geo_extent = self.ReprojectCoords(extent,src_srs,tgt_srs)
                            self._geoExtent = asarray(geo_extent)
                            self._projectionRef = src_srs
                        indataset = None
                    
                    thread = gdalThreadRead(i, self)
                    tmpfile = self._TmpFile + '%02d.tif' % i
                    callstr = command + filename + ' ' + tmpfile + self._DEV0
                    if(subprocess.call(callstr, shell=True) != 0):
                        self.config.tracer.fatal('shell execution error using gdal_translate')
                        self.config.exitError()
                        return False

                    self.J2KtoH5_step2(i)
                    if(os.path.isfile(tmpfile)):
                        os.remove(tmpfile)
                    break

        self.config.timestamp('L3_Tables: stop import')
        return True


    def J2KtoH5_step2(self, index):
        tmpfile = self._TmpFile + '%02d.tif' % index
        bandName = self.getBandNameFromIndex(index)
        indataset = gdal.Open(tmpfile, GA_ReadOnly)
        projectionRef = indataset.GetProjectionRef()
        cols = indataset.RasterXSize
        rows = indataset.RasterYSize

        h5file = openFile(self._ImageDataBase, mode='a', title =  str(self._resolution) + 'm bands')

        if(h5file.__contains__('/tmp') == False):
            h5file.createGroup('/', 'tmp', 'temporary data')

        if(h5file.__contains__('/metadata')):
            group = h5file.root.metadata
            table = h5file.root.metadata.META
        else:
            group = h5file.createGroup('/', 'metadata', 'metadata information')
            table = h5file.createTable(group, 'META', Particle, "Meta Data")

        if(h5file.__contains__('/arrays')):
            garrays = h5file.root.arrays
        else:
            garrays = h5file.createGroup('/', 'arrays', 'band arrays')

        if(h5file.__contains__('/arrays/' + bandName)):
            self.config.tracer.error( bandName + ' already exists in database ' + self._ImageDataBase)
            h5file.close()
            indataset = None
            return
        else:
            inband = indataset.GetRasterBand(1)
            dtOut = self.setDataType(inband.DataType)
            filters = Filters(complib="zlib", complevel=1)
            eArray = h5file.createEArray(garrays, bandName, dtOut, (0,inband.XSize), bandName, filters=filters)

        for i in range(inband.YSize):
            scanline = inband.ReadAsArray(0, i, inband.XSize, 1, inband.XSize, 1)
            scanline = choose( equal( scanline, None), (scanline, None) )
            eArray.append(scanline)

        particle = table.row
        particle['bandName'] = bandName
        particle['geoTransformation'] = self._geoTransformation
        particle['projectionRef'] = projectionRef
        particle['rasterXSize'] = cols
        particle['rasterYSize'] = rows
        particle['rasterCount'] = 1
        particle.append()
        table.flush()
        h5file.close()
        indataset = None
        self.config.tracer.info(bandName + ' imported')
        self.config.timestamp('L3_Tables: band ' + bandName + ' imported')
        return


    def H5toJ2K(self):
        workDir = self._L3_bandDir
        if(os.path.exists(workDir) == False):
            self.config.tracer.fatal('missing directory %s:' % workDir)
            self.config.exitError()
            return False

        os.chdir(workDir)
        database = self._ImageDataBase
        self.config.timestamp('L3_Tables: start export')
        if(self._resolution == 10):
            bandIndex = [1,2,3,7]

        elif(self._resolution == 20):
            bandIndex = [1,2,3,4,5,6,8,11,12]

        elif(self._resolution == 60):
            bandIndex = [0,1,2,3,4,5,6,8,9,11,12]

        #prepare the xml export
        granuleType = L3_UserProduct.GranuleType500()
        granuleType.set_granuleIdentifier(self.config.L3_TILE_ID)
        granuleType.set_datastripIdentifier(self.config.L3_DS_ID)
        granuleType.set_imageFormat("JPEG2000")

        for index in bandIndex:
            tmpfile = self._TmpFile + '%02d.tif' % index
            bandName = self.getBandNameFromIndex(index)
            filename = self._L3_Tile_BND_File
            tmpfile = os.path.basename(tmpfile)
            filename = filename.replace('BXX', bandName)
            option2 = ' UInt16 '
            self.H5toJ2K_step2(index)

            if os.name == 'posix':
                callstr = 'gdal_translate -of JPEG2000 -ot' + option2 + tmpfile + ' ' + filename + self._DEV0
            else: # windows
                callstr = 'geojasper -f ' + tmpfile + ' -F ' + filename + ' -T jp2 > NUL'
            
            if(subprocess.call(callstr, shell=True) != 0):
                self.config.tracer.fatal('shell execution error using gdal_translate')
                self.config.exitError()
                return False
            if(os.path.isfile(tmpfile)):
                os.remove(tmpfile) 
            filename = os.path.basename(filename.strip('.jp2'))
            imageId = L3_UserProduct.IMAGE_IDType()
            imageId.set_valueOf_(filename)
            granuleType.add_IMAGE_ID(imageId)

            self.config.tracer.debug('Band: ' + bandName + ' converted')

        granuleList = L3_UserProduct.Granule_ListType()
        granuleList.add_Granule(granuleType)
        xmlParser = L3_XmlParser(self.config, 'UP')
        productOrganisation = xmlParser.root.General_Info.Product_Info.Product_Organisation
        productOrganisation.add_Granule_List(granuleList)
        xmlParser.export()

        # update on tile level
        xmlParser = L3_XmlParser(self.config, 'TILE')
        xmlParser.root.General_Info.TILE_ID.valueOf_ = self.config.L3_TILE_ID
        xmlParser.root.General_Info.DATASTRIP_ID.valueOf_ =self.config.L3_DS_ID

        # clean up and post processing actions:
        if(self._resolution == 60):
            self.createPreviewImage()
            self.config.timestamp('L3_Tables: preview image exported')
            '''
            qiiL3 = xmlParser.root.Quality_Indicators_Info
            qiiL3.PVI_FILENAME = os.path.basename(self._L3_Tile_PVI_File)
            qiiL3 = xmlParser.root.Quality_Indicators_Info
            qiList = L3_Tile.A_L3_Pixel_Level_QI_LIST()
            qiiL3.L3_Pixel_Level_QI = qiList
            '''
        xmlParser.export()

        if(os.path.isfile(database)):
            os.remove(database)
        globdir = self.config.L3_UP_DIR + '/GRANULE/' + self.config.L3_TILE_ID + '/*/*.jp2.aux.xml'
        for filename in glob.glob(globdir):
            os.remove(filename)
        globdir = self.config.L3_UP_DIR + '/GRANULE/' + self.config.L3_TILE_ID + '/*/*/*.jp2.aux.xml'
        for filename in glob.glob(globdir):
            os.remove(filename)

        self.config.timestamp('L3_Tables: stop export')
        return True


    def H5toJ2K_step2(self, index):
        bandName = self.getBandNameFromIndex(index)
        tmpfile = self._TmpFile + '%02d.tif' % index
        database = self._ImageDataBase

        h5file = openFile(database, mode='r')
        if(h5file.__contains__('/arrays/' +  bandName)):
            node = h5file.getNode('/arrays', bandName)
        else:
            h5file.close()
            return

        array = node.read()
        out_driver = gdal.GetDriverByName('GTiff')
        table = h5file.root.metadata.META
        for x in table.iterrows():
            if(x['bandName'] == bandName):
                rasterXSize = x['rasterXSize']
                rasterYSize = x['rasterYSize']
                rasterCount = x['rasterCount']
                break

        table.flush()
        outdataset = out_driver.Create(tmpfile, rasterXSize, rasterYSize, rasterCount, GDT_UInt16)
        gt = self._geoTransformation
        if(gt is not None):
            outdataset.SetGeoTransform(gt)
        pr = self._projectionRef
        if(pr is not None):
            outdataset.SetProjection(pr.ExportToWkt())
        outband = outdataset.GetRasterBand(1)
        outband.WriteArray(array)
        h5file.close()
        outdataset = None
        self.config.tracer.info('Band ' + bandName + ' exported')
        self.config.timestamp('L3_Tables: band ' + bandName + ' exported')
        return


    def createPreviewImage(self):
        self.config.tracer.debug('Creating Preview Image')
        workDir = self._L3_QualityDataDir
        os.chdir(workDir)

        if(self._resolution != 60):
            self.config.tracer.fatal('wrong resolution for this procedure, must be 60m')
            self.config.exitError()
            return False

        filename = self._L3_Tile_PVI_File
        tmpfile = '.tmpfile.JPEG'
        b = self.getBand(self.B02)
        g = self.getBand(self.B03)
        r = self.getBand(self.B04)

        b = self.scaleImgArray(b)
        g = self.scaleImgArray(g)
        r = self.scaleImgArray(r)

        b = Image.fromarray(b)
        g = Image.fromarray(g)
        r = Image.fromarray(r)

        out = Image.merge('RGB', (r,g,b))
        out.save(tmpfile, 'JPEG')

        if os.name == 'posix':
            callstr = 'gdal_translate -of JPEG2000 -ot Byte ' + tmpfile + ' ' + filename + self._DEV0
        else: # windows
            callstr = 'geojasper -f ' + tmpfile + ' -F ' + filename + ' -T jp2 > NUL'

        if(subprocess.call(callstr, shell=True) != 0):
            self.config.tracer.fatal('shell execution error using gdal_translate')
            self.config.exitError()
            return False

        self.config.tracer.debug('Preview Image created')
        os.remove(tmpfile)
        return True


    def scaleImgArray(self, arr):
        if(arr.ndim) != 2:
            self.config.tracer.fatal('must be a 2 dimensional array')
            self.config.exitError()
            return False

        arrclip = arr.copy()
        min = 0.0
        max = 0.125
        arr = clip(arrclip, min, max)
        scale = 255
        scaledArr = arr * scale + 0.5
        return scaledArr.astype(uint8)


    def testDb(self):
        result = False
        try:
            h5file = openFile(self._ImageDataBase, mode='r')
            h5file.getNode('/arrays', 'B02')
            status = 'Database ' + self._ImageDataBase + ' exists and can be used'
            result = True
        except:
            status = 'Database  ' + self._ImageDataBase + ' will be removed due to corruption'
            os.remove(self._ImageDataBase)
            result = False

        h5file.close()
        self.config.tracer.info(status)
        return result


    def hasBand(self, index):
        result = False
        bandName = self.getBandNameFromIndex(index)
        try:
            h5file = openFile(self._ImageDataBase, mode='r')
            h5file.getNode('/arrays', bandName)
            self.config.tracer.debug('Channel %s is present', self.getBandNameFromIndex(index))
            result = True
        except:
            self.config.tracer.debug('Channel %s is not available', self.getBandNameFromIndex(index))
            result = False

        h5file.close()
        return result


    def getBandSize(self, index):
        h5file = openFile(self._ImageDataBase, mode='r')
        bandName = self.getBandNameFromIndex(index)
        table = h5file.root.metadata.META
        rasterXSize = -1
        rasterYSize = -1
        rasterCount = 0
        for x in table.iterrows():
            if(x['bandName'] == bandName):
                nrows = x['rasterYSize']
                ncols = x['rasterXSize']
                count = x['rasterCount']
        table.flush()
        h5file.close()
        return(nrows, ncols, count)


    def getBand(self, index, dataType=uint16):
        h5file = openFile(self._ImageDataBase, mode='r')
        bandName = self.getBandNameFromIndex(index)
        node = h5file.getNode('/arrays', bandName)

        if (node.dtype != dataType):
            self.config.tracer.fatal('Wrong data type, must be: ' + str(node.dtype))
            h5file.close()
            self.config.exitError()

        nrows, ncols, count = self.getBandSize(index)
        if (count < 1):
            self.config.tracer.fatal('Insufficient band size: ' + count)
            h5file.close()
            self.config.exitError()

        array = node.read()
        h5file.close()

        return array / self.config.dnScale # scaling from 0:1


    def getDataType(self, index):
        h5file = openFile(self._ImageDataBase, mode='r')
        bandName = self.getBandNameFromIndex(index)
        node = h5file.getNode('/arrays', bandName)
        dt = node.dtype
        h5file.close()
        return(dt)


    def setBand(self, index, array):
        h5file = openFile(self._ImageDataBase, mode='a')
        bandName = self.getBandNameFromIndex(index)

        if(h5file.__contains__('/arrays/' + bandName)):
            node = h5file.getNode('/arrays', bandName)
            node.remove()

        arr = h5file.root.arrays
        dtIn = self.setDataType(array.dtype)
        filters = Filters(complib="zlib", complevel=1)
        node = h5file.createEArray(arr, bandName, dtIn, (0,array.shape[1]), bandName, filters=filters)
        self.config.tracer.debug('Channel %02d %s added to table', index, self.getBandNameFromIndex(index))
        node.append(array)

        table = h5file.root.metadata.META
        update = False
        # if row exists, change it:
        for row in table.iterrows():
            if(row['bandName'] == bandName):
                row['rasterXSize'] = array.shape[1]
                row['rasterYSize'] = array.shape[0]
                row['rasterCount'] = 1
                row.update()
                update = True
        # else append it:
        if(update == False):
            row = table.row
            row['bandName'] = bandName
            row['rasterXSize'] = array.shape[1]
            row['rasterYSize'] = array.shape[0]
            row['rasterCount'] = 1
            row.append()

        table.flush()
        h5file.close()
        return


    def removeBand(self, index):
        h5file = openFile(self._ImageDataBase, mode='a')
        bandName = self.getBandNameFromIndex(index)
        table = h5file.root.metadata.META
        if(h5file.__contains__('/arrays/' + bandName)):
            node = h5file.getNode('/arrays', bandName)
            node.remove()
            table.flush()
            self.config.tracer.debug('Channel %02d %s removed from table', index, self.getBandNameFromIndex(index))


        h5file.close()
        return


    def removeAllBands(self):
        h5file = openFile(self._ImageDataBase, mode='a')
        if(h5file.__contains__('/arrays/')):
            node = h5file.getNode('/', 'arrays')
            del node
            self.config.tracer.debug('All channels removed from table')

        h5file.close()
        self.removeAllTmpBands()
        return


    def getTmpBand(self, index, dataType=int16):
        h5file = openFile(self._ImageDataBase, mode='r')
        bandName = self.getBandNameFromIndex(index)
        node = h5file.getNode('/tmp', bandName)

        if (node.dtype != dataType):
            self.config.tracer.error('wrong data type, must be: ' + str(node.dtype))
            h5file.close()
            self.config.exitError()

        nrows, ncols, count = self.getBandSize(index)
        if (count < 1):
            self.config.tracer.error('insufficient band size: ' + count)
            h5file.close()
            self.config.exitError()

        array = node.read()
        h5file.close()
        return array


    def setTmpBand(self, index, array):
        h5file = openFile(self._ImageDataBase, mode='a')
        bandName = self.getBandNameFromIndex(index)
        table = h5file.root.metadata.META

        if(h5file.__contains__('/tmp/' + bandName)):
            node = h5file.getNode('/tmp', bandName)
            node.remove()
            table.flush()
        tmp = h5file.root.tmp
        dtIn = self.setDataType(array.dtype)
        filters = Filters(complib="zlib", complevel=1)
        node = h5file.createEArray(tmp, bandName, dtIn, (0,array.shape[1]), bandName, filters=filters)
        self.config.tracer.debug('Temporary channel ' + str(index) + ' added to table')
        node.append(array)
        table.flush()
        h5file.close()
        return


    def removeTmpBand(self, index):
        h5file = openFile(self._ImageDataBase, mode='a')
        bandName = self.getBandNameFromIndex(index)
        table = h5file.root.metadata.META

        if(h5file.__contains__('/tmp/' + bandName)):
            node = h5file.getNode('/tmp', bandName)
            node.remove()
            table.flush()
            self.config.tracer.debug('Temporary channel ' + str(index) + ' removed from table')

        h5file.close()
        return


    def removeAllTmpBands(self):
        h5file = openFile(self._ImageDataBase, mode='a')
        table = h5file.root.metadata.META
        if(h5file.__contains__('/tmp/' +'')):
            node = h5file.getNode('/tmp')
            del node
            table.flush()
            self.config.tracer.debug('All temporary channels removed from table')
        h5file.close()
        return


    def setDataType(self, dtIn):
        if(dtIn == uint8):
            dtOut = UInt8Atom()
        elif(dtIn == uint16):
            dtOut = UInt16Atom()
        elif(dtIn == int16):
            dtOut = Int16Atom()
        elif(dtIn == uint32):
            dtOut = UInt32Atom()
        elif(dtIn == int32):
            dtOut = Int32Atom()
        elif(dtIn == float32):
            dtOut = Float32Atom()
        elif(dtIn == float64):
            dtOut = Float64Atom()
        elif(dtIn == GDT_Byte):
            dtOut = UInt8Atom()
        elif(dtIn == GDT_UInt16):
            dtOut = UInt16Atom()
        elif(dtIn == GDT_Int16):
            dtOut = Int16Atom()
        elif(dtIn == GDT_UInt32):
            dtOut = UInt32Atom()
        elif(dtIn == GDT_Int32):
            dtOut = Int32Atom()
        elif(dtIn == GDT_Float32):
            dtOut = Float32Atom()
        elif(dtIn == GDT_Float64):
            dtOut = Float64Atom()

        return dtOut


    def getArray(self, filename):
        cfg = L3_Config()
        filename = self._testdir + filename + '.npy'
        if((os.path.isfile(filename)) == False):
            cfg.tracer.critical('File ' + filename + ' not present')
            return False

        return load(filename)


    def getDiffFromArrays(self, filename1, filename2):
        cfg = L3_Config()
        filename1 = self._testdir + filename1 + '.npy'
        filename2 = self._testdir + filename2 + '.npy'
        if((os.path.isfile(filename1)) == False):
            cfg.tracer.critical('File ' + filename1 + ' not present')
            return False

        if((os.path.isfile(filename2)) == False):
            cfg.tracer.critical('File ' + filename2 + ' not present')
            return False

        arr1 = load(filename1)
        arr2 = load(filename2)
        return (arr1-arr2)


    def saveArray(self, filename, arr):
        cfg = L3_Config()
        filename = self._testdir + filename + '.npy'
        save(filename, arr)

        if(os.path.exists(self._L3_bandDir) == False):
                os.makedirs(self._L3_bandDir)

        cfg.tracer.info('File ' + filename + ' saved to disk')
        return

