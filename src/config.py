import numpy as np
###########################################################################
# Do not change these variables                                           #
###########################################################################

# SECTION 0: Definitions (normally don't modify this section)
# view
PLAN_VIEW = 1
HEIGHT_SLICE = 2
SURFACE_TIME = 3
NO_PLOT = 4

# wind field
CONSTANT_WIND = 1
FLUCTUATING_WIND = 2
PREVAILING_WIND = 3

# number of stacks
ONE_STACK = 1
TWO_STACKS = 2
THREE_STACKS = 3
FOUR_STACKS = 4
FIVE_STACKS = 5
SIX_STACKS = 6
SEVEN_STACKS = 7
EIGHT_STACKS = 8
NINE_STACKS = 9
TEN_STACKS = 10

# stability of the atmosphere
CONSTANT_STABILITY = 1
ANNUAL_CYCLE = 2
stability_str = ['Very unstable', 'Moderately unstable', 'Slightly unstable', 'Neutral',
                 'Moderately stable', 'Very stable']
# Aerosol properties
HUMIDIFY = 2
DRY_AEROSOL = 1

SODIUM_CHLORIDE = 1
SULPHURIC_ACID = 2
ORGANIC_ACID = 3
AMMONIUM_NITRATE = 4
nu = [2., 2.5, 1., 2.]
rho_s = [2160., 1840., 1500., 1725.]
Ms = [58.44e-3, 98e-3, 200e-3, 80e-3]
Mw = 18e-3

dxy = 100  # resolution of the model in both x and y directions
dz = 100
x = np.mgrid[-4000:4000 + dxy:dxy]  # solve on a 4x4 km domain
y = x  # x-grid is same as y-grid

# Location of central point as Easting/Northing
UTM_easting = 480786
UTM_northing = 6216800
EPSG:2062
UTM_zone = '30V'