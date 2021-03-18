"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 17 March 2021 15:28 

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
        # receptor location in UTM coordinates    
        self.receptors = {
            'Little Raith Farm': {'utm_e': 482520, 'utm_n': 6218359, 'original': 1},
            'Watters Crescent Lochgelly': {'utm_e': 480697, 'utm_n': 6219619, 'original': 1},
            'Watson Street Cowdenbeath':  {'utm_e': 479138, 'utm_n': 6218032, 'original': 1},
            'Donibristle':  {'utm_e': 478871, 'utm_n': 6215555, 'original': 1},
            'Cowdenbeath Primary':   {'utm_e': 478610, 'utm_n': 6218032, 'original': 0},
            'Hill of Beath Primary': {'utm_e': 477146, 'utm_n': 6216830, 'original': 0},
            'Beath High School': {'utm_e': 477491, 'utm_n': 6218694, 'original': 0},
            'Foulford Primary':   {'utm_e': 478204, 'utm_n': 6218820, 'original': 0},
            'Medical Practice':  {'utm_e': 478130, 'utm_n': 6218471, 'original': 0},
            'Leisure Centre':     {'utm_e': 478537, 'utm_n': 6218450, 'original': 0},
            'Lumphinnans Primary': {'utm_e': 478917, 'utm_n': 6219305, 'original': 0}
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
                      "fwind": 5,
                      "ts"  : 0
                    }
        self.stabls = ["A","B","C","D","E","F","G"]
        self.outp=['plan','time_series','height_slice','none']
        self.wvar=["constant","prevailing","fluctuating"]
        self.recepstouse=['Little Raith Farm','Watters Crescent Lochgelly','Watson Street Cowdenbeath',
                         'Donibristle']    # default                 
        self.mls_recps = widgets.SelectMultiple(
                     options=['Little Raith Farm','Watters Crescent Lochgelly','Watson Street Cowdenbeath',
                         'Donibristle','Cowdenbeath Primary','Hill of Beath Primary','Beath High School',
                         'Foulford Primary','Medical Practice','Leisure Centre','Lumphinnans Primary'],
                     value=['Little Raith Farm','Watters Crescent Lochgelly','Watson Street Cowdenbeath',
                         'Donibristle'],
                     #rows=10,
                     description='receptors',
                     disabled=False
                     )
        self.rb_tm = widgets.RadioButtons(
                options=['manual', 'timeseries'],
                value='manual',
                description='Run_Type:',
                disabled=False)
        self.bit_nstacks = widgets.BoundedIntText(value = self.stack["nstack"], min=1,  max=10, step=1, 
                                     description="N Stacks", width=50)
        self.bit_wind = widgets.BoundedIntText(value = self.stack["wind"], min=1,  max=15, step=1, 
                                     description="u ($m \ s^{-1}$)", width=50)
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
        self.rb_tm.observe(self.rb_tm_eventhandler, names='value')
        self.mls_recps.observe(self.mls_recps_eventhandler, names='value')
        
        #self.btn = widgets.Button(description='Run RLINE', width=100)
        #self.btn.style.button_color = 'tomato'
        #self.btn.on_click(self.btn_eventhandler)
        self.h1 = widgets.HBox(children=[self.bit_wind, self.dd_stability,self.bit_wdirn])
        self.h2 = widgets.HBox(children=[self.bit_height, self.bit_heat, self.bit_strength])
        self.h3 = widgets.HBox(children=[self.dd_viewd, self.dd_wvarib, self.bit_nstacks])
        self.h4 = widgets.HBox(children=[self.mls_recps, self.rb_tm])
        
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
    
    def rb_tm_eventhandler(self,change):
        self.rb_tm.observe(self.rb_tm_eventhandler, names='value')
        self.stack["ts"]=self.rb_tm.value
        # disable some options if using met data
        if self.stack["ts"] == 'timeseries':  
            self.bit_wind.disabled=True
            self.bit_wdirn.disabled=True
            self.dd_stability.disabled=True
        else:
            self.bit_wind.disabled=False
            self.bit_wdirn.disabled=False
            self.dd_stability.disabled=False  
    
    def mls_recps_eventhandler(self,change):
        self.mls_recps.observe(self.mls_recps_eventhandler, names='value')
        self.recepstouse=self.mls_recps.value
        #print(self.recepstouse)

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
        
