import datetime
import numpy as np

def boundsCheck(var,dtype):#,missingIndicator=None,lowerBound=None,upperBound=None):
    a = []

    tmp = map(float,dtype[:-1].split('.'))
    if tmp[1] == 0.:
        subtract = 0
    else:
        subtract = 1

    size = tmp[0] - tmp[1]-1
    upperBound = 10**(size-subtract)-1
    lowerBound = -1*(10**(size-subtract)-1)
    missingIndicator = lowerBound
    for i in range(len(var)):
        if (var[i] >= lowerBound and var[i] <= upperBound):
            if np.isnan(var[i]):
#                a.append(('%%%s' % (dtype.split('.')[0]+'s')) % (missingIndicator))
                a.append(('%%%s' % (dtype)) % (missingIndicator))
            else:
                a.append(('%%%s' % (dtype)) % (var[i]))
        else:
            a.append(('%%%s' % (dtype)) % (missingIndicator))
#            a.append(missingIndicator)
    return np.array(a)
                  
    

def writeSfcFile(fname,lat,lon,t,H,ustar,wstar,VPTG,PBL,SBL,L,z0,bowen,albedo,ws,wd,T,prate,rh,sfcPres,tcdc,crain,csnow):
    
    timeList = t.timeSpaceList()
    f = open('%s.SFC' % (fname),'w')
    if lat <0:
        fLat = '%.3fS' % (lat)
    else:
        fLat = '%.3fN' % (lat)

    if lon <0:
        fLon = '%.3fW' % (lon)
    else:
        fLon = '%.3fN' % (lon)

    f.write('   %s  %s          UA_ID:    99999  SF_ID:    99999  OS_ID:              VERSION: 13350  CCVR_Sub TEMP_Sub\n' % (fLat,fLon))

    HFile = boundsCheck(H,'6.1f')#,missingIndicator='-999')
    ustarFile = boundsCheck(ustar,'6.3f')#,missingIndicator='-9')
    wstarFile = boundsCheck(wstar,'6.3f')#,missingIndicator='-9')
    VPTGFile = boundsCheck(VPTG,'6.3f')#,missingIndicator='-9') 
    PBLFile = boundsCheck(PBL,'5.0f')#,missingIndicator='-999')  
    SBLFile = boundsCheck(SBL,'5.0f')#,missingIndicator='-999')  
    LFile = boundsCheck(L,'8.1f')#,missingIndicator='-99999')  
    z0File = boundsCheck(z0,'7.4f')#,missingIndicator='-9')  
    bowenFile = boundsCheck(bowen,'6.2f')#,missingIndicator='-999',lowerBound=-999.99,upperBound=999.)  
    albedoFile  = boundsCheck(albedo/100.,'6.2f')#,missingIndicator='-9')
    wsFile  = boundsCheck(ws,'7.2f')#,missingIndicator='-9999')    
    wdFile  = boundsCheck(wd,'5.0f')#,missingIndicator='-999')    
    TFile = boundsCheck(T,'6.1f')#,missingIndicator='-99')
    pamt = boundsCheck(prate,'6.2f')#,missingIndicator='-9')
    rhFile = boundsCheck(rh,'6.0f')#,missingIndicator='-999')
    sfcPresFile = boundsCheck(sfcPres/100,'6.0f')#,missingIndicator='-9999')
    #ccvr = boundsCheck(tcdc*10,'5d',missingIndicator='-999')

    for i in range(1,len(timeList)):
        if timeList[i].hour == 0:
            hour = 24
            date = timeList[i] - datetime.timedelta(hours=24)
        else:
            hour=timeList[i].hour
            date = timeList[i]

        JD = timeList[i].timetuple().tm_yday
        if crain[i]:
            ipcode = '%5s' % ('11')
        elif csnow[i]:
            ipcode = '%5s' % ('22')
        else:
            ipcode = '%5s' % ('0')

        f.write('%2d %2d %2d %3d %2d %s %s %s %s %s %s %s %s %s %s %s %s %6.1f %s %6.1f %s %s %s %s %5d      0 NAD-SFC NoSubs\n'% (date.year-2000,date.month,date.day,JD,hour,HFile[i],ustarFile[i],wstarFile[i],VPTGFile[i],PBLFile[i],SBLFile[i],LFile[i],z0File[i],bowenFile[i],albedoFile[i],wsFile[i],wdFile[i],2.,TFile[i],2.,ipcode,pamt[i],rhFile[i],sfcPresFile[i],tcdc[i]*10.))

    f.close()

def writeUpperFile(fname,lat,lon,t,Z,WD,WS,T,sigmaT,sigmaW):
    f = open('%s.PFL' % (fname),'w')
    # f.write('*    AERMET Version  13350\n')
    # f.write('*% UPPERAIR\n')
    # f.write('*      QAOUT     UPPER.OQA\n')
    # f.write('*      XDATES    %d/%d/%d TO %d/%d/%d\n' % (t.startDate.year,t.startDate.month,t.startDate.day,t.endDate.year,t.endDate.month,t.endDate.day))
    # f.write('*@     LOCATION  99999   %s   %s   %d\n' % (lon,lat,0))
    # f.write('*** EOH: END OF UPPERAIR QA HEADERS\n')
    
    time = t.timeSpaceList()[1:]
    for i in range(len(time)):
        for j in range(len(Z[0])):
            if Z[i,j] <0 or Z[i,j]>=1e4:
                pass
            else:
                if j == len(Z[0])-1:
                    top = 1
                elif Z[i,j+1] >= 1e4:
                    top=1
                else:
                    top = 0
                date = time[i]
                if date.hour == 0:
                    hour = 24
                    date = date - datetime.timedelta(hours=24)
                else:
                    hour=date.hour
                    
                f.write('%2d %2d %2d %2d %6.1f %1d %5.0f %7.2f %7.1f %6.1f %7.2f\n' % (date.year - 2000,date.month,date.day,hour,Z[i,j],top,WD[i,j],WS[i,j],T[i,j]-273.15,sigmaT[i,j],sigmaW[i,j]))
    f.close()
