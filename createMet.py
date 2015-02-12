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
from stability import *
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

    CLC = skyCondition(lcdc,mcdc,hcdc)
    CLT = cloudTypes(lcdc,mcdc,hcdc,lcb,mcb,hcb)
    weather = pwth(precip,sfcTemp)

    writeSfcFile(SfcFname,lat,lon,t,slp,pres,lcb,tcdc,lcdc,CLC,CLT,weather,vis,sfcTemp,wetBulb,dewPoint,rh,windDir,windSpeed,precip)



if doUpper:
    
    pres    = readSfcReanalysis('pres.sfc','pres',t.startDate.year,lat,lon,t)

    T, normalPressureLevels = readUpperReanalysis('air','air',lat,lon,t,returnLevels=True)
    TKE, tkePressureLevels = readUpperReanalysis('tke','tke',lat,lon,t,returnLevels=True)
    tmpSigmaTheta,tmpSigmaPhi = tke2sigma(TKE)
    sigmaTheta = np.ones(np.shape(T))*tmpSigmaTheta[:,-1][:,None]
    sigmaTheta[:,0:15] = tmpSigmaTheta

    sigmaPhi = np.ones(np.shape(T))*tmpSigmaPhi[:,-1][:,None]
    sigmaPhi[:,0:15] = tmpSigmaPhi


    V = readUpperReanalysis('vwnd','vwnd',lat,lon,t)
    U = readUpperReanalysis('uwnd','uwnd',lat,lon,t)

    windSpd = np.sqrt(U**2 + V**2)
    windDir = np.arctan2(V,U)*180/np.pi
    windDir = 270. - windDir
    windDir[np.where(windDir > 360.)] -= 360.
    windDir[np.where(windDir < 0.)] += 360.

    sigmaW = windSpd*np.sin(sigmaPhi/180*np.pi)
    
    PRESLEVELS,SFCPRES = np.meshgrid(normalPressureLevels,pres)
    Z = barometric(SFCPRES,PRESLEVELS*100)
    
    writeUpperFile(upperFname,lat,lon,t,Z,windDir,windSpd,T,sigmaTheta,sigmaW)
