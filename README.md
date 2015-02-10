# AERMETfromNARR
Python script to create an AERMET file from NARR data if observations are not available.

Although basic, this script will give the user a "jumping off point" for which to start an AERMOD run. An important thing to note is that AERMET is still neccesary to convert this surface observational output to an input file that AERMOD will understand.

This package has some dependencies:
     - NumPy
     - netCDF4
     - wget (Unix)
     - Datetime
     - SciPy