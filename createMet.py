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
lat,lon,t,timeZone = readSiteConfig('met.cfg')
doSfc, SfcFname, doUpper, upperFname = readAERMODConfig('met.cfg')

if doSfc:
    # Download the appropriate met files
    # downloadYears = np.arange(t.startDate.year,t.endDate.year+1,1)

    # for year in downloadYears:
    H    = readSfcReanalysis('shtfl','shtfl',lat,lon,t,timeZone)
    PBL    = readSfcReanalysis('hpbl','hpbl',lat,lon,t,timeZone)
    latent = readSfcReanalysis('lhtfl','lhtfl',lat,lon,t,timeZone)
    B = H/latent
    albedo = readSfcReanalysis('albedo','albedo',lat,lon,t,timeZone)
    u       = readSfcReanalysis('uwnd.10m','uwnd',lat,lon,t,timeZone)
    v       = readSfcReanalysis('vwnd.10m','vwnd',lat,lon,t,timeZone)
    ws = np.sqrt(u**2+v**2)
    sfcTemp = readSfcReanalysis('air.sfc','air',lat,lon,t,timeZone)
    tcdc = readSfcReanalysis('tcdc','tcdc',lat,lon,t,timeZone)
    dswrf = readSfcReanalysis('dswrf','dswrf',lat,lon,t,timeZone)    
    pres    = readSfcReanalysis('pres.sfc','pres',lat,lon,t,timeZone)
    prate   = readSfcReanalysis('prate','prate',lat,lon,t,timeZone)*3600.
    crain = np.array(np.round(readSfcReanalysis('crain','crain',lat,lon,t,timeZone)),dtype=int)
    csnow = np.array(np.round(readSfcReanalysis('csnow','csnow',lat,lon,t,timeZone)),dtype=int)
    rh = readSfcReanalysis('rhum.2m','rhum',lat,lon,t,timeZone)
    #tcdc = readSfcReanalysis('tcdc','tcdc',lat,lon,t,timeZone)


    R = 287.058
    rho = np.ones_like(sfcTemp)
    z0 = readRoughnessLength(lat,lon,t,timeZone)
    # ustar,L = moninObukhovLength(ws,z0,rho,sfcTemp,H)
    stability = pasquilStability(ws,dswrf,tcdc)
    ustar, L, SBL = moninObukhovLength(ws,z0,rho,sfcTemp,H,stability,tcdc/100.)
    wstar = turbulentVeloctiyScale(H,rho,sfcTemp,PBL)

    T, normalPressureLevels = readUpperReanalysis('air','air',lat,lon,t,timeZone,returnLevels=True)

    PRESLEVELS,SFCPRES = np.meshgrid(normalPressureLevels,pres)
    Z = barometric(SFCPRES,PRESLEVELS*100)
    p0 = 100000. # Pa
    theta = T*(p0/pres[:,np.newaxis])**(.286) 
    VPTG = get_VPTG(PBL,theta,Z)

    windDir   = np.arctan2(v,u) *180/np.pi
    #convert direction to degreed FROM north
    windDir = 270 - windDir
    windDir[np.where(windDir > 360.)] = windDir[np.where(windDir > 360)] - 360
    windDir[np.where(windDir < 0.)] = windDir[np.where(windDir < 0.)] + 360

    writeSfcFile(SfcFname,lat,lon,t,H,ustar,wstar,VPTG,PBL,SBL,L,z0,B,albedo,ws,windDir,sfcTemp,prate,rh,pres,tcdc,crain,csnow)


if doUpper:
    
    pres    = readSfcReanalysis('pres.sfc','pres',lat,lon,t,timeZone)

    T, normalPressureLevels = readUpperReanalysis('air','air',lat,lon,t,timeZone,returnLevels=True)

    u = readSfcReanalysis('uwnd.10m','uwnd',lat,lon,t,timeZone)    
    v = readSfcReanalysis('vwnd.10m','vwnd',lat,lon,t,timeZone)    
    dswrf = readSfcReanalysis('dswrf','dswrf',lat,lon,t,timeZone)
    tcdc = readSfcReanalysis('tcdc','tcdc',lat,lon,t,timeZone)
    WS = np.sqrt(u**2+v**2)

    sigmaTheta,sigmaPhi = stability2sigma(pasquilStability(WS,dswrf,tcdc))

    V = readUpperReanalysis('vwnd','vwnd',lat,lon,t,timeZone)
    U = readUpperReanalysis('uwnd','uwnd',lat,lon,t,timeZone)

    windSpd = np.sqrt(U**2 + V**2)
    windDir = np.arctan2(V,U)*180/np.pi
    windDir = 270. - windDir
    windDir[np.where(windDir > 360.)] -= 360.
    windDir[np.where(windDir < 0.)] += 360.

    sigmaW = windSpd*np.sin(sigmaPhi[:,np.newaxis]/180*np.pi)
    
    PRESLEVELS,SFCPRES = np.meshgrid(normalPressureLevels,pres)
    Z = barometric(SFCPRES,PRESLEVELS*100)
    
    sigmaTheta = np.ones_like(T)*sigmaTheta[:,np.newaxis]
    writeUpperFile(upperFname,lat,lon,t,Z,windDir,windSpd,T,sigmaTheta,sigmaW)
