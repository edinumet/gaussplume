"""
Class to produce a streetmap image
Get the Streetmap image for the background
Needs to be done ONCE at the start of the program
and put in memory, rather than be loaded from disk.
Almost ALL code in this Class comes from:
https://bryanbrattlof.com/adding-openstreetmaps-to-matplotlib/

"""

import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from itertools import product
from io import BytesIO

class stmap():
    def __init__(self,lat_max,lat_min,lon_min,lon_max,zoom):

        self.URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png".format
        self.TILE_SIZE = 256
        self.top, self.bot = lat_max, lat_min
        self.lef, self.rgt = lon_min, lon_max
        self.zoom = zoom   

        
    def point_to_pixels(self,lon, lat, zoom):
        """convert gps coordinates to web mercator"""
        self.r = math.pow(2, zoom) * self.TILE_SIZE
        lat = math.radians(lat)
        self.x = int((lon + 180.0) / 360.0 * self.r)
        self.y = int((1.0 - math.log(math.tan(lat) + 
           (1.0 / math.cos(lat))) / math.pi) / 2.0 * self.r)
        return self.x, self.y


    def drawmp(self): # Lets just check we've brought in the correct map!
            plt.figure(figsize=(4, 4))
            plt.axis('off')
            plt.imshow(self.img, aspect='auto')
            plt.show()
        # img now stored in memory for later use. 

        
    def run(self):
        self.x0, self.y0 = self.point_to_pixels(self.lef, self.top, self.zoom)
        self.x1, self.y1 = self.point_to_pixels(self.rgt, self.bot, self.zoom)

        self.x0_tile, self.y0_tile = int(self.x0 / self.TILE_SIZE), int(self.y0 / self.TILE_SIZE)
        self.x1_tile, self.y1_tile = math.ceil(self.x1 / self.TILE_SIZE), math.ceil(self.y1 / self.TILE_SIZE)

        assert (self.x1_tile - self.x0_tile) * (self.y1_tile - self.y0_tile) < 50, "That's too many tiles!"

        # full size image we'll add tiles to
        self.img = Image.new('RGB', (
            (self.x1_tile - self.x0_tile) * self.TILE_SIZE,
            (self.y1_tile - self.y0_tile) * self.TILE_SIZE))

        # loop through every tile inside our bounded box
        for self.x_tile, self.y_tile in product(range(self.x0_tile, self.x1_tile),
                              range(self.y0_tile, self.y1_tile)):

            with requests.get(self.URL(x=self.x_tile, y=self.y_tile, z=self.zoom)) as resp:
                self.tile_img = Image.open(BytesIO(resp.content))

            # add each tile to the full size image
            self.img.paste(
                im=self.tile_img,
                box=((self.x_tile - self.x0_tile) * self.TILE_SIZE,\
                     (self.y_tile - self.y0_tile) * self.TILE_SIZE))

        # Cropping The Multi Tile
        self.xc, self.yc = self.x0_tile * self.TILE_SIZE, self.y0_tile * self.TILE_SIZE

        self.img = self.img.crop((
            self.x0 - self.xc,  # left
            self.y0 - self.yc,  # top
            self.x1 - self.xc,  # right
            self.y1 - self.yc)) # bottom

        self.drawmp()
    # end run    