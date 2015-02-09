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

#def readReanalysis(keyword,year,lat,lon,t):
keyword = "prmsl"
year = 2013
lat = 40.587773
lon = -105.147914
startDate = datetime.datetime(2013, 1, 1, 0, 0)
endDate = datetime.datetime(2013, 1, 31, 23, 0)
t = reanalysisTime(startDate,endDate)
infile=Dataset('%s.%s.nc' % (keyword,year),'r',format='NETCDF4')

ncTime=infile.variables["time"][:]
ncLat=infile.variables["lat"][:]
ncLon=infile.variables["lon"][:]
ncKeyword=infile.variables[keyword][:]
infile.close()

bestx,besty = bestxy(lat,lon,ncLat,ncLon)
ncKeyword = ncKeyword[:,besty-1:besty+2,bestx-1:bestx+2]
ncLat = ncLat[besty-1:besty+2,bestx-1:bestx+2]
ncLon = ncLon[besty-1:besty+2,bestx-1:bestx+2]

from scipy.interpolate import LinearNDInterpolator, griddata

xi = np.linspace(ncLon.min(),ncLon.max(),3)
yi = np.linspace(ncLat.min(),ncLat.max(),3)

zi = griddata((ncTime,ncLat.flatten(),ncLon.flatten()),ncKeyword.flatten(),(ncTime,yi,xi))
#f = LinearNDInterpolator((ncTime.flatten(),ncLat.flatten(),ncLon.flatten()),ncKeyword)
