import datetime
import numpy as np
import pandas as pd
class reanalysisTime:
    def __init__(self,startDate,endDate):
        self.startDate = startDate
        self.endDate = endDate


    def hoursSince1800(self):
        # timedelta object, time since 1800
        ncepTime1800 = self.timeSpaceArray() - np.datetime64('1800-01-01')

        # time since 01/01/1800 in hours
        ncepHours1800 = ncepTime1800/1e6/3600.

        #return ncepHours1800
        return np.array(ncepHours1800,dtype=np.float64)
    


    def hoursSince0001(self):
        # timedelta object, time since 1800
        ncepTime0001 = self.timeSpaceArray() - np.datetime64('0001-01-01')

        # time since 01/01/0001 in hours
        ncepHours0001 = ncepTime0001/1e6/3600.

        #return ncepHours1800
        return np.array(ncepHours0001,dtype=np.float64)

    def timeSpaceArray(self):

        return np.arange(self.startDate,self.endDate,datetime.timedelta(hours=1))

