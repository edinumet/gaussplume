#!/usr/bin/env python
# coding: utf-8

from io import BytesIO
import requests
from PIL import Image
import numpy as np
import sys
from scipy.special import erfcinv as erfcinv
# from calc_sigmas import calc_sigmas
import numpy as np
import sys
from scipy.special import erfcinv as erfcinv
import tqdm as tqdm
import time
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import ticker, cm
#import matplotlib.image as mpimg
from src import gauss_func, overlay_on_map, calc_sigmas, smooth
from src import config as cfg
from pyproj import Proj, transform

rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
# for Palatino and other serif fonts use:
rc('font', **{'family': 'serif', 'serif': ['Palatino']})
# rc('text', usetex = False)
print('imports OK')

# https://bryanbrattlof.com/adding-openstreetmaps-to-matplotlib/
URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png".format
import math
TILE_SIZE = 256

def point_to_pixels(lon, lat, zoom):
    """convert gps coordinates to web mercator"""
    r = math.pow(2, zoom) * TILE_SIZE
    lat = math.radians(lat)

    x = int((lon + 180.0) / 360.0 * r)
    y = int((1.0 - math.log(math.tan(lat) + (1.0 / math.cos(lat))) / math.pi) / 2.0 * r)

    return x, y

# SECTION 1: Configuration
# Variables can be changed by the user
RH = 0.90
aerosol_type = cfg.SODIUM_CHLORIDE
x = cfg.x
y = cfg.y
dry_size = 60e-9
humidify = cfg.DRY_AEROSOL

stab1 = 4  # set from 1-6
stability_used = cfg.CONSTANT_STABILITY

output = cfg.PLAN_VIEW #HEIGHT_SLICE # PLAN_VIEW  # SURFACE_TIME # PLAN_VIEW
x_slice = 26  # position (1-50) to take the slice in the x-direction
y_slice = 1  # position (1-50) to plot concentrations vs time

wind = cfg.PREVAILING_WIND
stacks = cfg.FOUR_STACKS
stack_x = [0., -100., -1000., 300,  130, 330, -1000, -1500, -2000, 2000]
stack_y = [0., 100., 500., 300, 250, 850, -1000, 1500, 2000, 2000]

Q = [400., 500., 600., 700, 1000, 20, 40, 50, 10, 10]  # mass emitted per unit time
H = [10., 15., 60., 50, 15, 10, 15, 35, 10, 10]  # stack height, m
days = 5  # run the model for n days - could be 365!

times = np.mgrid[1:days * 24 + 1:1] / 24.

Dy = 100.
Dz = 100.

# Get the map Data
# Get more than one tile
lat_max = 56.132276
lat_min = 56.060534
lon_min = -3.3733
lon_max = -3.244456

#################################
#      Multi Tile Visual
#################################
top, bot = lat_max, lat_min
lef, rgt = lon_min, lon_max

zoom = 13
x0, y0 = point_to_pixels(lef, top, zoom)
x1, y1 = point_to_pixels(rgt, bot, zoom)

x0_tile, y0_tile = int(x0 / TILE_SIZE), int(y0 / TILE_SIZE)
x1_tile, y1_tile = math.ceil(x1 / TILE_SIZE), math.ceil(y1 / TILE_SIZE)

assert (x1_tile - x0_tile) * (y1_tile - y0_tile) < 50, "That's too many tiles!"

from itertools import product

# full size image we'll add tiles to
img = Image.new('RGB', (
        (x1_tile - x0_tile) * TILE_SIZE,
        (y1_tile - y0_tile) * TILE_SIZE))

# loop through every tile inside our bounded box
for x_tile, y_tile in product(range(x0_tile, x1_tile),
                              range(y0_tile, y1_tile)):

    with requests.get(URL(x=x_tile, y=y_tile, z=zoom)) as resp:
        tile_img = Image.open(BytesIO(resp.content))

    # add each tile to the full size image
    img.paste(
        im=tile_img,
        box=((x_tile - x0_tile) * TILE_SIZE,\
             (y_tile - y0_tile) * TILE_SIZE))

#plt.imshow(img)
#plt.savefig('mossmorran_0.png', bbox_inches ="tight")


#################################
#      Crop Lines Visual
#  Don't include this in article
#################################
from PIL import ImageDraw
img2 = img.copy()

# find the mercator coordinates of the top-left corner of all
# the tiles we downloaded from OpenStreetMap
xc, yc = x0_tile * TILE_SIZE, y0_tile * TILE_SIZE

# draw a red rectangle of the part of the image we want to keep
draw = ImageDraw.Draw(img2)
draw.rectangle(
    (x0 - xc,  # left
     y0 - yc,  # top
     x1 - xc,  # right
     y1 - yc), # bottom
    outline=(255, 0, 0),
    width=5)

# draw black rectangles around each individual tile
for x_tile, y_tile in product(range(0, (x1_tile - x0_tile)),
                              range(0, (y1_tile - y0_tile))):

    xc, yc = x_tile * TILE_SIZE, y_tile * TILE_SIZE
    draw.rectangle(
        (xc - 2,  # left
         yc - 2,  # top
         (xc + TILE_SIZE),  # right
         (yc + TILE_SIZE)), # bottom
        outline=(0, 0, 0),
        width=2)

#plt.imshow(img2)
#plt.savefig('mossmorran.png', bbox_inches ="tight")

#################################
# Cropping The Multi Tile Visual
#################################
xc, yc = x0_tile * TILE_SIZE, y0_tile * TILE_SIZE

