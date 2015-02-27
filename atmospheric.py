import numpy as np

def barometric(p0,pz):
   H = 7400. #m
   return -np.log(pz/p0)*H


def Td(T,RH):
   A1= 17.625
   B1=243.04

   numerator = B1 * (np.log(RH/100.) + (A1*T)/(B1+T))
   denominator = A1 - np.log(RH/100.) - (A1*T)/(B1+T)

   return numerator/denominator

def Tw(T,RH):
   # Taken from Stull et al. (2011), Journal of Applied Meteorology and climatology
   # T has units of degrees celcius
   # RH has units of %
   a= T * np.arctan(0.151977 * np.sqrt(RH + 8.313659))
   b = np.arctan(T + RH)
   c = -np.arctan(RH - 1.676331)
   d = 0.00391838 * (RH**(3/2.)) * np.arctan(0.023101*RH)
   e = -4.686035

   return a+b+c+d+e

def murphy(T):
   A=54.842763 - 6763.22/T - 4.210*np.log(T)+.000367*T
   B=np.tanh(.0415*(T-218.8))*(53.878 - 1331.22/T - 9.44526*np.log(T)+.014025*T)
   return np.exp(A+B)

def sh2rh(SH,T,pLevels):
   w = SH/(1-SH)
   e = w*pLevels/(w+0.622)
   es = murphy(T)
   RH= e/es*100
   return RH 


def phi_zref(zref,L):
   mu = (1.-16.*zref/L)**(1/4.)
   return 2*np.log((1+mu)/2.) + np.log((1+mu**2)/2) - 2*np.arctan(mu) + np.pi/2

def phi_z0(z0,L):
   mu = (1.-16.*z0/L)**(1/4.)
   return 2*np.log((1+mu)/2.) + np.log((1+mu**2)/2) - 2*np.arctan(mu) + np.pi/2

def moninObukhovLength(u,z0,rho,T,H,stability,n,zref = 2.):
   ustarAll = np.zeros_like(u,dtype=float)
   LAll = np.zeros_like(u,dtype=float)
   SBL = np.zeros_like(u,dtype=float)
   k = 0.4
   g = 9.81
   cp = 1005.
   betaM = 4.7
   for i in range(len(u)):
      if stability[i] < 4:
         L= [1e0,-1000]
         iterations = 0
         while abs(L[0]-L[1])>.0000001:
            L[0] = L[1]
            ustar = k*u[i]/(np.log(zref/z0[i]) - phi_zref(zref,L[0]) + phi_z0(z0[i],L[0]))
            L[1] = -rho[i]*cp*T[i]*(ustar**3)/(k*g*H[i])
            iterations+=1

         ustarAll[i] = ustar
         LAll[i] = L[0]
         SBL[i] = 2300.*(ustarAll[i]**(3/2.))
      else:
         C_D = k/(np.log(zref/z0[i]))
         thetastar = 0.09*(1 - 0.5*n[i]**2)
         u0 = np.sqrt(betaM*zref*g*thetastar/T[i])
         ustarAll[i] = C_D*u[i]/2.*(1.+np.sqrt(1. - (2*u0/(np.sqrt(C_D)*u[i]))**2))
         LAll[i]= -rho[i]*cp*T[i]*(ustarAll[i]**3)/(k*g*H[i])
         SBL[i] = 2300.*(ustarAll[i]**(3/2.))
   return ustarAll,LAll, SBL

def turbulentVeloctiyScale(H,rho,T):
   g = 9.81
   cp = 1005.
   zic = 4000.
   return (g*H*zic/(rho*cp*T))**(1/3.)

def get_VPTG(PBL,theta,Z):
   VPTG = np.zeros_like(PBL)
   for i in range(len(PBL)):
      inds = np.where(Z[i]>PBL[i])[0]
      Znew = Z[i,inds]
      thetaNew = theta[i,inds]
      
      dtdz = (thetaNew[:-1] - thetaNew[1:])/(Znew[:-1] - Znew[1:])
      VPTG[i] = dtdz.mean()

   return VPTG
