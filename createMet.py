import numpy as np
from netCDF4 import Dataset
import datetime
from readConfig import *
from getData import *
from readReanalysis import *
from atmospheric import *
from skyCondition import *
from cloudTypes import *
from pwth import *
from writeToFile import *
from dateutil.relativedelta import relativedelta
import sys
# Read in information from the configuration file
lat,lon,t = readSiteConfig('met.cfg')
doSfc, SfcFname, doUpper, upperFname = readAERMODConfig('met.cfg')

if doSfc:
    # Download the appropriate met files
    downloadYears = np.arange(t.startDate.year,t.endDate.year+1,1)

    for year in downloadYears:
        downloadSfcNARR(year)

        slp     = readSfcReanalysis('prmsl','prmsl',year,lat,lon,t)
        pres    = readSfcReanalysis('pres.sfc','pres',year,lat,lon,t)
        lcb     = readSfcReanalysis('pres.lcb.gauss','pres',year,lat,lon,t)
        mcb     = readSfcReanalysis('pres.mcb.gauss','pres',year,lat,lon,t)
        hcb     = readSfcReanalysis('pres.mcb.gauss','pres',year,lat,lon,t)
        precip  = readSfcReanalysis('prate','prate',year,lat,lon,t)
        tcdc    = readSfcReanalysis('tcdc','tcdc',year,lat,lon,t)
        lcdc    = readSfcReanalysis('lcdc','lcdc',year,lat,lon,t)
        mcdc    = readSfcReanalysis('mcdc','mcdc',year,lat,lon,t)
        hcdc    = readSfcReanalysis('hcdc','hcdc',year,lat,lon,t)
        sfcTemp = readSfcReanalysis('air.sfc','air',year,lat,lon,t)
        rh      = readSfcReanalysis('rhum.2m','rhum',year,lat,lon,t)
        u       = readSfcReanalysis('uwnd.10m','uwnd',year,lat,lon,t)
        v       = readSfcReanalysis('vwnd.10m','vwnd',year,lat,lon,t)
        vis     = readSfcReanalysis('vis','vis',year,lat,lon,t)

    precip[np.where(precip < 0)] = 0.
    precip *= (1*3600)
    #precip[np.where(precip < 1e-1)]=0

    windSpeed = np.sqrt(u**2 + v**2)
    windDir   = np.arctan2(v,u) *180/np.pi
    #convert direction to degreed FROM north

    windDir = 270 - windDir
    windDir[np.where(windDir > 360.)] = windDir[np.where(windDir > 360)] - 360
    windDir[np.where(windDir < 0.)] = windDir[np.where(windDir < 0.)] + 360

    lcb = barometric(slp,lcb)
    mcb = barometric(slp,mcb)
    hcb = barometric(slp,hcb)
    wetBulb = Tw(sfcTemp - 273.15, rh)
    dewPoint = Td(sfcTemp - 273.15,rh)

    # SKY CONDITION
    # CLC = np.zeros((4,len(tcdc)))
    # CLC=np.array(CLC,dtype=str)
    # for i in range(len(tcdc)):
    #     tmp=skyCondition(lcdc[i],mcdc[i],hcdc[i])
    #     if lcdc[i] < 0.:
    #         lcdc[i] = 0.
    #     if mcdc[i] < 0.:
    #         mcdc[i] = 0.
    #     if hcdc[i] < 0.:
    #         hcdc[i] = 0.


    #     CLC[0,i]= '0%02d%02d' % (tmp[0],lcdc[i]/10.)

    #     CLC[1,i]= '0%02d%02d' % (tmp[1],mcdc[i]/10.)
    #     CLC[2,i]= '0%02d%02d' % (tmp[2],hcdc[i]/10.)
    #     CLC[3,i]= '00000'

    CLC = skyCondition(lcdc,mcdc,hcdc)


     # FIND CLOUD IDENTIFIERS

    # CLT = np.zeros((4,len(tcdc)))
    # CLT = np.array(CLT,dtype=str)

    # for i in range(len(tcdc)):
    #     tmp=cloudTypes(lcdc[i],mcdc[i],mcdc[i])
    #     if np.isnan(lcb[i]):
    #         CLT[0,i] = '09999'
    #     else:
    #         CLT[0,i] = '0%02d%02d' % (tmp[0],lcb[i]/100.)
    #     if np.isnan(mcb[i]):
    #         CLT[1,i] = '09999'
    #     else:
    #         CLT[1,i] = '0%02d%02d' % (tmp[1],mcb[i]/100.)
    #     if np.isnan(hcb[i]):
    #         CLT[2,i] = '09999'
    #     else:
    #         CLT[2,i] = '0%02d%02d' % (tmp[2],hcb[i]/100.)
    #     CLT[3,i] = '0%02d%02d' % (tmp[3],0.)

    CLT = cloudTypes(lcdc,mcdc,hcdc,lcb,mcb,hcb)

    # Let's see if we can't come up with an algorithm to predict "weather"

    # PWTH_file = np.zeros((len(precip)))
    # PWTH_file = np.array(PWTH_file,dtype='str')

    # for i in range(len(precip)):
    #     tmp = pwth(precip[i],sfcTemp[i])
    #     PWTH_file[i] = '0%02d%02d' % (tmp[0],tmp[1])
    
    weather = pwth(precip,sfcTemp)

    writeSfcFile(SfcFname,lat,lon,t,slp,pres,lcb,tcdc,lcdc,CLC,CLT,weather,vis,sfcTemp,wetBulb,dewPoint,rh,windDir,windSpeed,precip)
    end = start - time.time()




if doUpper:
    curr = t.startDate
    # Download the appropriate met files
    downloadYears = np.arange(t.startDate.year,t.endDate.year+1,1)
    
    pres    = readSfcReanalysis('pres.sfc','pres',curr.year,lat,lon,t)
    end = t.endDate
    dates = [curr]
    while curr < end:
        downloadUpperNARR(curr.year,curr.month,flag = 'nc')
        curr += relativedelta(months=1)

        f = open('%s.PFL' % (upperFname),'w')

        T = readUpperReanalysis('air','air',curr,lat,lon,t)
        f.close()
        sys.exit()