img = img.crop((
    x0 - xc,  # left
    y0 - yc,  # top
    x1 - xc,  # right
    y1 - yc)) # bottom


# SECTION 2: Act on the configuration information

# Decide which stability profile to use
if stability_used == cfg.CONSTANT_STABILITY:

    stability = stab1 * np.ones((days * 24, 1))
    stability_str = cfg.stability_str[stab1 - 1]
elif stability_used == cfg.ANNUAL_CYCLE:

    stability = np.round(2.5 * np.cos(times * 2. * np.pi / 365.) + 3.5)
    stability_str = 'Annual cycle'
else:
    sys.exit()

# decide what kind of run to do, plan view or y-z slice, or time series
if output == cfg.PLAN_VIEW or output == cfg.SURFACE_TIME or output == cfg.NO_PLOT:

    C1 = np.zeros((len(x), len(y), days * 24))  # array to store data, initialised to be zero

    [x, y] = np.meshgrid(x, y)  # x and y defined at all positions on the grid
    z = np.zeros(np.shape(x))  # z is defined to be at ground level.
elif output == cfg.HEIGHT_SLICE:
    z = np.mgrid[0:500 + cfg.dz:cfg.dz]  # z-grid

    C1 = np.zeros((len(y), len(z), days * 24))  # array to store data, initialised to be zero

    [y, z] = np.meshgrid(y, z)  # y and z defined at all positions on the grid
    x = x[x_slice] * np.ones(np.shape(y))  # x is defined to be x at x_slice
else:
    sys.exit()

# Set the wind based on input flags++++++++++++++++++++++++++++++++++++++++
wind_speed = 12. * np.ones((days * 24, 1))  # m/s
if wind == cfg.CONSTANT_WIND:
    wind_dir = 225. * np.ones((days * 24, 1))
    wind_dir_str = 'Constant wind'
elif wind == cfg.FLUCTUATING_WIND:
    wind_dir = 360. * np.random.rand(days * 24, 1)
    wind_dir_str = 'Random wind'
elif wind == cfg.PREVAILING_WIND:
    wind_dir = -np.sqrt(2.) * erfcinv(2. * np.random.rand(24 * days, 1)) * 2.  # norminv(rand(days.*24,1),0,40)
    # note at this point you can add on the prevailing wind direction, i.e.
    wind_dir = wind_dir + 135
    wind_dir[np.where(wind_dir >= 360.)] =         np.mod(wind_dir[np.where(wind_dir >= 360)], 360)
    wind_dir_str = 'Prevailing wind'
else:
    sys.exit()


# In[3]:


# SECTION 3: Main loop
# For all times...
C1 = np.zeros((len(x), len(y), len(wind_dir)))
for i in tqdm.tqdm(range(0, len(wind_dir))):
    for j in range(0, stacks):
        C = np.ones((len(x), len(y)))
        C = gauss_func.gauss_func(Q[j], wind_speed[i], wind_dir[i], x, y, z,
                       stack_x[j], stack_y[j], H[j], Dy, Dz, stability[i])
        C1[:, :, i] = C1[:, :, i] + C


# In[8]:


# SECTION 4: Post process / output

# decide whether to humidify the aerosol and hence increase the mass
if humidify == cfg.DRY_AEROSOL:
    print('do not humidify')
elif humidify == cfg.HUMIDIFY:
    mass = np.pi / 6. * rho_s[aerosol_type] * dry_size ** 3.
    moles = mass / Ms[aerosol_type]

    nw = RH * nu[aerosol_type] * moles / (1. - RH)
    mass2 = nw * Mw + moles * Ms[aerosol_type]
    C1 = C1 * mass2 / mass
else:
    sys.exit()

# output the plots
if output == cfg.PLAN_VIEW:
    # Set the map limit around Mossmorran
    extent = [-3.3733, -3.244456, 56.060534, 56.132276]
    fig, ax = plt.subplots()

    # x and y are curently in units of metres from the central point (0,0)
    # convert them to eastings and northings
    xe = cfg.UTM_easting + x
    yn = cfg.UTM_northing + y
    # now convert to lat-lon
    p2 = Proj("+proj=utm +zone=30V, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
    xp, yp = p2(xe,yn,inverse=True)
    xmin = np.max(xp)
    xmax = np.min(xp)
    ymax = np.max(yp)
    ymin = np.min(yp)
    print(xmin,xmax,ymin, ymax)

    data = np.mean(C1, axis=2)*1e6
    maxc = np.max(data)
    minc = np.min(data)
    print(minc, maxc)
    
    plt.contourf(xp, yp, data, alpha=0.5, cmap = 'jet', levels=[ 1000, 2000, 3000, 4000, 
        5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000])
    ax.imshow(img, extent=(xmax, xmin, ymin, ymax)) 
    #plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = False
    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    ax.set_title('Mossmorran AQ Breaches, 2020' + '\n'
                 +'('+stability_str + ' - ' + wind_dir_str+')', pad=35)
    
    cb1 = plt.colorbar()
    cb1.set_label('$\mu$ g m$^{-3}$')
    #img = plt.imread("mossmorran_final.png")
    
    ax.set_ylim(ymin, ymax)
    ax.set_xlim(xmax, xmin)
    plt.savefig("Mossmorran_Concentrations.png")
    plt.show()

elif output == cfg.HEIGHT_SLICE:
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

elif output == cfg.SURFACE_TIME:
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

elif output == NO_PLOT:
    print('don''t plot')
else:
    sys.exit()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




