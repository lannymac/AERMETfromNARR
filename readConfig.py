import ConfigParser
from reanalysisTime import *

def readSiteConfig(fname):
    Config = ConfigParser.ConfigParser()
    Config.read(fname)
    
    lat = Config.getfloat("site","latitude")
    lon = Config.getfloat("site","longitude")
    startDate = datetime.datetime.strptime(Config.get("site","startDate"), '%Y-%m-%d %H:%M:%S')
    endDate = datetime.datetime.strptime(Config.get("site","endDate"), '%Y-%m-%d %H:%M:%S')

    t = reanalysisTime(startDate,endDate)
    timeZone = Config.getint("site","timeZone")
    return lat,lon,t,timeZone


def readAERMODConfig(fname):
    Config = ConfigParser.ConfigParser()
    Config.read(fname)
    
    SfcFname = Config.get("AERMOD","SfcFname")
    doSfc = Config.getboolean("AERMOD","doSfc")

    upperFname = Config.get("AERMOD","upperFname")
    doUpper = Config.getboolean("AERMOD","doUpper")

    return doSfc, SfcFname, doUpper, upperFname

