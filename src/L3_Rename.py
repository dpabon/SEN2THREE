'''
Created on Feb 10, 2015

@author: umwilm
'''
import sys, os, fnmatch




def stdoutWrite(s):
    sys.stdout.write(s)
    sys.stdout.flush()
    
def stderrWrite(s):
    sys.stderr.write(s)
    sys.stderr.flush() 

def changeTimeAndDate(parentDir, ID, fn, monthFmt):
    if 'A$$' in ID:
        ID  = ID[:56] + fn[56:]
    elif 'B$$' in ID:
        ID = ID[:56] + fn[60:]
            
    fOld = parentDir + '/' + fn
    
    fNew = ID.replace('XX','14')
    fNew = fNew.replace('YY', monthFmt)
    fNew = parentDir + '/' + fNew
    #print fOld
    #print fNew
    os.rename(fOld, fNew)
    return fNew

def main(args):
    
    if os.path.exists(args.directory) == False:
        stderrWrite('directory "%s" does not exist\n.' % args.directory)
        sys.exit(-1)

    PRODUCT_ID =    'S2A_USER_PRD_MSIL2A_MPS__20150621T120000_R0YY_V20XXYY01T000000_20XXYY28T235959'
    DATASTRIP_ID =  'S2A_USER_MSI_L2A_DS_MPS__20150621T120000_S20XXYY01T000000_N01.01'
    TILE_ID =       'S2A_USER_MSI_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ_N01.01'
    PRODUCT_MTD =   'S2A_USER_MTD_MSIL2A_MPS__20150621T120000_R0YY_V20XXYY01T000000_20XXYY28T235959.xml'
    DATASTRIP_MTD = 'S2A_USER_MTD_L2A_DS_MPS__20150621T120000_S20XXYY01T000000.xml'
    TILE_MTD =      'S2A_USER_MSI_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ.xml'
    GIP_MTD =       'S2A_USER_GIP_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ.xml'
    TRACE_MTD =     'S2A_USER_MTD_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ_Trace.xml'        
    REPORT_MTD =    'S2A_USER_MTD_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ_Report.xml' 
        
    IMG_MSI = 'S2A_USER_MSI_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ_A$$'
    IMG_SCL = 'S2A_USER_SCL_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ_A$$'
    IMG_CLD = 'S2A_USER_CLD_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ_A$$'
    IMG_SNW = 'S2A_USER_SNW_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ_A$$'
    IMG_DEM = 'S2A_USER_DEM_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ_A$$'
    IMG_PVI = 'S2A_USER_PVI_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ.A$$'
    IMG_AOT = 'S2A_USER_AOT_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ_B$$'
    IMG_WVP = 'S2A_USER_WVP_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ_B$$'
    IMG_VIS = 'S2A_USER_VIS_L2A_TL_MPS__20XXYY15T120000_A0000YY_T14RMQ_B$$'


    USR_MSK = 'S2A_USER_PRD_*'
    DIR_MSK = 'S2A_*.01'
    MTD_MSK = 'S2A_*.xml'
    IMG_MSK = 'S2A_*.jp2'
    
    workDir = args.directory
    stdoutWrite('\nApplication started ...\n')    
    month = 0
    products = sorted(os.listdir(workDir))
    for f in products:
        if(fnmatch.fnmatch(f, USR_MSK) == False):
            continue
        
        L2A_UP_ID = workDir + '/' + f
        month += 1
        monthFmt = format('%02d' % month)
        files = sorted(os.listdir(L2A_UP_ID))
        for f in files:
            if(fnmatch.fnmatch(f, MTD_MSK) == False):     
                continue
            changeTimeAndDate(L2A_UP_ID, PRODUCT_MTD, f, monthFmt)
            break
        
        DATASTRIP = L2A_UP_ID + '/DATASTRIP'
        files = sorted(os.listdir(DATASTRIP))
        for f in files:        
            if(fnmatch.fnmatch(f, DIR_MSK) == False):
                continue
            DATASTRIP_NEW = changeTimeAndDate(DATASTRIP, DATASTRIP_ID, f, monthFmt)
            files = sorted(os.listdir(DATASTRIP_NEW))
            for f in files:        
                if(fnmatch.fnmatch(f, MTD_MSK) == False):
                    continue
                changeTimeAndDate(DATASTRIP_NEW, DATASTRIP_MTD, f, monthFmt)
                break
            break

        GRANULE = L2A_UP_ID + '/GRANULE'
        files = sorted(os.listdir(GRANULE))
        for f in files:        
            if(fnmatch.fnmatch(f, DIR_MSK) == False):
                continue
            TILE_ID_NEW = changeTimeAndDate(GRANULE, TILE_ID, f, monthFmt)
            #TILE_ID_NEW = GRANULE + '/' + f
            files = sorted(os.listdir(TILE_ID_NEW))
            for f in files:
                if(fnmatch.fnmatch(f, MTD_MSK) == False):
                    continue            
                changeTimeAndDate(TILE_ID_NEW, TILE_MTD, f, monthFmt)
                break                  

            AUX_DATA = TILE_ID_NEW + '/AUX_DATA'
            files = sorted(os.listdir(AUX_DATA))
            for f in files:
                if(fnmatch.fnmatch(f, IMG_MSK) == True):         
                    changeTimeAndDate(AUX_DATA, IMG_DEM, f, monthFmt)
                elif(fnmatch.fnmatch(f, MTD_MSK) == True):
                    changeTimeAndDate(AUX_DATA, GIP_MTD, f, monthFmt)                   
                else:
                    continue

            SCL_MSK = '*_SCL_*'
            IMG_DATA = TILE_ID_NEW + '/IMG_DATA'
            files = sorted(os.listdir(IMG_DATA))
            for f in files:
                if(fnmatch.fnmatch(f, SCL_MSK) == False):
                    continue
                changeTimeAndDate(IMG_DATA, IMG_SCL, f, monthFmt)

            AOT_MSK = '*_AOT_*'
            WVP_MSK = '*_WVP_*'
            VIS_MSK = '*_VIS_*'
            R20 = IMG_DATA + '/R20m'
            files = sorted(os.listdir(R20))
            for f in files:
                if(fnmatch.fnmatch(f, IMG_MSK) == False):
                    continue
                if(fnmatch.fnmatch(f, AOT_MSK) == True):
                    changeTimeAndDate(R20, IMG_AOT, f, monthFmt) 
                elif(fnmatch.fnmatch(f, WVP_MSK) == True):
                    changeTimeAndDate(R20, IMG_WVP, f, monthFmt) 
                elif(fnmatch.fnmatch(f, VIS_MSK) == True):
                    changeTimeAndDate(R20, IMG_VIS, f, monthFmt) 
                else:
                    changeTimeAndDate(R20, IMG_MSI, f, monthFmt)           

            R60 = IMG_DATA + '/R60m'
            files = sorted(os.listdir(R60))
            for f in files:
                if(fnmatch.fnmatch(f, IMG_MSK) == False):
                    continue
                if(fnmatch.fnmatch(f, AOT_MSK) == True):
                    changeTimeAndDate(R60, IMG_AOT, f, monthFmt) 
                elif(fnmatch.fnmatch(f, WVP_MSK) == True):
                    changeTimeAndDate(R60, IMG_WVP, f, monthFmt) 
                elif(fnmatch.fnmatch(f, VIS_MSK) == True):
                    changeTimeAndDate(R60, IMG_VIS, f, monthFmt) 
                else:
                    changeTimeAndDate(R60, IMG_MSI, f, monthFmt) 
                 
            CLD_MSK = '*_CLD_*'
            SNW_MSK = '*_SNW_*'
            PVI_MSK = '*_PVI_*'
            TRC_MSK = '*_Trace.xml'
            RPT_MSK = '*_Report.xml'
            QI_DATA = TILE_ID_NEW + '/QI_DATA'
            files = sorted(os.listdir(QI_DATA))
            for f in files:
                if(fnmatch.fnmatch(f, TRC_MSK) == True):
                    changeTimeAndDate(QI_DATA, TRACE_MTD, f, monthFmt)
                elif(fnmatch.fnmatch(f, RPT_MSK) == True):
                    changeTimeAndDate(QI_DATA, REPORT_MTD, f, monthFmt)
                elif(fnmatch.fnmatch(f, PVI_MSK) == True):
                    changeTimeAndDate(QI_DATA, IMG_PVI, f, monthFmt)                     
                elif(fnmatch.fnmatch(f, CLD_MSK) == True):
                    changeTimeAndDate(QI_DATA, IMG_CLD, f, monthFmt)           
                elif(fnmatch.fnmatch(f, SNW_MSK) == True):
                    changeTimeAndDate(QI_DATA, IMG_SNW, f, monthFmt)                    
                else:
                    continue           
    
    stdoutWrite('\nApplication terminated successfully.\n')
    return True

if __name__ == "__main__":
    # Someone is launching this directly
    import argparse
    descr = ''
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('directory', help='Directory where the Level-2A input files are located')
    args = parser.parse_args()
    main(args)
