import numpy as np
def cloudTypes(lcf,mcf,hcf,lcb,mcb,hcb),:
    '''
    THIS DEFINITION WILL ESTIMATE THE CLOUD TYPE
    DESCRIBED BELOW:

    -------     ---------------------
    TD-3280     DESCRIPTION OF CLOUDS
    -------     ---------------------
    00          none
    11          cumulus
    12          towering cumulus
    13          stratus fractus
    14          stratus cumulus lenticular
    15          stratus cumulus
    16          stratus
    17          cumulus fractus
    18          cumulonimbus
    19          cumulonimbus mammatus
    21          altostratus
    22          nimbostratus
    23          altocumulus
    24          altocumulus lenticular
    28          altocumulus castellanus
    29          altocumulus mammatus
    32          cirrus
    35          cirrocumulus lenticular
    37          cirrostratus
    39          cirrocumulus
    '''



    clouds=np.zeros((4,len(lcf)))
    
    clouds[0,np.where(lcf < 50)] = 11
    clouds[0,np.where(lcf >= 50)] = 16

    # if lcf < 50.:
    #     clouds[0]=11
    # elif lcf >= 50.:
    #     clouds[0]=16

    clouds[1,np.where(mcf < 50)] = 23
    clouds[1,np.where(mcf >= 50)] = 21

    # if mcf < 50.:
    #     clouds[1]=23
    # elif mcf >= 50.:
    #     clouds[1]=21

    clouds[2,np.where(hcf < 50)] = 32
    clouds[2,np.where(hcf >= 50)] = 37

    # if hcf < 50.:
    #     clouds[2]=32
    # elif hcf >= 50.:
    #     clouds[2]=37


    cloudsString = np.zeros_like(clouds,dtype=str)
    for i in range(len(lcf)):
        if np.isnan(lcb[i]):
            cloudsString[0,i] = '09999'
        else:
            cloudsString[0,i] = '0%02d%02d' % (clouds[0,i],lcb[i]/100.)

        if np.isnan(mcb[i]):
            cloudsString[1,i] = '09999'
        else:
            cloudsString[1,i] = '0%02d%02d' % (clouds[1,i],mcb[i]/100.)

        if np.isnan(hcb[i]):
            cloudsString[2,i] = '09999'
        else:
            cloudsString[2,i] = '0%02d%02d' % (clouds[3,i],hcb[i]/100.)
        cloudsString[3,i] = '09999'

    return cloudsString
