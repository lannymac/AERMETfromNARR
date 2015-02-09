import os

narrURL = 'ftp://ftp.cdc.noaa.gov/Datasets/NARR'
ncepURL = 'ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis'

def downloadNARR(year,flag = 'nc'):
    year = str(year)
    # get the sea level pressure data
    os.system("wget -%s %s/monolevel/prmsl.%s.nc" % (flag,narrURL,year))

    # get the surface pressure data
    os.system("wget -%s %s/monolevel/pres.sfc.%s.nc" % (flag,narrURL,year))

    # get pressure at low cloud bottom
    os.system("wget -%s %s/other_gauss/pres.lcb.gauss.%s.nc" % (flag,ncepURL,year))
    os.system("wget -%s %s/other_gauss/pres.mcb.gauss.%s.nc" % (flag,ncepURL,year))
    os.system("wget -%s %s/other_gauss/pres.hcb.gauss.%s.nc" % (flag,ncepURL,year))

    # get precipitation rate
    os.system("wget -%s %s/monolevel/prate.%s.nc" % (flag,narrURL,year))

    # get cloud cover
    os.system("wget -%s %s/monolevel/tcdc.%s.nc" % (flag,narrURL,year))
    os.system("wget -%s %s/monolevel/lcdc.%s.nc" % (flag,narrURL,year))
    os.system("wget -%s %s/monolevel/mcdc.%s.nc" % (flag,narrURL,year))
    os.system("wget -%s %s/monolevel/hcdc.%s.nc" % (flag,narrURL,year))

    # get surface air temperature
    os.system("wget -%s %s/monolevel/air.sfc.%s.nc" % (flag,narrURL,year))

    # get relative humidity
    os.system("wget -%s %s/monolevel/rhum.2m.%s.nc" % (flag,narrURL,year))

    # get U and V wind
    os.system("wget -%s %s/monolevel/uwnd.10m.%s.nc" % (flag,narrURL,year))
    os.system("wget -%s %s/monolevel/vwnd.10m.%s.nc" % (flag,narrURL,year))

    # get visibility
    os.system("wget -%s %s/monolevel/vis.%s.nc" % (flag,narrURL,year))
