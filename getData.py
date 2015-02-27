import os

narrURL = 'ftp://ftp.cdc.noaa.gov/Datasets/NARR'
ncepURL = 'ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis'

# def downloadSfcNARR(year,flag = 'nc'):
#     year = str(year)
#     # get the sea level pressure data
#     os.system("wget -%s %s/monolevel/prmsl.%s.nc -P ncFiles/" % (flag,narrURL,year))

#     # get the surface pressure data
#     os.system("wget -%s %s/monolevel/pres.sfc.%s.nc -P ncFiles/" % (flag,narrURL,year))

#     # get pressure at low cloud bottom
#     os.system("wget -%s %s/other_gauss/pres.lcb.gauss.%s.nc -P ncFiles/" % (flag,ncepURL,year))
#     os.system("wget -%s %s/other_gauss/pres.mcb.gauss.%s.nc -P ncFiles/" % (flag,ncepURL,year))
#     os.system("wget -%s %s/other_gauss/pres.hcb.gauss.%s.nc -P ncFiles/" % (flag,ncepURL,year))

#     # get precipitation rate
#     os.system("wget -%s %s/monolevel/prate.%s.nc -P ncFiles/" % (flag,narrURL,year))

#     # get cloud cover
#     os.system("wget -%s %s/monolevel/tcdc.%s.nc -P ncFiles/" % (flag,narrURL,year))
#     os.system("wget -%s %s/monolevel/lcdc.%s.nc -P ncFiles/" % (flag,narrURL,year))
#     os.system("wget -%s %s/monolevel/mcdc.%s.nc -P ncFiles/" % (flag,narrURL,year))
#     os.system("wget -%s %s/monolevel/hcdc.%s.nc -P ncFiles/" % (flag,narrURL,year))

#     # get surface air temperature
#     os.system("wget -%s %s/monolevel/air.sfc.%s.nc -P ncFiles/" % (flag,narrURL,year))

#     # get relative humidity
#     os.system("wget -%s %s/monolevel/rhum.2m.%s.nc -P ncFiles/" % (flag,narrURL,year))

#     # get U and V wind
#     os.system("wget -%s %s/monolevel/uwnd.10m.%s.nc -P ncFiles/" % (flag,narrURL,year))
#     os.system("wget -%s %s/monolevel/vwnd.10m.%s.nc -P ncFiles/" % (flag,narrURL,year))

#     # get visibility
#     os.system("wget -%s %s/monolevel/vis.%s.nc -P ncFiles/" % (flag,narrURL,year))


def downloadUpperNARR(year,month,flag = 'nc',fname = None):

    if fname == None:
        # get the sea level pressure data
        os.system("wget -%s %s/monolevel/pres.sfc.%s.nc -P ncFiles/" % (flag,narrURL,year))


        #os.system('wget '+cl+' '+narrurl+'pressure/air.'+yrstr+'.'+i+'.nc')
        os.system('wget -%s %s/pressure/air.%s%02d.nc -P ncFiles/' % (flag,narrURL,year,month))

        # get upper U and V wind
        os.system('wget -%s %s/pressure/uwnd.%s%02d.nc -P ncFiles/' % (flag,narrURL,year,month))
        os.system('wget -%s %s/pressure/vwnd.%s%02d.nc -P ncFiles/' % (flag,narrURL,year,month))

        # get upper specific humidity
        os.system('wget -%s %s/pressure/shum.%s%02d.nc -P ncFiles/' % (flag,narrURL,year,month))

    else:
        os.system('wget -%s %s/pressure/%s.%s%02d.nc -P ncFiles/' % (flag,narrURL,fname,year,month))

def downloadSfcNARR(year,flag = 'nc',fname = None, folder = 'monolevel',URL = narrURL):

    #if folder == 'monolevel':
    os.system("wget -%s %s/%s/%s.%s.nc -P ncFiles/" % (flag,URL,folder,fname,year))
    #elif folder == 'other_gauss':
    #    os.system("wget -%s %s/%s/%s.%s.nc -P ncFiles/" % (flag,URL,folder,fname,year))
