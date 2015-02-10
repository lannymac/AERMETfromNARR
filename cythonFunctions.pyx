import numpy as np

def bestxy(emislat,emislon,lat,lon):
   bestfit=1e20
   l = np.shape(lat)
   for x in range(l[1]):
      for y in range(l[0]):
         thisfit = (lat[y,x]-emislat)**2 + (lon[y,x]-emislon)**2
         if thisfit < bestfit:
            bestfit = thisfit
            bestx = x
            besty = y
   return bestx,besty


def meshgridLambertConformal(arr,startDim):
   arrShape = np.shape(arr)
   dims = []
   for i in range(len(arrShape)):
      if i >= startDim:
         dims.append(np.prod(arrShape[startDim:]))
      else:
         dims.append(arrShape[i])

   arr2 = np.zeros(dims)

   for i in range(arrShape[0]):
      for j in range(arrShape[1]):
         a,a = np.meshgrid(arr[i,j],arr[i,j])
         arr2[i,j] = a

   return arr2
