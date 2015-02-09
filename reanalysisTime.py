import datetime
import numpy as np

class reanalysisTime:
    def __init__(self,startDate,endDate):
        self.startDate = startDate
        self.endDate = endDate


    def hoursSince1800(self):
        # timedelta object, time since 1800
        ncepTime1800Start = self.startDate - datetime.datetime(1800,1,1) 
        ncepTime1800End   = self.endDate   - datetime.datetime(1800,1,1)

        # time since 01/01/1800 in hours
        ncepHours1800Start = ncepTime1800Start.days*24+ncepTime1800Start.seconds/3600. 
        ncepHours1800End = ncepTime1800End.days*24+ncepTime1800End.seconds/3600.

        return ncepHours1800Start,ncepHours1800End


    def hoursSince0001(self):
        # timedelta object, time since year 1
        ncepTime0001Start = self.startDate - datetime.datetime(1,1,1) 
        ncepTime0001End = self.endDate - datetime.datetime(1,1,1)

        # time since 01/01/01 in hours
        ncepHours0001Start = ncepTime0001Start.days*24+ncepTime0001Start.seconds/3600. 
        ncepHours0001End = ncepTime0001End.days*24+ncepTime0001End.seconds/3600. 

        return ncepHours0001Start,ncepHours0001End

    def timeSpaceArray(self):
        
        return np.arange(self.startDate,self.endDate,datetime.timedelta(hours=1))
