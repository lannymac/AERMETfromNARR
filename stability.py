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
    

def stability2sigma(stability):
    sigmaTheta = np.zeros_like(stability)
    sigmaPhi = np.zeros_like(stability)

    sigmaTheta[np.where(stability==6)]=np.random.rand(np.shape(np.where(stability==6))[1])*1.7 + 2.1
    sigmaTheta[np.where(stability==5)]=np.random.rand(np.shape(np.where(stability==5))[1])*3.7 + 3.8
    sigmaTheta[np.where(stability==4)]=np.random.rand(np.shape(np.where(stability==4))[1])*5 + 7.5
    sigmaTheta[np.where(stability==3)]=np.random.rand(np.shape(np.where(stability==3))[1])*5 + 12.5
    sigmaTheta[np.where(stability==2)]=np.random.rand(np.shape(np.where(stability==2))[1])*5 + 17.5
    sigmaTheta[np.where(stability==1)]=np.random.rand(np.shape(np.where(stability==1))[1])*27.5 + 22.5

    sigmaPhi[np.where(stability==6)]=np.random.rand(np.shape(np.where(stability==6))[1])*2.4
    sigmaPhi[np.where(stability==5)]=np.random.rand(np.shape(np.where(stability==5))[1])*2.6 + 2.4
    sigmaPhi[np.where(stability==4)]=np.random.rand(np.shape(np.where(stability==4))[1])*2.8 + 5.0
    sigmaPhi[np.where(stability==3)]=np.random.rand(np.shape(np.where(stability==3))[1])*2.2 + 7.8
    sigmaPhi[np.where(stability==2)]=np.random.rand(np.shape(np.where(stability==2))[1])*2 + 10
    sigmaPhi[np.where(stability==1)]=np.random.rand(np.shape(np.where(stability==1))[1])*13 + 12

    return sigmaTheta, sigmaPhi

def pasquilStability(WS,SOLAR,tcdc):
    stability = np.zeros_like(WS)
    # DAYTIME
    strongSolar = 600. # W m-2
    moderateSolar = 300. # W m-2
    slightSolar = 10. # W m-2

    stability[np.where((SOLAR >= strongSolar) & (WS < 2.))] = 1
    stability[np.where((SOLAR >= strongSolar) & (WS >= 2.) & (WS < 3))] = 1
    stability[np.where((SOLAR >= strongSolar) & (WS >= 3.) & (WS < 5))] = 2
    stability[np.where((SOLAR >= strongSolar) & (WS >= 5.) & (WS < 6))] = 3
    stability[np.where((SOLAR >= strongSolar) & (WS > 6.))] = 3

    stability[np.where((SOLAR >= moderateSolar) & (SOLAR < strongSolar) & (WS < 2.))] = 1
    stability[np.where((SOLAR >= moderateSolar) & (SOLAR < strongSolar) & (WS >= 2.) & (WS < 3))] = 2
    stability[np.where((SOLAR >= moderateSolar) & (SOLAR < strongSolar) & (WS >= 3.) & (WS < 5))] = 2
    stability[np.where((SOLAR >= moderateSolar) & (SOLAR < strongSolar) & (WS >= 5.) & (WS < 6))] = 3
    stability[np.where((SOLAR >= moderateSolar) & (SOLAR < strongSolar) & (WS > 6.))] = 4

    stability[np.where((SOLAR >= slightSolar) & (SOLAR < moderateSolar) & (WS < 2.))] = 2
    stability[np.where((SOLAR >= slightSolar) & (SOLAR < moderateSolar) & (WS >= 2.) & (WS < 3))] = 3
    stability[np.where((SOLAR >= slightSolar) & (SOLAR < moderateSolar) & (WS >= 3.) & (WS < 5))] = 3
    stability[np.where((SOLAR >= slightSolar) & (SOLAR < moderateSolar) & (WS >= 5.) & (WS < 6))] = 4
    stability[np.where((SOLAR >= slightSolar) & (SOLAR < moderateSolar) & (WS > 6.))] = 4

    

    stability[np.where((SOLAR < slightSolar) & (tcdc >= 50) & (WS < 2.))] = 5
    stability[np.where((SOLAR < slightSolar) & (tcdc >= 50) & (WS >= 2.) & (WS < 3.))] = 5
    stability[np.where((SOLAR < slightSolar) & (tcdc >= 50) & (WS >= 3.) & (WS < 5.))] = 4
    stability[np.where((SOLAR < slightSolar) & (tcdc >= 50) & (WS >= 5.) & (WS < 6.))] = 4
    stability[np.where((SOLAR < slightSolar) & (tcdc >= 50) & (WS >= 6.))] = 4

    stability[np.where((SOLAR < slightSolar) & (tcdc < 50) & (WS < 2.))] = 6
    stability[np.where((SOLAR < slightSolar) & (tcdc < 50) & (WS >= 2.) & (WS < 3.))] = 6
    stability[np.where((SOLAR < slightSolar) & (tcdc < 50) & (WS >= 3.) & (WS < 5.))] = 5
    stability[np.where((SOLAR < slightSolar) & (tcdc < 50) & (WS >= 5.) & (WS < 6.))] = 4
    stability[np.where((SOLAR < slightSolar) & (tcdc < 50) & (WS >= 6.))] = 4

    return stability
