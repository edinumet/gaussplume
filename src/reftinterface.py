"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 5 Feb 2021 16:30 

DESCRIPTION
===========
This package contains the class object for configuring and running 
the RLINE/EFT Jupyter notebook

"""
import os
import subprocess
import ipywidgets as widgets
from IPython.display import display

class reftinterface():
    def __init__(self):
        # Should now scale for the time of day effect
        # TAF - Temporal Allocation Factor
        #  Get from up-to-date Tom Tom web site: 
        #      https://www.tomtom.com/en_gb/traffic-index/edinburgh-traffic/
        #  For a typical Wednesday since that seems to be the eveing rush-hour with most    congestion
        # TAF list has % congestion by hour starting at hour 0, midnight
        # In Jupyter Notebook make this a Figure
        self.TomTom_congestion = [2, 0, 0, 0, 0, 0, 13, 54, 80, 50, 38, 38, 40, \
            40, 42, 55, 81, 86, 54, 30, 20, 16, 14, 8]
        #print(sum(TomTom_congestion))
        self.trafficstats = {"AADT": 10000,
                    "hour": 12,
                    "vs": 15
                   }
        # Now adjust for fleet Mix and AADT and Time
        # Defaults -  get from spreadsheet for 2020
        # Urban split for England in 2020 below since that's likely to be the most relevant
        # Use a selection box for this
        self.fleetmix_2020 = {"electric": 0.5, 
                         "petrol": 47.8, 
                         "diesel":33.1,
                         "petrol_lgv": 0.4,
                         "diesel_lgv": 15.0,
                         "rigid": 0.9,
                         "artic": 0.4,
                         "biodiesel": 0.1,
                         "buses": 0.7,
                         "motorcycle": 1.1
                        }
        self.sumt=0.0
        for x in self.fleetmix_2020.values():
            self.sumt=self.sumt+x
            self.sumtt=(str(int(self.sumt)))
        #print(self.sumtt)

        self.bft_electric = widgets.BoundedFloatText(value = self.fleetmix_2020["electric"], min=0.1,  max=90, step=1, 
                                     description="electric %", width=50)
        self.bft_petrol_cars = widgets.BoundedFloatText(value = self.fleetmix_2020["petrol"], min=5, max=75, step=0.5, 
                                        description="petrol cars %", width=50)
        self.bft_diesel_cars = widgets.BoundedFloatText(value =self.fleetmix_2020["diesel"],  min=5, max=75, step=0.5, 
                                        description="diesel cars %", width=50)
        self.bft_petrol_lgv = widgets.BoundedFloatText(value =self.fleetmix_2020["petrol_lgv"], min=0.1, max=0.8, step=0.1, 
                                       description="petrol lgv %", width=50)
        self.bft_diesel_lgv = widgets.BoundedFloatText(value=self.fleetmix_2020["diesel_lgv"], min=3, max=18, step=1, 
                                       description="diesel lgv %", width=50)
        self.bft_rigid_truck = widgets.BoundedFloatText(value=self.fleetmix_2020["rigid"],min=0.1, max=1.0, step=0.1, 
                                        description="rigid truck %", width=50)
        self.bft_artic_truck = widgets.BoundedFloatText(value=self.fleetmix_2020["artic"], min=0.1, max=0.6, step=0.1, 
                                        description="artic truck %", width=50)  
        self.bft_biodiesel = widgets.BoundedFloatText(value=self.fleetmix_2020["biodiesel"], min=0.1, max=1.0,step=0.1, 
                                      description="biodiesel %", width=50)
        self.bft_buses = widgets.BoundedFloatText(value=self.fleetmix_2020["buses"], min=0.1, max=1.5, step=0.1, 
                                  description="buses %", width=50)
        self.bft_motorcycles = widgets.BoundedFloatText(value=self.fleetmix_2020["motorcycle"], min=0.5, max=1.5, step=0.1, 
                                        description="motorcycles %", width=50)
        self.sumtotal = widgets.Text(value=self.sumtt,description="Total should be 100%", width=50, color='red')
        
        self.bft_electric.observe(self.bft_electric_eventhandler, names='value')
        self.bft_hour = widgets.BoundedIntText(value=self.trafficstats["hour"],min=1, max=24, step=1,
                                    description="Hour of Day")
        self.bft_AADT = widgets.BoundedIntText(value=self.trafficstats["AADT"], min=1000, max=55000,step=1000,
                                    description="AADT")
        self.bft_vs = widgets.BoundedIntText(value=self.trafficstats["vs"], min=5, max=85, step=5,
                                  description="Speed")
        self.bft_petrol_cars.observe(self.bft_petrol_cars_eventhandler, names='value')
        self.bft_diesel_cars.observe(self.bft_diesel_cars_eventhandler, names='value')
        self.bft_petrol_lgv.observe(self.bft_petrol_lgv_eventhandler, names='value')
        self.bft_diesel_lgv.observe(self.bft_diesel_lgv_eventhandler, names='value')
        self.bft_rigid_truck.observe(self.bft_rigid_truck_eventhandler, names='value')
        self.bft_artic_truck.observe(self.bft_artic_truck_eventhandler, names='value')
        self.bft_biodiesel.observe(self.bft_biodiesel_eventhandler, names='value')
        self.bft_buses.observe(self.bft_buses_eventhandler, names='value')
        self.bft_motorcycles.observe(self.bft_motorcycles_eventhandler, names='value')
        
        self.bft_hour.observe(self.bft_hour_eventhandler, names='value')
        self.bft_AADT.observe(self.bft_AADT_eventhandler, names='value')
        self.bft_vs.observe(self.bft_vs_eventhandler, names='value')
        self.btn = widgets.Button(description='Run RLINE', width=100)
        self.btn.style.button_color = 'tomato'
        self.btn.on_click(self.btn_eventhandler)

        self.h1 = widgets.HBox(children=[self.bft_electric, self.bft_petrol_cars, self.bft_diesel_cars])
        self.h2 = widgets.HBox(children=[self.bft_petrol_lgv, self.bft_diesel_lgv, self.bft_rigid_truck])
        self.h3 = widgets.HBox(children=[self.bft_artic_truck, self.bft_biodiesel, self.bft_buses])
        self.h4 = widgets.HBox(children=[self.bft_motorcycles,self.sumtotal])

    def checksum(self):
        sum=0.0
        for x in self.fleetmix_2020.values():
            sum=sum+x
        self.sumt=sum
        self.sumtt=(str(int(self.sumt))) # make it an integer so students don't chase getting exactly 100.0
        self.sumtotal.value = self.sumtt
           
    def bft_electric_eventhandler(self,change):
        self.bft_electric.observe(self.bft_electric_eventhandler, names='value')
        self.fleetmix_2020["electric"]=self.bft_electric.value
        self.checksum()

    def bft_petrol_cars_eventhandler(self,change):
        self.bft_petrol_cars.observe(self.bft_petrol_cars_eventhandler, names='value')
        self.fleetmix_2020["petrol"]=self.bft_petrol_cars.value
        self.checksum()

    def bft_diesel_cars_eventhandler(self,change):
        self.bft_diesel_cars.observe(self.bft_diesel_cars_eventhandler, names='value')
        self.fleetmix_2020["diesel"]=self.bft_diesel_cars.value
        self.checksum()

    def bft_petrol_lgv_eventhandler(self,change):
        self.bft_petrol_lgv.observe(self.bft_petrol_lgv_eventhandler, names='value')
        self.fleetmix_2020["petrol_lgv"]=self.bft_petrol_lgv.value
        self.checksum()

    def bft_diesel_lgv_eventhandler(self,change):
        self.bft_diesel_lgv.observe(self.bft_diesel_lgv_eventhandler, names='value')
        self.fleetmix_2020["diesel_lgv"]=self.bft_diesel_lgv.value
        self.checksum()

    def bft_rigid_truck_eventhandler(self,change):
        self.bft_rigid_truck.observe(self.bft_rigid_truck_eventhandler, names='value')
        self.fleetmix_2020["rigid"]=self.bft_rigid_truck.value
        self.checksum()

    def bft_artic_truck_eventhandler(self,change):
        self.bft_artic_truck.observe(self.bft_artic_truck_eventhandler, names='value')
        self.fleetmix_2020["artic"]=self.bft_artic_truck.value
        self.checksum()

    def bft_biodiesel_eventhandler(self,change):
        self.bft_biodiesel.observe(self.bft_biodiesel_eventhandler, names='value')
        self.fleetmix_2020["biodiesel"]=self.bft_biodiesel.value
        self.checksum()

    def bft_buses_eventhandler(self,change):
        self.bft_buses.observe(self.bft_buses_eventhandler, names='value')
        self.fleetmix_2020["buses"]=self.bft_buses.value
        self.checksum()

    def bft_motorcycles_eventhandler(self,change):
        self.bft_motorcycles.observe(self.bft_motorcycles_eventhandler, names='value')
        self.fleetmix_2020["motorcycle"]=self.bft_motorcycles.value
        self.checksum()
        
    def bft_hour_eventhandler(self,change):
        self.bft_hour.observe(self.bft_hour_eventhandler, names='value')
        self.trafficstats["hour"]=self.bft_hour.value
            
    def bft_AADT_eventhandler(self,change):
        self.bft_AADT.observe(self.bft_AADT_eventhandler, names='value')
        self.trafficstats["AADT"]=self.bft_AADT.value

    def bft_vs_eventhandler(self,change):
        self.bft_vs.observe(self.bft_vs_eventhandler, names='value')
        self.trafficstats["vs"]=self.bft_vs.value
    
    def btn_eventhandler(self,obj):
        if not os.path.exists("Line_Source_Inputs.txt"):
            print("File does not exist: "+str('Line_Source_Inputs.txt'))
        if not os.path.exists("Receptor_Example.txt"):
            print("File does not exist: "+str("Receptor_Example.txt"))    
        if not os.path.exists("Source_Example.txt"):
            print("File does not exist: "+str("Source_Example.txt"))
        if not os.path.exists("Met_Example.sfc"):
            print("File does not exist: "+str("Met_Example.sfc"))
        # Delete any old data before running the model again
        ## delete only if file exists ##
        if os.path.exists("RLINEv1_2.ifort.x"):
            #ret = subprocess.run(["./RLINEv1_2.ifort.x"],shell=True)
            print("running RLINE ...")
            ret = subprocess.call(["./RLINEv1_2.ifort.x"],shell=True)
        else:
            sys.exit(0)
        if(ret == 0):
            print("Run complete - goto next cell")    
        
        
