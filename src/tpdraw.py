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
#from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import os
# from matplotlib.mlab import griddata # deprecated since 2018


def tpdraw(c, df1, cols, fd, dt_string):   # output the plots
    fig, ax = plt.subplots(c,1, sharex=True, figsize=(12,25));
    fig.tight_layout(h_pad=4)
    fig.suptitle('Fife Ethylene Plant \n'+'Modelled air pollution \n'+ fd.datetouse[0], fontsize=14)
    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95)
    #plt.xticks(rotation=45)
    # Define the date format
    
    #plt.gca().xaxis.set_major_formatter(date_format)
    colylabels = ['(m $ s^{-1}$)', 'degrees', '', 'concentration \n ($ \mu g m^{-3}$)',
                   'concentration \n ($ \mu g m^{-3}$)', 'concentration \n ($ \mu g m^{-3}$)',
                   'concentration \n ($ \mu g m^{-3}$)','concentration \n ($ \mu g m^{-3}$)',
                   'concentration \n ($ \mu g m^{-3}$)','concentration \n ($ \mu g m^{-3}$)',
                   'concentration \n ($ \mu g m^{-3}$)','concentration \n ($ \mu g m^{-3}$)',
                   'concentration \n ($ \mu g m^{-3}$)']
    pltcols = ['r','g', 'b', 'm', 'm', 'm','m','m','m','m','m','m','m']
    for i in range(0,len(cols)):
        df1.plot(x='time',y=cols[i], ax=ax[i], color=pltcols[i])
        ax[i].set_ylabel(colylabels[i])
        ax[i].set_xlabel('Date & Time')
        plt.xticks(rotation=25)
        #date_format = DateFormatter('%m-%d-%h')
        #plt.gca().xaxis.set_major_formatter(date_format)
        #ax[i].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%h'))

    path = './results'
    plt.savefig(os.path.join(path,'receps_'+dt_string))
    fig.tight_layout()
    plt.show()    