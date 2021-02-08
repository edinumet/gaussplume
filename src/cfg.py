
"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 5 Feb 2021 16:30 

DESCRIPTION
===========

Configures stacks in gaussian plume model
"""


import numpy as np
import math


def cfg():
    # SECTION 1: Configuration
    # Variables can be changed by the user

    dxy = 100  # resolution of the model in both x and y directions
    dz = 100
    x = np.mgrid[-4000:4000 + dxy:dxy]  # solve on a 4x4 km domain
    y = x  # x-grid is same as y-grid

    # Location of central point as Easting/Northing
    UTM_easting = 480786
    UTM_northing = 6216800
    EPSG:2062
    UTM_zone = '30V'

    stab1 = fd.stabls.index(fd.stack["stab"])  # set from 1-6
    print(stab1)

    output = fd.stack["view"]
    x_slice = 26  # position (1-50) to take the slice in the x-direction
    y_slice = 1  # position (1-50) to plot concentrations vs time

    wind = fd.stack["wvari"]
    stacks = fd.stack["nstack"]
    stack_x = [0., -100., -1000., 300,  130, 330, -1000, -1500, -2000, 2000]
    stack_y = [0., 100., 500., 300, 250, 850, -1000, 1500, 2000, 2000]

    Q = [600., 500., 600., 700, 1000, 20, 40, 50, 10, 10]  # mass emitted per unit time
    H = [80., 65., 60., 50, 15, 10, 15, 35, 10, 10]  # stack height, m
    days = 2  # run the model for n days - could be 365!

    times = np.mgrid[1:days * 24 + 1:1] / 24.

    Dy = 100.
    Dz = 100.

    # Assume CONSTANT_STABILITY for now
    stability = stab1 * np.ones((days * 24, 1))
    stability_str = cfg.stability_str[stab1 - 1]

    # decide what kind of run to do, plan view or y-z slice, or time series
    if output != "height_slice": #== cfg.PLAN_VIEW or output == cfg.SURFACE_TIME or output == cfg.NO_PLOT:
        C1 = np.zeros((len(x), len(y), days * 24))  # array to store data, initialised to be zero
        [x, y] = np.meshgrid(x, y)  # x and y defined at all positions on the grid
        z = np.zeros(np.shape(x))  # z is defined to be at ground level.
    elif output == "height_slice":
        z = np.mgrid[0:500 + cfg.dz:cfg.dz]  # z-grid
        C1 = np.zeros((len(y), len(z), days * 24))  # array to store data, initialised to be zero
        [y, z] = np.meshgrid(y, z)  # y and z defined at all positions on the grid
        x = x[x_slice] * np.ones(np.shape(y))  # x is defined to be x at x_slice
    else:
        sys.exit()

    # Set the wind based on input flags++++++++++++++++++++++++++++++++++++++++
    wind_speed = fd.stack["wind"] * np.ones((days * 24, 1))  # m/s

    if wind == fd.wvar[0]:    #cfg.CONSTANT_WIND:
        wind_dir = fd.stack["wdirn"] * np.ones((days * 24, 1))
        wind_dir_str = 'Constant wind'
    elif wind == fd.wvar[2]:   #cfg.FLUCTUATING_WIND:
        wind_dir = 360. * np.random.rand(days * 24, 1)
        wind_dir_str = 'Random wind'
    elif wind == fd.wvar[1]:   #cfg.PREVAILING_WIND:
        wind_dir = -np.sqrt(2.) * erfcinv(2. * np.random.rand(24 * days, 1)) * 2.  #         norminv(rand(days.*24,1),0,40)
        # note at this point you can add on the prevailing wind direction, i.e.
        wind_dir = wind_dir + fd.stack["wdirn"]
        wind_dir[np.where(wind_dir >= 360.)] = \
            np.mod(wind_dir[np.where(wind_dir >= 360)], 360)
        wind_dir_str = 'Prevailing wind'
    else:
        sys.exit()
