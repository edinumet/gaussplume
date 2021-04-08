"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 6 April 2021 17:04 

DESCRIPTION
===========

Plots Gaussian Plume output
"""


import numpy as np
import math
import matplotlib.pyplot as plt
# from matplotlib.mlab import griddata # deprecated since 2018
from scipy.interpolate import griddata
# https://www.reddit.com/r/Python/comments/87lbao/matplotlib_griddata_deprecation_help/
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
#'plan','time_series','height_slice','none'
from pyproj import Proj, transform
import os
from datetime import datetime

def gpdraw(C1,img,dlist,outfile):   # output the plots
    output = dlist[0]
    easting = dlist[1]
    northing = dlist[2]
    x = dlist[3]
    y = dlist[4]
    stability_str = str(dlist[5])
    wind_dir_str = str(dlist[6])
    fheight_str = str(int(dlist[7]))
    rtoplot = dlist[9]
    dtimestr = dlist[10]
    bts = dlist[11]

    if output == "plan":    #cfg.PLAN_VIEW:
    # Set the map limit around Mossmorran
        
        extent = [-3.3733, -3.244456, 56.060534, 56.132276]
        fig, ax = plt.subplots(figsize=(14,16))

        # x and y are curently in units of metres from the central point (0,0)
        # convert them to eastings and northings
        xe = easting + x
        yn = northing + y
        # now convert to lat-lon
        p2 = Proj("+proj=utm +zone=30V, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
        xp, yp = p2(xe,yn,inverse=True)
        xmin = np.max(xp)
        xmax = np.min(xp)
        ymax = np.max(yp)
        ymin = np.min(yp)
        
        # We should also plot the receptors to be used
        rtplotll = []   # lat lon coordinates of receptors
        for i in range(0,len(rtoplot)):
            xer = easting + rtoplot[i][0]
            ynr = northing + rtoplot[i][1]
            xpr, ypr = p2(xer,ynr,inverse=True)
            rtplotll.append((xpr,ypr))
        
        #print(rtplotll)
        data = np.mean(C1, axis=2)*1e6
        # Find max conc so we can set the levels for the contours
        maxc = np.max(data)
        minc = np.min(data)
        # Need a cleverer and automatic solution to get levels.
        plt.contourf(xp, yp, data, alpha=0.25,levels=[5e0, 1e1, 5e1, 1e2, 5e2,1e3,5e3,5e4],
                cmap=plt.cm.jet,norm = LogNorm())
                 #levels=[ 5, 10, 20, 30, 40, 50, 100, 250, 750, 1000, 2000, 3000, 4000, 5000])
                #levels=[5e0, 5e1, 5e2,5e3,5e4],cmap=plt.cm.jet,norm = LogNorm()
        ax.imshow(img, extent=(xmax, xmin, ymin, ymax)) 
        #plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = False
        ax.set_xlabel('longitude')
        ax.set_ylabel('latitude')
        if bts:
            ax.set_title('Fife Ethylene Plant - Contribution' + '\n'
             + 'to pollution level in period: '+ dtimestr + '\n'
             + 'Effective Height  = '+ fheight_str +' m ', pad=15)
        else:
            ax.set_title('Fife Ethylene Plant - Hourly Contribution' + '\n'
            +'(Stability = '+stability_str + ', Direction = ' + wind_dir_str+'$^o$'+ '\n'
            + 'Effective Height  = '+ fheight_str +' m )', pad=35)
        cb1 = plt.colorbar(shrink=0.35)
        cb1.set_label('$\mu$ g m$^{-3}$')
        # plot the receptors
        xs = [x[0] for x in rtplotll]
        ys = [x[1] for x in rtplotll]
        plt.scatter(xs, ys, c="r", alpha=0.7, marker='^',
            label="receptor")
        ax.set_ylim(ymin, ymax)
        ax.set_xlim(xmax, xmin)
        path = './results'
        plt.savefig(os.path.join(path,outfile))
        plt.show()        

    elif output == "height_slice":    #cfg.HEIGHT_SLICE:
        plt.figure()
        plt.ion()
        plt.pcolor(y, z, np.mean(C1, axis=2) * 1e6, cmap='jet', shading='nearest')
        plt.clim((0, 1e2))
        plt.xlabel('y (metres)')
        plt.ylabel('z (metres)')
        plt.title(stability_str + '\n' + wind_dir_str)
        cb1 = plt.colorbar()
        cb1.set_label('$\mu$ g m$^{-3}$')
        plt.show()

    elif output == "time_series":    #cfg.SURFACE_TIME:
        f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False)
        ax1.plot(times, 1e6 * np.squeeze(C1[y_slice, x_slice, :]))
        try:
            ax1.plot(times, smooth(1e6 * np.squeeze(C1[y_slice, x_slice, :]), 24), 'r')
            ax1.legend(('Hourly mean', 'Daily mean'))
        except:
            sys.exit()

        ax1.set_xlabel('time (days)')
        ax1.set_ylabel('Mass loading ($\mu$ g m$^{-3}$)')
        ax1.set_title(stability_str + '\n' + wind_dir_str)

        ax2.plot(times, stability)
        ax2.set_xlabel('time (days)')
        ax2.set_ylabel('Stability parameter')
        f.show()

    elif output == "none":   #NO_PLOT:
        print('don''t plot')
    else:
        sys.exit()
