"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 10 Feb 2021 21:08 

DESCRIPTION
===========
This package contains the class object for configuring and running 
the long term gaussian plume Jupyter notebook

"""

import ipywidgets as widgets
from IPython.display import display
import math

class ltgpinterface():

    def __init__(self):
         # ADMS stability classes
        self.stability = {
            'A':  {'u*': 0.1, 'H': 350, "L":-2 },
            'B':  {'u*': 0.2, 'H': 250, "L":-10 },
            'C':  {'u*': 0.5, 'H': 150, "L":-100 },
            'D':  {'u*': 0.5, 'H': 50, "L":0 },
            'E':  {'u*': 0.3, 'H': 25, "L":100 },
            'F':  {'u*': 0.2, 'H': -5, "L":20 },
            'G':  {'u*': 0.1, 'H': -25, "L":5 },
            }
        
        self.stack = {"wind": 5, 
                         "wdirn": 135, 
                         "stab":"D",
                         "height": 30,
                         "strength": 350,
                         "heat": 0,
                         "nstack": 1,
                         "view": "plan",
                         "wvari": "constant",
                         "fheight": 30,
                         "fwind": 5
                    }
        self.stabls = ["A","B","C","D","E","F","G"]
        self.outp=['plan','time_series','height_slice','none']
        self.wvar=["constant","prevailing","fluctuating"]
        self.bit_nstacks = widgets.BoundedIntText(value = self.stack["nstack"], min=1,  max=10, step=1, 
                                     description="N Stacks", width=50)
        self.bit_wind = widgets.BoundedIntText(value = self.stack["wind"], min=1,  max=15, step=1, 
                                     description="wind speed $m \ s^{-1}$", width=50)
        self.bit_height = widgets.BoundedIntText(value = self.stack["height"], min=1, max=100, step=1, 
                                        description="Height (m)", width=50)
        self.bit_strength = widgets.BoundedIntText(value =self.stack["strength"], min=150, max=4000, step=10, 
                                        description="source strength g s-1", width=50)
        self.dd_stability = widgets.Dropdown(value =self.stack["stab"], options=self.stabls, 
                                       description="stability", width=50)
        self.dd_viewd = widgets.Dropdown(value =self.stack["view"], options=self.outp, 
                                       description="views", width=50)
        self.dd_wvarib = widgets.Dropdown(value =self.stack["wvari"], options=self.wvar, 
                                       description="wind variability", width=50)
        self.bit_wdirn = widgets.BoundedIntText(value=self.stack["wdirn"], min=1, max=359, step=5, 
                                       description="wind direction", width=50)
        self.bit_heat = widgets.BoundedIntText(value=self.stack["heat"], min=0, max=20, step=1, 
                                       description="heat output", width=50)
        
        #self.sumtotal = widgets.Text(value=self.sumtt,description="Total should be 100%", width=50, color='red')
        
        self.bit_nstacks.observe(self.bit_nstacks_eventhandler, names='value')
        self.bit_wind.observe(self.bit_wind_eventhandler, names='value')
        self.bit_height.observe(self.bit_height_eventhandler, names='value')
        self.bit_strength.observe(self.bit_strength_eventhandler, names='value')
        self.dd_stability.observe(self.dd_stability_eventhandler, names='value')
        self.dd_viewd.observe(self.dd_viewd_eventhandler, names='value')
        self.dd_wvarib.observe(self.dd_wvarib_eventhandler, names='value')
        self.bit_wdirn.observe(self.bit_wdirn_eventhandler, names='value')
        self.bit_heat.observe(self.bit_heat_eventhandler, names='value')
        
        #self.btn = widgets.Button(description='Run RLINE', width=100)
        #self.btn.style.button_color = 'tomato'
        #self.btn.on_click(self.btn_eventhandler)
        self.h1 = widgets.HBox(children=[self.bit_wind, self.dd_stability,self.bit_wdirn])
        self.h2 = widgets.HBox(children=[self.bit_height, self.bit_heat, self.bit_strength])
        self.h3 = widgets.HBox(children=[self.dd_viewd, self.dd_wvarib, self.bit_nstacks])
        
    def bit_nstacks_eventhandler(self,change):
        self.bit_nstacks.observe(self.bit_nstacks_eventhandler, names='value')
        self.stack["nstack"]=self.bit_nstacks.value
           
    def bit_wind_eventhandler(self,change):
        self.bit_wind.observe(self.bit_wind_eventhandler, names='value')
        self.stack["wind"]=self.bit_wind.value

    def bit_wdirn_eventhandler(self,change):
        self.bit_wdirn.observe(self.bit_wdirn_eventhandler, names='value')
        self.stack["wdirn"]=self.bit_wdirn.value

    def dd_stability_eventhandler(self,change):
        self.dd_stability.observe(self.dd_stability_eventhandler, names='value')
        self.stack["stab"]=self.dd_stability.value
        
    def dd_viewd_eventhandler(self,change):
        self.dd_viewd.observe(self.dd_viewd_eventhandler, names='value')
        self.stack["view"]=self.dd_viewd.value
        
    def dd_wvarib_eventhandler(self,change):
        self.dd_wvarib.observe(self.dd_wvarib_eventhandler, names='value')
        self.stack["wvari"]=self.dd_wvarib.value

    def bit_height_eventhandler(self,change):
        self.bit_height.observe(self.bit_height_eventhandler, names='value')
        self.stack["height"]=self.bit_height.value

    def bit_strength_eventhandler(self,change):
        self.bit_strength.observe(self.bit_strength_eventhandler, names='value')
        self.stack["strength"]=self.bit_strength.value

    def bit_heat_eventhandler(self,change):
        self.bit_heat.observe(self.bit_heat_eventhandler, names='value')
        self.stack["heat"]=self.bit_heat.value
        self.stack["fheight"] = self.m_finalheight()
        #print("wind before effective height = "+ str(self.stack["wind"]))
        self.stack["fwind"] = self.wind_profile()
        #print("wind after effective height = "+ str(self.stack["fwind"]))
        
    def m_finalheight(self):
        """ docstring """
        if self.stack["heat"] == 0:
            self.dh = 0
        elif self.stack["heat"] >= 20:
            self.dh = 3.3 *  math.pow(self.stack["heat"], 0.333) *  math.pow(10 * self.stack["height"],
                                                                            0.667) / self.stack["wind"]
        else:
            self.dh = 20.5 * math.pow(self.stack["heat"], 0.6) * math.pow(self.stack["height"], 0.4) / self.stack["wind"]
        if self.stack["stab"] in ["A", "B", "C", "D"]:
            # Stability of A..D :
            return self.stack["height"] + self.dh
        elif self.stack["stab"] == "E":
            return self.stack["height"] + self.dh * 0.95
        elif self.stack["stab"] in ["F", "G"]:
            return self.stack["height"] + self.dh * 0.85
            # returns m_finalHeight    

    def wind_profile(self):
        """ docstring """
        a = 0.2
        # returns m_windProfile
        return self.stack["wind"] * math.pow(self.stack["fheight"] / 10, a)    
        
