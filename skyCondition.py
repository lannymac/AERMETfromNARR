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
    

    CLC=np.zeros((4))
    
    #LOW CLOUD FRACTION 
    if lcf < 10.:
        CLC[0]=0
    elif lcf <50:
        CLC[0]=2
    elif lcf < 90:
        CLC[0]=4
    #elif lcf <= 100:
    else:
        CLC[0] = 6

    #MEDIUM CLOUD FRACTION 
    if mcf < 10.:
        CLC[1]=0
    elif mcf <50:
        CLC[1]=2
    elif mcf < 90:
        CLC[1]=4
    #elif mcf <= 100:
    else:
        CLC[1] = 6

    #HIGH CLOUD FRACTION
    if hcf < 10.:
        CLC[2]=0
    elif hcf <50:
        CLC[2]=1
    elif hcf < 90:
        CLC[2]=3
    #elif hcf <= 100:
    else:
        CLC[2] = 5

    return CLC
    
