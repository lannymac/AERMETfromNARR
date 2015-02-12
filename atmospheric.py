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


