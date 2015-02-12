import numpy as np
def pwth(precip,temperature):
    '''
    THIS DEFINITION WILL TRY AND ESTIMATE CURRENT WEATHER
    ACCORDING TO THE DEFINITIONS IN AERMOD/AERMET

    THE DATA USED IS FROM THE NCEP REANALYSIS. IT IS IMPOSSIBLE TO 
    PREDICT THE PROPER CODES WITH 100% ACCURACY.

    THE PRESENT WEATHER CODES ARE AS FOLLOWS:

    TD-3280     THUNDERSTORM, TORNADO, SQUALL
    -------     -----------------------------
    10          thunderstorm - lightning and thunder
    11          severe thunderstorm - frequent intense lightning and thunder
    12          report of tornado or water spout
    13          light squall
    14          moderate squall
    15          heavy squall
    16          water spout
    17          funnel cloud
    18          tornado 
    19          unknown
    -------     --------------------------------
    TD-3280     RAIN, RAIN SHOWER, FREEZING RAIN
    -------     --------------------------------
    20          light rain
    21          moderate rain
    22          heavy rain
    23          light rain showers
    24          moderate rain showers
    25          heavy rain showers
    26          light freezing rain
    27          moderate freezing rain
    28          heavy freezing rain
    29          unkown
    -------     --------------------------------------
    TD-3280     RAIN SQUALL, DRIZZLE, FREEZING DRIZZLE
    -------     --------------------------------------
    30          light rain squalls
    31          moderate rain squalls
    32          heavy rain squalls
    33          light drizzle
    34          moderate drizzle
    35          heavy drizzle
    36          light freezing drizzle
    37          moderate freezing drizzle
    38          heavy freezing drizzle
    39          unknown
    -------     --------------------------------
    TD-3280     SNOW, SNOW PELLETS, ICE CRYSTALS
    -------     --------------------------------
    40          light snow
    41          moderate snow
    42          heavy snow
    43          light snow pellets
    44          moderate snow pellets
    45          heavy snow pellets
    46          light snow crystals
    47          moderate snow crystals
    48          heavy snow crystals
    49          unknown
    -------     ---------------------------------------
    TD-3280     SNOW SHOWERS, SNOW SQUALLS, SNOW GRAINS
    -------     ---------------------------------------
    50          light snow showers
    51          moderate snow showers
    52          heavy snow showers
    53          light snow squalls
    54          moderate snow squalls
    55          heavy snow squalls
    56          light snow grains
    57          moderate snow grains
    58          heavy snow grains
    59          unknown
    -------     -------------------------
    TD-3280     SLEET, SLEET SHOWER, HAIL
    -------     -------------------------
    60          light ice pellet showers
    61          moderate ice pellet showers
    62          heavy ice pellet showers
    63          light hail
    64          moderate hail
    65          heavy hail
    66          light small hail
    67          moderate small hail
    68          heavy small hail
    69          unknown
    -------     -------------------------------
    TD-3280     FOG, BLOWING DUST, BLOWING SAND
    -------     -------------------------------
    70          fog
    71          ice fog
    72          ground fog
    73          blowing dust
    74          blowing sand
    75          heavy fog
    76          glaze
    77          heavy ice fog
    78          heavy ground fog
    79          unknown
    -------     ----------------------------------------------
    TD-3280     SMOKE, HAZE, BLOWING SNOW, BLOWING SPRAY, DUST
    -------     ----------------------------------------------
    80          smoke
    81          haze
    82          smoke and haze
    83          dust
    84          blowing snow
    85          blowing spray
    86          dust storm
    87          --
    88          --
    89          unknown
    -------     --------------------------------------------------------------
    TD-3280     ICE PELLETS, HAIL SHOWERS, SMALL HAIL/SNOW PELLET SHOWERS, FOG
    -------     --------------------------------------------------------------
    90          light ice pellets
    91          moderate ice pellets
    92          heavy ice pellets
    93          hail showers
    94          small hail/snow pellet showers
    95          partial fog
    96          patches fog
    97          low drifting snow
    98          --
    99          unknown
    '''
    
    weather = np.zeros((2,len(precip)))

    weather[0,np.where((precip > 0.) & (precip < 2.) & (temperature > 273.15))] = 20
    weather[1,np.where((precip > 0.) & (precip < 2.) & (temperature < 273.15))] = 40


    weather[0,np.where((precip >= 2.) & (precip < 10.) & (temperature > 273.15))] = 21
    weather[1,np.where((precip >= 2.) & (precip < 10.) & (temperature < 273.15))] = 41

    weather[0,np.where((precip >= 10.) & (temperature > 273.15))] = 22
    weather[1,np.where((precip >= 10.) & (temperature < 273.15))] = 42


    # if precip > 0. and precip < 2.:
    #     if temperature >273.15:
    #         weather[0]=20
    #     else:
    #         weather[1]=40

    # elif precip >= 2. and precip < 10.:
    #     if temperature > 273.15:
    #         weather[0] = 21
    #     else:
    #         weather[1] = 41


    # elif precip >=10.:
    #     if temperature > 273.15:
    #         weather[0] = 22
    #     else:
    #         weather[1] = 42

    weatherString = np.zeros_like(precip,dtype='|S5')

    for i in range(len(precip)):
        weatherString[i]='0%02d%02d' % (weather[0,i],weather[1,i])
            

    return weatherString
