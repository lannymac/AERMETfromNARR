from netCDF4 import Dataset
from reanalysisTime import *
import numpy as np
import datetime
def bestxy(emislat,emislon,lat,lon):
   bestfit=1e20
   for x in range(0,349):
      for y in range(0,277):
         thisfit = (lat[y,x]-emislat)**2 + (lon[y,x]-emislon)**2
         if thisfit < bestfit:
            bestfit = thisfit
            bestx = x
            besty = y
   return bestx,besty

def readReanalysis(fname,keyword,year,lat,lon,t):

   infile=Dataset('%s.%s.nc' % (fname,year),'r',format='NETCDF4')

   ncTime=infile.variables["time"][:]
   ncLat=infile.variables["lat"][:]
   ncLon=infile.variables["lon"][:]
   ncKeyword=infile.variables[keyword][:]
   infile.close()

   if ncTime[0] < 1e7:
      tWanted = t.hoursSince1800()
   else:
      tWanted = t.hoursSince0001()

   bestx,besty = bestxy(lat,lon,ncLat,ncLon)
   ncKeyword = ncKeyword[:,besty-1:besty+2,bestx-1:bestx+2]
   ncLat = ncLat[besty-1:besty+2,bestx-1:bestx+2]
   ncLon = ncLon[besty-1:besty+2,bestx-1:bestx+2]

   from scipy.interpolate import LinearNDInterpolator, griddata, interp1d
   data = np.zeros_like(ncTime)

   for i in range(len(ncTime)):
      f = LinearNDInterpolator((ncLat.flatten(),ncLon.flatten()),ncKeyword[i].flatten())
      data[i] = f(lat,lon)

   f2 = interp1d(ncTime,data)

   del ncKeyword, ncTime,ncLat,ncLon
   return f2(tWanted)
