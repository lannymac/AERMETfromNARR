
def bestxy(emislat,emislon,lat,lon):
   bestfit=1e20
   for x in range(0,349):
      for y in range(0,277):
         thisfit = (lat[y,x]-emislat)**2 + (lon[y,x]-emislon)**2
         if thisfit < bestfit:
            bestfit = thisfit
            bestx = x
            besty = y
   return bestx,besty

