# -*- coding: utf-8 -*-
"""Optimization config for the SensorFinger with less design variables.
We optimise both for:
    - An absolute deflection angle.
    - An altered Volume Sensibility metric for avoiding obtaining non feasible design with too small cavities
"""

__authors__ = "tnavez"
__contact__ = "tanguy.navez@inria.fr"
__version__ = "1.0.0"
__copyright__ = "(c) 2020, Inria"
__date__ = "Oct 28 2022"


import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute())+"/../")
sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute()))

from Config import Config

import numpy as np 

class OptimizationConfig(Config):


    def get_objective_data(self):
        return {"AbsoluteBendingAngle": ["maximize", 80],}

    def get_assessed_together_objectives(self):
        return [["AbsoluteBendingAngle"]]    


    
    
