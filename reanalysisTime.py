import datetime
import numpy as np
import pandas as pd
   
from dateutil.relativedelta import relativedelta
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

        return np.arange(self.startDate,self.endDate+datetime.timedelta(hours=1),datetime.timedelta(hours=1))


    def timeSpaceList(self):
        curr =  self.startDate
        l= [curr]
        i=0
        while curr < self.endDate:
            curr = curr + datetime.timedelta(hours=1)
            l.append(curr)
        return l


    def monthsYears(self,surround=False):
        times = self.timeSpaceList()
        months = [times[0].month]
        years = [times[0].year]        
        for i in range(1,len(times)):

            if months[-1] == times[i].month:
                pass
            else:
                months.append(times[i].month)
                years.append(times[i].year)
        if surround:

            months.insert(0,(times[0]-relativedelta(months=1)).month)
            years.insert(0,(times[0]-relativedelta(months=1)).year)

            months.append((times[-1]+relativedelta(months=1)).month)
            years.append((times[-1]+relativedelta(months=1)).year)
        return months,years
        
