import numpy as np
from netCDF4 import Dataset
import datetime
from readConfig import readConfig
from getData import downloadNARR
from readReanalysis import readReanalysis
import sys
# Read in information from the configuration file
lat,lon,t = readConfig('met.cfg')

# Download the appropriate met files
downloadYears = np.arange(t.startDate.year,t.endDate.year+1,1)

for year in downloadYears:
    downloadNARR(year)

    slp = readReanalysis('prmsl','prmsl',year,lat,lon,t)
    pres = readReanalysis('pres.sfc','pres',year,lat,lon,t)
    lcb = readReanalysis('pres.lcb.gauss','pres',year,lat,lon,t)






