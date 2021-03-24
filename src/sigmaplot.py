"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 5 Feb 2021 16:30 

DESCRIPTION
===========

Plots sigma_y amd sigma_z as a function of atmospheric stability

"""
import matplotlib.pyplot as plt
import numpy as np
from src import calc_sigmas

def sigmaplot():
    stabs = [0,1,2,3,4,5]
    legend = ['A','B','C','D','E','F']
    xr = np.arange(100,7100,100)          # every 100 m to 7 km
    c = len(stabs)
    r = np.size(xr,axis=0)
    sigy = np.zeros(r)
    sigz = np.zeros(r)
    sy = np.array([ [0] *c for i in range(r) ])
    sz = np.array([ [0] *c for i in range(r) ])

    for stablty in stabs:           # loop from very unstable to very stable
        sigy,sigz = calc_sigmas.calc_sigmas(stablty, xr)
        sy[:,stablty] = sigy
        sz[:,stablty] = sigz

    fig = plt.figure(figsize=(9,6))
    fig.suptitle('Spreading parameters $\sigma_y$ and $\sigma_z$')
    ax = plt.subplot(1, 2, 1)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(True, which="both", ls="-")
    ax.set_xlabel('distance downwind')
    ax.set_ylabel('$\sigma_y$ (m)')
    for i in stabs:
        ax.plot(xr, sy[:,i], label=legend[i])
    ax.legend()
    ax1 = plt.subplot(1, 2, 2)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.grid(True, which="both", ls="-")
    ax1.set_xlabel('distance downwind')
    ax1.set_ylabel('$\sigma_z$ (m)')
    for i in stabs:
        ax1.plot(xr, sz[:,i], label=legend[i])
    ax1.legend()
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()