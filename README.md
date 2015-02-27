# AERMETfromNARR
Python script to create an AERMET file from NARR data if observations are not available.

Although basic, this script will give the user a "jumping off point" for which to start an AERMOD run. AERMET is not neccesary to when using this script. There are still some minor issues that must be addressed.

This package has some dependencies:
     - NumPy
     - netCDF4
     - wget (Unix)
     - Datetime
     - SciPy