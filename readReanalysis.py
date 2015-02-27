from netCDF4 import Dataset
from reanalysisTime import *
import numpy as np
import datetime
from scipy.interpolate import LinearNDInterpolator, griddata, interp1d, NearestNDInterpolator
import sys
from cythonFunctions import bestxy
from getData import *
from glob import glob
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

'''
The two functions in this file are meant to read in NARR data
and linear interpolate it to the time, latitude and longitude
that we want.

I realize that this code is current very inefficient. I am working
hard to make it run much faster.
'''

def meshgridLambertConformal(arr,startDim):
   arrShape = np.shape(arr)
   dims = []
   for i in range(len(arrShape)):
      if i >= startDim:
         dims.append(np.prod(arrShape[startDim:]))
      else:
         dims.append(arrShape[i])

   arr2 = np.zeros(dims)

   if startDim == 1:
      for i in range(arrShape[0]):
         a,a = np.meshgrid(arr[i],arr[i])
         arr2[i] = a
   elif startDim == 2:
      for i in range(arrShape[0]):
         for j in range(arrShape[1]):
            a,a = np.meshgrid(arr[i,j],arr[i,j])
            arr2[i,j] = a

   return arr2


def readSfcReanalysis(fname,keyword,lat,lon,t,folder='monolevel',URL='ftp://ftp.cdc.noaa.gov/Datasets/NARR'):
   months, years = t.monthsYears(surround=True)
   years = np.unique(years)
   for k in range(len(years)):
      downloadSfcNARR(years[k],flag = 'nc',fname=fname,folder=folder,URL=URL)
      infile=Dataset('ncFiles/%s.%s.nc' % (fname,years[k]),'r',format='NETCDF4')

      ncTime=infile.variables["time"][:]
      ncLat=infile.variables["lat"][:]
      ncLon=infile.variables["lon"][:]
      ncKeyword=infile.variables[keyword][:]
      infile.close()


      if len(np.shape(ncLat)) == 2:

         bestx,besty = bestxy(lat,lon,ncLat,ncLon)
         ncKeyword = ncKeyword[:,besty-1:besty+2,bestx-1:bestx+2]
         ncLat = ncLat[besty-1:besty+2,bestx-1:bestx+2]
         ncLon = ncLon[besty-1:besty+2,bestx-1:bestx+2]


         tmpData = np.zeros_like(ncTime)
         for i in range(len(ncTime)):
            f = LinearNDInterpolator((ncLat.flatten(),ncLon.flatten()),ncKeyword[i].flatten())
            tmpData[i] = f(lat,lon)

         if k == 0:
            data = tmpData
            ncAllTimes = ncTime
         else:
            data = np.concatenate((data,tmpData))
            ncAllTimes = np.concatenate((ncAllTimes,ncTime))

      else:
         lon += 360
         bestx=np.argmin(abs(ncLon - lon))
         besty=np.argmin(abs(ncLat - lat))

         ncKeyword = ncKeyword[:,besty-1:besty+2,bestx-1:bestx+2]
         ncLat = ncLat[besty-1:besty+2]
         ncLon = ncLon[bestx-1:bestx+2]

         ncLON,ncLAT = np.meshgrid(ncLon,ncLat)
         tmpData = np.zeros_like(ncTime)
         if np.any(ncKeyword.mask):
            for i in range(len(ncTime)):
               if len(ncKeyword[i][~ncKeyword[i].mask])>3:
                  inds = ~ncKeyword[i].mask
                  f = LinearNDInterpolator((ncLAT[inds].flatten(),ncLON[inds].flatten()),ncKeyword[i][inds].flatten())
                  tmpData[i] = f(lat,lon)
