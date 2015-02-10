import datetime
import numpy as np

def writeSfcFile(fname,lat,lon,t,slp,pres,lcb,tcdc, lcdc,CLC,CLT,PWTH,vis,sfcTemp,wetBulb,dewPoint,rh,windDir,windSpeed,precip):

    # assume sky cover, 2//3 layers (tenths//tenths)
    C2 = 99
    C3=  99

    f = open('%s.OQA' % (fname),'w')
    f.write('*    AERMET Version  13350\n')
    f.write('*% SURFACE\n')
    f.write('*      QAOUT     SURFACE.OQA\n')
    f.write('*      XDATES    %d/%d/%d TO %d/%d/%d\n' % (t.startDate.year,t.startDate.month,t.startDate.day,t.endDate.year,t.endDate.month,t.endDate.day))
    f.write('*@     LOCATION  99999   %s   %s   %d 0\n' % (lon,lat,0))
    f.write('*  SF     SURFACE DATA QUALITY ASSESSMENT\n')
    f.write('*** EOH: END OF SURFACE QA HEADERS\n')


    for i in range(len(slp)):
        date = t.startDate + datetime.timedelta(hours = i)
        if np.isnan(lcb[i]):
            lcb_temp = 999
        else:
            lcb_temp = lcb[i]/100.
        f.write(' %02d%02d%02d%02d %5d %5d %5d %5d %03d%02d %03d%02d %s %s %s %s\n'% (date.year-2000,date.month,date.day,date.hour,precip[i]*1000.,slp[i]/10.,pres[i]/10.,lcb_temp,tcdc[i]/10,lcdc[i]/10,C2,C3,CLC[0,i],CLC[1,i],CLC[2,i],CLC[3,i]))
        f.write('         %s %s %s %s %s %5d %5d %5d %5d %5d %5d %5d  N\n' % (CLT[0,i],CLT[1,i],CLT[2,i],CLT[3,i],PWTH[i],vis[i]/1000.*10.,(sfcTemp[i]-273.15)*10,wetBulb[i]*10.,dewPoint[i]*10.,rh[i],(windDir[i])/10.,windSpeed[i]*10))
    f.close()


def startUpperFile(fname,lat,lon,t):
    f = open('%s.OQA' % (fname),'w')
    f.write('*    AERMET Version  13350\n')
    f.write('*% UPPERAIR\n')
    f.write('*      QAOUT     UPPER.OQA\n')
    f.write('*      XDATES    %d/%d/%d TO %d/%d/%d\n' % (t.startDate.year,t.startDate.month,t.startDate.day,t.endDate.year,t.endDate.month,t.endDate.day))
    f.write('*@     LOCATION  99999   %s   %s   %d\n' % (lon,lat,0))
    f.write('*** EOH: END OF UPPERAIR QA HEADERS\n')


    return f
