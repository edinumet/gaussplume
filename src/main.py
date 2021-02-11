"""

"""
import tqdm as tqdm
import numpy as np
from ipywidgets import GridspecLayout
from src import gauss_func, calc_sigmas, smooth
from src import gpdraw

class main():
    def __init__(self,c,fd,img):
        self.c = c
        self.fd = fd
        self.img = img
        
    def run(self):    #self.c,self.fd,self.img):
        # SECTION 3: Main loop
        # For all times...
        self.C1 = np.zeros((len(self.c.x), len(self.c.y), len(self.c.wind_dir)))
        for i in tqdm.tqdm(range(0, len(self.c.wind_dir))):
            for j in range(0, self.c.stacks):
                self.C = np.ones((len(self.c.x), len(self.c.y)))
                self.C = gauss_func.gauss_func(self.c.Q[j], self.c.wind_speed[i], self.c.wind_dir[i], self.c.x, self.c.y,
                    self.c.z, self.c.stack_x[j], self.c.stack_y[j], self.c.H[j], self.c.Dy, self.c.Dz, self.c.stability[i])
                self.C1[:, :, i] = self.C1[:, :, i] + self.C
        
    def mdraw(self):  # SECTION 4: Post process / output
        self.dlist=[self.c.output,self.c.UTM_easting,self.c.UTM_northing,
            self.c.x,self.c.y,self.fd.stack["stab"],self.fd.stack["wdirn"]]
    
        # create a 10x2 grid layout
        self.grid = GridspecLayout(10, 2)
        # fill it in with widgets
        self.grid[:, 0] = self.fd.h1
        self.grid[0, 1] = self.fd.h1
        self.grid[1, 1] = self.fd.h2
        self.grid[2, 1] = self.fd.h3

        # set the widget properties
        self.grid[:, 0].layout.height = 'auto'
        self.grid
        self.gpdraw.gpdraw(self.C1,self.img,self.dlist)