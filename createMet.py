import numpy as np
from netCDF4 import Dataset
import datetime
from readConfig import readConfig
from getData import downloadNARR
from readReanalysis import readReanalysis
from atmospheric import *
import sys
# Read in information from the configuration file
lat,lon,t = readConfig('met.cfg')

# Download the appropriate met files
downloadYears = np.arange(t.startDate.year,t.endDate.year+1,1)

for year in downloadYears:
    downloadNARR(year)

    slp     = readReanalysis('prmsl','prmsl',year,lat,lon,t)
    pres    = readReanalysis('pres.sfc','pres',year,lat,lon,t)
    lcb     = readReanalysis('pres.lcb.gauss','pres',year,lat,lon,t)
    mcb     = readReanalysis('pres.mcb.gauss','pres',year,lat,lon,t)
    hcb     = readReanalysis('pres.mcb.gauss','pres',year,lat,lon,t)
    precip  = readReanalysis('prate','prate',year,lat,lon,t)
    tcdc    = readReanalysis('tcdc','tcdc',year,lat,lon,t)
    lcdc    = readReanalysis('lcdc','lcdc',year,lat,lon,t)
    mcdc    = readReanalysis('mcdc','mcdc',year,lat,lon,t)
    hcdc    = readReanalysis('hcdc','hcdc',year,lat,lon,t)
    sfcTemp = readReanalysis('air.sfc','air',year,lat,lon,t)
    rh      = readReanalysis('rhum.2m','rhum',year,lat,lon,t)
    u       = readReanalysis('uwnd.10m','uwnd',year,lat,lon,t)
    v       = readReanalysis('vwnd.10m','vwnd',year,lat,lon,t)
    vis     = readReanalysis('vis','vis',year,lat,lon,t)


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


# assume sky cover, 2//3 layers (tenths//tenths)

C2 = 99
C3=  99

# SKY CONDITION
CLC = np.zeros((4,len(tcdc)))
CLC=np.array(CLC,dtype=str)
for i in range(len(tcdc)):
   tmp=sky_condition(lcdc[i],mcdc[i],hcdc[i])
   if lcdc_file_zoom[i] < 0.:
      lcdc_file_zoom[i] = 0.
   if mcdc_file_zoom[i] < 0.:
      mcdc_file_zoom[i] = 0.
   if hcdc_file_zoom[i] < 0.:
      hcdc_file_zoom[i] = 0.


   CLC[0,i]= '0%02d%02d' % (tmp[0],lcdc[i]/10.)
   CLC[1,i]= '0%02d%02d' % (tmp[1],mcdc[i]/10.)
   CLC[2,i]= '0%02d%02d' % (tmp[2],hcdc[i]/10.)
   CLC[3,i]= '00000'



# FIND CLOUD IDENTIFIERS

CLT = np.zeros((4,len(tcdc)))
CLT = np.array(CLT,dtype=str)

for i in range(len(tcdc)):
   tmp=cloud_types(lcdc[i],mcdc[i],mcdc[i])
   CLT[0] = '0%02d%02d' % (tmp[0],lcb[i]/100.)
   CLT[1] = '0%02d%02d' % (tmp[1],mcb[i]/100.)
   CLT[2] = '0%02d%02d' % (tmp[2],hcb[i]/100.)
   CLT[3] = '0%02d%02d' % (tmp[3],0.)



# Let's see if we can't come up with an algorithm to predict "weather"

PWTH_file = np.zeros((len(precip)))
PWTH_file = np.array(PWTH_file,dtype='str')

for i in range(len(precip)):
   tmp = pwth(precip[i],sfcTemp[i])
   PWTH_file[i] = '0%02d%02d' % (tmp[0],tmp[1])