#                  print f(lat,lon)
               else:
                  tmpData[i] = np.nan
         else:
            for i in range(len(ncTime)):
               f = LinearNDInterpolator((ncLAT.flatten(),ncLON.flatten()),ncKeyword[i].flatten())
               tmpData[i] = f(lat,lon)


         if k == 0:
            data = tmpData
            ncAllTimes = ncTime
         else:
            data = np.concatenate((data,tmpData))
            ncAllTimes = np.concatenate((ncAllTimes,ncTime))


   if ncTime[0] < 1e7:
      tWanted = t.hoursSince1800()
   else:
      tWanted = t.hoursSince0001()

   f2 = interp1d(ncAllTimes,data,kind='nearest')
   del ncKeyword, ncTime,ncLat,ncLon
   ncKeywordFuncTime=f2(tWanted)
   return ncKeywordFuncTime



def readUpperReanalysis(fname,keyword,lat,lon,t,returnLevels=False):
   months,years = t.monthsYears(surround=True)

   for k in range(len(months)):
      downloadUpperNARR(years[k],months[k],flag = 'nc',fname=fname)
      infile=Dataset('ncFiles/%s.%04d%02d.nc' % (fname,years[k],months[k]),'r',format='NETCDF4')
      ncTime=infile.variables["time"][:]
      ncLat=infile.variables["lat"][:]
      ncLon=infile.variables["lon"][:]
      ncKeyword=infile.variables[keyword][:]
      ncLevels=infile.variables["level"][:]
      infile.close()


   
      bestx,besty = bestxy(lat,lon,ncLat,ncLon)
      ncKeyword = ncKeyword[:,:,besty-1:besty+2,bestx-1:bestx+2]
      ncLat = ncLat[besty-1:besty+2,bestx-1:bestx+2]
      ncLon = ncLon[besty-1:besty+2,bestx-1:bestx+2]

   
      tmpData = np.zeros((len(ncTime),len(ncLevels)))

      for i in range(len(ncTime)):
         for j in range(len(ncLevels)):
            f = LinearNDInterpolator((ncLat.flatten(),ncLon.flatten()),ncKeyword[i,j].flatten())
            tmpData[i,j] = f(lat,lon)

      if k == 0:
         data = tmpData
         ncAllTimes = ncTime
      else:
         data = np.concatenate((data,tmpData))
         ncAllTimes = np.concatenate((ncAllTimes,ncTime))

   if ncAllTimes[0] < 1e7:
      tWanted = t.hoursSince1800()
   else:
      tWanted = t.hoursSince0001()

   LEVELS,TIME = np.meshgrid(ncLevels,ncAllTimes)
   f2 = LinearNDInterpolator((LEVELS.flatten(),TIME.flatten()),data.flatten())

   LEVELS2, TWANTED = np.meshgrid(ncLevels,tWanted)
   ncKeywordFuncTime = f2(LEVELS2,TWANTED)

   del ncKeyword, ncTime,ncLat,ncLon
   if returnLevels:
      return ncKeywordFuncTime,ncLevels
   else:
      return ncKeywordFuncTime


def readRoughnessLength(lat,lon,t):
   files = glob('ncFiles/z0/*.nc')
   lon += 360
   for i in range(len(files)):
      
      infile=Dataset('%s' % files[i],'r',format='NETCDF4')
      ncLat=infile.variables["lat"][:]
      ncLon=infile.variables["lon"][:]
      ncZ0=infile.variables['SFC_R_L1'][:]

      ncTime = infile.variables['valid_date_time'][:]
      ncLAT,ncLON = np.meshgrid(ncLat,ncLon)
      if i == 0:
         dt=[]
         z0 = []
      for j in range(len(ncTime)):
         month = int(ncTime[j][4]+ncTime[j][5])
         dt.append(month)
         f = LinearNDInterpolator((ncLAT.flatten(),ncLON.flatten()),ncZ0[j].flatten())
         z0.append(f(lat,lon))
      
      infile.close()
   z0 = np.array(z0)
   dt = np.array(dt)   
   tWanted = t.timeSpaceList()
   tMonths = np.zeros((len(tWanted)))
   for i in range(len(tWanted)):
      tMonths[i] = tWanted[i].month
   z0ByMonth = np.zeros((len(tWanted)))
   for i in range(0,12):
      z0ByMonth[np.where(tMonths== i+1)] = np.mean(z0[np.where(dt == i+1)])
      
   return z0ByMonth
