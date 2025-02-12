# -*- coding: utf-8 -*-
"""Config for the SensorFinger"""

__authors__ = "tnavez"
__contact__ = "tanguy.navez@inria.fr"
__version__ = "1.0.0"
__copyright__ = "(c) 2020, Inria"
__date__ = "Oct 28 2022"


import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute())+"/../")
sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute()))

from BaseConfig import GmshDesignOptimization

import numpy as np 

class Config(GmshDesignOptimization):
    def __init__(self):
        super(GmshDesignOptimization,self).__init__("AnkleModel")
        
    def init_model_parameters(self):

        ########################
        ### Parametric Model ###
        ########################

        # Geometric parameters
        self.dimBase=50.0
        self.dimVer=20.0
        self.percentageHeightBase=0.5
        self.numModules=5
        self.totalHeight=100.0
        self.origin_coord=[0,0,0]
        self.surfaceColor=[0.0, 0.8, 0.7, 1.0]
        self.rotation=[0.0,0.0,0.0]
        self.translation=[0.0,0.0,0.0]
                                    
        # Elasticity parameters
        self.PoissonRation = 0.3 #0.47
        self.YoungsModulus = 180000
        self.totalMass=1.0

        # Meshing parameters
        self.meshResolution=10.0

        
        # Cable
        self.numberCables = 4
        self.margin = self.dimBase*0.08
        
    def get_design_variables(self):            
        return {
        "dimBase":[self.dimBase,30.0,60.0],
        "numModules": [self.numModules, int(2), int(10)],
        "dimVer": [self.dimVer, 20.0 , 40.0],
        "percentageHeightBase": [self.percentageHeightBase, 0.1, 0.9]
        }
               
    def get_objective_data(self):
        return {"AbsoluteBendingAngle": ["maximize", 1000],}

    def get_assessed_together_objectives(self):
        return [["AbsoluteBendingAngle"]]

    def set_design_variables(self, new_values):
        super(Config,self).set_design_variables(new_values)
    def print_variables(self):
                # Geometric parameters
        print("dimBase:",self.dimBase,"dimVer=",
        self.dimVer,"percentageHeightBase=",
        self.percentageHeightBase,"numModules=",
        self.numModules,"totalHeight=",
        self.totalHeight,"origin_coord=",
        self.origin_coord,"surfaceColor=",
        self.surfaceColor,"rotation=",
        self.rotation,"translation=",
        self.translation,"PoissonRation=",
        self.PoissonRation,"YoungsModulus=",
        self.YoungsModulus,"totalMass=",
        self.totalMass,"meshResolution=",
        self.meshResolution,"numberCables=",
        self.numberCables,"margin=",
        self.margin)
    
