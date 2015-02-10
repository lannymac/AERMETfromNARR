from netCDF4 import Dataset
from reanalysisTime import *
import numpy as np
import datetime
from scipy.interpolate import LinearNDInterpolator, griddata, interp1d
import sys
from cythonFunctions import bestxy
# def bestxy(emislat,emislon,lat,lon):
#    bestfit=1e20
#    for x in range(0,349):
#       for y in range(0,277):
#          thisfit = (lat[y,x]-emislat)**2 + (lon[y,x]-emislon)**2
#          if thisfit < bestfit:
#             bestfit = thisfit
#             bestx = x
#             besty = y
#    return bestx,besty

def readSfcReanalysis(fname,keyword,year,lat,lon,t):

   infile=Dataset('ncFiles/%s.%s.nc' % (fname,year),'r',format='NETCDF4')

   ncTime=infile.variables["time"][:]
   ncLat=infile.variables["lat"][:]
   ncLon=infile.variables["lon"][:]
   ncKeyword=infile.variables[keyword][:]
   infile.close()

   if ncTime[0] < 1e7:
      tWanted = t.hoursSince1800()
   else:
      tWanted = t.hoursSince0001()
      
   if len(np.shape(ncLat)) == 2:

      bestx,besty = bestxy(lat,lon,ncLat,ncLon)
      ncKeyword = ncKeyword[:,besty-1:besty+2,bestx-1:bestx+2]
      ncLat = ncLat[besty-1:besty+2,bestx-1:bestx+2]
      ncLon = ncLon[besty-1:besty+2,bestx-1:bestx+2]


      data = np.zeros_like(ncTime)

      for i in range(len(ncTime)):
         f = LinearNDInterpolator((ncLat.flatten(),ncLon.flatten()),ncKeyword[i].flatten())
         data[i] = f(lat,lon)

      f2 = interp1d(ncTime,data)

      del ncKeyword, ncTime,ncLat,ncLon
      ncKeywordFuncTime=f2(tWanted)

   else:
      lon += 360
      bestx=np.argmin(abs(ncLon - lon))
      besty=np.argmin(abs(ncLat - lat))

      ncKeyword = ncKeyword[:,besty-1:besty+2,bestx-1:bestx+2]
      ncLat = ncLat[besty-1:besty+2]
      ncLon = ncLon[bestx-1:bestx+2]

      ncLAT,ncLON = np.meshgrid(ncLat,ncLon)
      if np.any(ncKeyword.mask):
         
         data = np.zeros_like(ncTime)

         for i in range(len(ncTime)):

            if len(ncKeyword[i][~ncKeyword[i].mask])>3:

               f = LinearNDInterpolator((ncLAT[~ncKeyword[i].mask],ncLON[~ncKeyword[i].mask]),ncKeyword[i][~ncKeyword[i].mask])
               data[i] = f(lat,lon)
            else:
               data[i] = np.nan
      else:
         data = np.zeros_like(ncTime)

         for i in range(len(ncTime)):
            f = LinearNDInterpolator((ncLAT.flatten(),ncLON.flatten()),ncKeyword[i].flatten())
            data[i] = f(lat,lon)

         
      f2 = interp1d(ncTime,data)

      del ncKeyword, ncTime,ncLat,ncLon
      ncKeywordFuncTime=f2(tWanted)
   return ncKeywordFuncTime



def readUpperReanalysis(fname,keyword,curr,lat,lon,t):

   infile=Dataset('ncFiles/%s.%04d%02d.nc' % (fname,curr.year,curr.month),'r',format='NETCDF4')

   ncTime=infile.variables["time"][:]
   ncLat=infile.variables["lat"][:]
   ncLon=infile.variables["lon"][:]
   ncKeyword=infile.variables[keyword][:]
   ncLevels=infile.variables["level"][:]
   infile.close()


   if ncTime[0] < 1e7:
      tWanted = t.hoursSince1800()
   else:
      tWanted = t.hoursSince0001()
      

   bestx,besty = bestxy(lat,lon,ncLat,ncLon)
   ncKeyword = ncKeyword[:,:,besty-1:besty+2,bestx-1:bestx+2]
   ncLat = ncLat[besty-1:besty+2,bestx-1:bestx+2]
   ncLon = ncLon[besty-1:besty+2,bestx-1:bestx+2]

   
   data = np.zeros((len(ncTime),len(ncLevels)))

   for i in range(len(ncTime)):
      for j in range(len(ncLevels)):
         f = LinearNDInterpolator((ncLat.flatten(),ncLon.flatten()),ncKeyword[i,j].flatten())
         data[i,j] = f(lat,lon)

   LEVELS,TIME = np.meshgrid(ncLevels,ncTime)

   f2 = LinearNDInterpolator((LEVELS.flatten(),TIME.flatten()),data.flatten())

   LEVELS2, TWANTED = np.meshgrid(ncLevels,tWanted)

   # ncKeywordFuncTime = np.zeros((len(tWanted),len(ncLevels)))
   # for i in range(len(tWanted)):
   #    for j in range(len(ncLevels)):
   ncKeywordFuncTime = f2(LEVELS2,TWANTED)

   del ncKeyword, ncTime,ncLat,ncLon

   return ncKeywordFuncTime
