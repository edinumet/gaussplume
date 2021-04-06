
"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 02 April 2021 14:04 

DESCRIPTION
===========

Configures stacks in gaussian plume model
"""

import numpy as np

class cfg():
    def __init__(self,stack,stabls,wvar):
        # SECTION 1: Configuration
        # Variables can be changed by the user
        self.stack = stack
        self.stabls = stabls
        self.wvar = wvar
        
        self.dxy = 50  # resolution of the model in both x and y directions
        self.dz = 50
        self.x = np.mgrid[-4000:4000 + self.dxy:self.dxy]  # solve on a 4x4 km domain
        self.y = self.x  # x-grid is same as y-grid

        # Location of central point as UTM Easting/Northing
        self.UTM_easting = 480786
        self.UTM_northing = 6216800
        self.EPSG:2062
        self.UTM_zone = '30V'

        self.stab1 = self.stabls.index(self.stack["stab"])  # set from 1-6

        self.output = self.stack["view"]
        self.x_slice = 26  # position (1-50) to take the slice in the x-direction
        self.y_slice = 1  # position (1-50) to plot concentrations vs time

        self.wind = self.stack["wvari"]
        #self.stack["nstack"] = self.stack["ntstack"]+self.stack["nsstack"]
        self.stacks = self.stack["nstack"]
        print(self.stack["nstack"])
     
        #       [600., 500., 600., 700, 1000, 20, 40, 50, 10, 10]  # mass emitted per unit time
        if self.stack["ntstack"]==1:
            self.stack_x = [0., -50., 0., 50]
            self.stack_y = [0., 50., 0., -50]
            self.Q = [self.stack["tstrength"], self.stack["sstrength"], 
                  self.stack["sstrength"], self.stack["sstrength"]]  #  assume just 1 stack for now 
            self.H = [self.stack["fheight"], 5, 5, 5]  # assume just 1 stack for now
        else:
            self.stack_x = [-50., 0., 50]
            self.stack_y = [50., 0., -50]
            self.Q = [self.stack["sstrength"],self.stack["sstrength"], self.stack["sstrength"]]  #  assume just 1 stack for now 
            self.H = [5, 5, 5]
        #        [80., 65., 60., 50, 15, 10, 15, 35, 10, 10]  # stack height, m
        self.hours = 1  # run the model for n days - could be 365!

        self.times = np.mgrid[1:self.hours * 24 + 1:1] / 24.

        self.Dy = 50.
        self.Dz = 50.

        # Assume CONSTANT_STABILITY for now
        self.stability = self.stab1 * np.ones((self.hours, 1))
        #stability_str = cfg.stability_str[stab1 - 1]

        # decide what kind of run to do, plan view or y-z slice, or time series
        if self.output != "height_slice": #== cfg.PLAN_VIEW or output == cfg.SURFACE_TIME or output == cfg.NO_PLOT:
            self.C1 = np.zeros((len(self.x), len(self.y), self.hours))  # array to store data, initialised to be zero
            [self.x, self.y] = np.meshgrid(self.x, self.y)  # x and y defined at all positions on the grid
            self.z = np.zeros(np.shape(self.x))  # z is defined to be at ground level.
        elif self.output == "height_slice":
            self.z = np.mgrid[0:500 + self.dz:self.dz]  # z-grid
            self.C1 = np.zeros((len(self.y), len(self.z), self.hours))  # array to store data, initialised to be zero
            [self.y, self.z] = np.meshgrid(self.y, self.z)  # y and z defined at all positions on the grid
            self.x = self.x[self.x_slice] * np.ones(np.shape(self.y))  # x is defined to be x at x_slice
        else:
            sys.exit()

        # Set the wind based on input flags++++++++++++++++++++++++++++++++++++++++
        self.wind_speed = self.stack["fwind"] * np.ones((self.hours, 1))  # m/s

        if self.wind == self.wvar[0]:    #cfg.CONSTANT_WIND:
            self.wind_dir = self.stack["wdirn"] * np.ones((self.hours, 1))
            self.wind_dir_str = 'Constant wind'
        elif self.wind == self.wvar[2]:   #cfg.FLUCTUATING_WIND:
            self.wind_dir = 360. * np.random.rand(self.hours, 1)
            self.wind_dir_str = 'Random wind'
        elif self.wind == self.wvar[1]:   #cfg.PREVAILING_WIND:
            self.wind_dir = -np.sqrt(2.) * erfcinv(2. * np.random.rand(self.hours, 1)) * 2.  #         norminv(rand(days.*24,1),0,40)
            # note at this point you can add on the prevailing wind direction, i.e.
            self.wind_dir = self.wind_dir + self.stack["wdirn"]
            self.wind_dir[np.where(self.wind_dir >= 360.)] = \
                np.mod(self.wind_dir[np.where(self.wind_dir >= 360)], 360)
            self.wind_dir_str = 'Prevailing wind'
        else:
            sys.exit()
    
        #return(x,y,z,times,stacks,stack_x,stack_y,stability,Dy,Dz,UTM_easting,UTM_northing,
        #      output,Q,H,wind_dir,wind_speed)