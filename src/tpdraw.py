"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 5 Feb 2021 16:30 

DESCRIPTION
===========

Plots time series and weather data
"""


import numpy as np
import math
import matplotlib.pyplot as plt
# from matplotlib.mlab import griddata # deprecated since 2018


def tpdraw(c, df1, cols, fd):   # output the plots
    fig, ax = plt.subplots(c,1, sharex=True, figsize=(10,25));
    fig.tight_layout(h_pad=4)
    fig.suptitle('Fife Ethylene Plant \n' + fd.datetouse[0], fontsize=14)
    plt.subplots_adjust(top=0.95)
    plt.xticks(rotation=45)
    for i in range(0,len(cols)):
        df1.plot(x='time',y=cols[i], ax=ax[i])
        plt.xticks(rotation=45)
    plt.show()    