import numpy as np

def tke2stability(TKE):
    
    '''
    Relationship between TKE and stability class
    taken from "Assessing atmospheric stability and its impacts on
    rotor-disk wind characteristics at an onshore wind farm"
    by Sonia Wharton, and Julie K. Lundquist.

    DOI : 10.1002/we.483

    '''
    
    stability = np.zeros_like(TKE)#,dtype='|S1')

    stability[np.where(TKE < 0.4)] = 7#'G'
    stability[np.where((TKE >= 0.4) & (TKE < 0.7))] = 6#'F'
    stability[np.where((TKE >= 0.7) & (TKE < 1.0))] = 4#'D'
    stability[np.where((TKE >= 1.0) & (TKE < 1.4))] = 2#'B'
    stability[np.where(TKE >= 1.4)] = 1#'A'

    return stability
    

def tke2sigma(TKE):
    stability = tke2stability(TKE)

    sigmaTheta = np.zeros_like(TKE)
    sigmaPhi = np.zeros_like(TKE)

    sigmaTheta[np.where(stability==7)]=np.random.rand(np.shape(np.where(stability==7))[1])*2.1
    sigmaTheta[np.where(stability==6)]=np.random.rand(np.shape(np.where(stability==6))[1])*1.7 + 2.1
    sigmaTheta[np.where(stability==4)]=np.random.rand(np.shape(np.where(stability==4))[1])*5.0 + 7.5
    sigmaTheta[np.where(stability==2)]=np.random.rand(np.shape(np.where(stability==2))[1])*5 + 17.5
    sigmaTheta[np.where(stability==1)]=np.random.rand(np.shape(np.where(stability==1))[1])*337.5 + 22.5

    sigmaPhi[np.where(stability==7)]=np.random.rand(np.shape(np.where(stability==7))[1])*2.4
    sigmaPhi[np.where(stability==6)]=np.random.rand(np.shape(np.where(stability==6))[1])*2.6 + 2.4
    sigmaPhi[np.where(stability==4)]=np.random.rand(np.shape(np.where(stability==4))[1])*2.8 + 5.0
    sigmaPhi[np.where(stability==2)]=np.random.rand(np.shape(np.where(stability==2))[1])*2.0 + 10
    sigmaPhi[np.where(stability==1)]=np.random.rand(np.shape(np.where(stability==1))[1])*10 + 12

    return sigmaTheta, sigmaPhi
