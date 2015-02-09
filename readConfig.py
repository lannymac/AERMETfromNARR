import ConfigParser
from reanalysisTime import *

def readConfig(fname):
    Config = ConfigParser.ConfigParser()
    Config.read(fname)
    
    lat = float(Config.get("site","latitude"))
    lon = float(Config.get("site","longitude"))
    startDate = datetime.datetime.strptime(Config.get("site","startDate"), '%Y-%m-%d %H:%M:%S')
    endDate = datetime.datetime.strptime(Config.get("site","endDate"), '%Y-%m-%d %H:%M:%S')

    t = reanalysisTime(startDate,endDate)

    return lat,lon,t

