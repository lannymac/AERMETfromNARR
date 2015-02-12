import numpy as np
def skyCondition(lcf,mcf,hcf):
    
    '''
    THIS FUNCTION WILL RETURN SKY CONDITIONS WITH
    THE DEFINITIONS BELOW:

    -------     -----------------------------
    TD-3280     DESCRIPTION OF SKY CONDITIONS
    -------     -----------------------------
    00          clear or less that 0.1 coverage
    01          thin scattered 0.1 to 0.5 coverage
    02          scattered 0.1 to 0.5 coverage
    03          thin broken 0.6 to 0.9 coverage
    04          broken 0.6 to 0.9 coverage
    05          thin overcast 1.0 coverage
    06          overcast 1.0 coverage
    07          obscuration 1.0 coverage
    08          partial obscuration <1.0 coverage
    09          unknown
    '''
    

    lcf[np.where(lcf < 0)] = 0
    mcf[np.where(mcf < 0)] = 0
    hcf[np.where(hcf < 0)] = 0


    CLC=np.zeros((4,len(lcf)))
    
    #LOW CLOUD FRACTION 
    CLC[0,np.where(lcf < 10)] = 0
    CLC[0,np.where((lcf >= 10) & (lcf < 50))] = 2
    CLC[0,np.where((lcf >= 50) & (lcf < 90))] = 4
    CLC[0,np.where((lcf >= 90))] = 6

    # if lcf < 10.:
    #     CLC[0]=0
    # elif lcf <50:
    #     CLC[0]=2
    # elif lcf < 90:
    #     CLC[0]=4
    # #elif lcf <= 100:
    # else:
    #     CLC[0] = 6

    #MEDIUM CLOUD FRACTION 
    CLC[1,np.where(mcf < 10)] = 0
    CLC[1,np.where((mcf >= 10) & (mcf < 50))] = 2
    CLC[1,np.where((mcf >= 50) & (mcf < 90))] = 4
    CLC[1,np.where((mcf >= 90))] = 6

    # if mcf < 10.:
    #     CLC[1]=0
    # elif mcf <50:
    #     CLC[1]=2
    # elif mcf < 90:
    #     CLC[1]=4
    # #elif mcf <= 100:
    # else:
    #     CLC[1] = 6

    #HIGH CLOUD FRACTION
    CLC[2,np.where(hcf < 10)] = 0
    CLC[2,np.where((hcf >= 10) & (hcf < 50))] = 1
    CLC[2,np.where((hcf >= 50) & (hcf < 90))] = 3
    CLC[2,np.where((hcf >= 90))] = 5

    # if hcf < 10.:
    #     CLC[2]=0
    # elif hcf <50:
    #     CLC[2]=1
    # elif hcf < 90:
    #     CLC[2]=3
    # #elif hcf <= 100:
    # else:
    #     CLC[2] = 5


    CLCString = np.zeros_like(CLC,dtype=str)

    for i in range(len(lcf)):
        CLCString[0,i] = '0%02d%02d' % (CLC[0,i],lcf[i]/10.)
        CLCString[1,i] = '0%02d%02d' % (CLC[1,i],mcf[i]/10.)
        CLCString[2,i] = '0%02d%02d' % (CLC[2,i],hcf[i]/10.)
        CLCString[3,i] = '00000' 

    return CLCString
    
