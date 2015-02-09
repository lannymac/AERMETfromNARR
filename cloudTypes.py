import numpy as np
def cloudTypes(lcf,mcf,hcf):
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
    clouds=np.zeros((4))
    if lcf < 50.:
        clouds[0]=11
    elif lcf >= 50.:
        clouds[0]=16

    if mcf < 50.:
        clouds[1]=23
    elif mcf >= 50.:
        clouds[1]=21


    if hcf < 50.:
        clouds[2]=32
    elif hcf >= 50.:
        clouds[2]=37

    return clouds
