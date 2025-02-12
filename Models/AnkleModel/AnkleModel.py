# -*- coding: utf-8 -*-
"""Config for the SensorFinger"""

__authors__ = "sescaidanavarro, tnavez"
__contact__ = "stefan.escaida@uoh.cl, tanguy.navez@inria.fr"
__version__ = "1.0.0"
__copyright__ = "(c) 2020, Inria"
__date__ = "Oct 28 2022"

import math
import numpy as np

from BaseFitnessEvaluationController import BaseFitnessEvaluationController
from stlib3.scene import MainHeader,ContactHeader
from Generation import Ankle


class FitnessEvaluationController(BaseFitnessEvaluationController):   
    
    def __init__(self, *args, **kwargs):

        print('>>> Start Init SOFA scene ...')

        super(FitnessEvaluationController,self).__init__(*args, **kwargs)

        self.ModelNode = self.rootNode.ankle.ElasticMaterialObject     
        self.Cables = self.ModelNode.cables
        self.StartPosition = np.array(self.ModelNode.endEffector.endEffectorPoint.position.value)[0]
        self.StartAngle = math.acos( np.abs(self.StartPosition[2]) / np.linalg.norm(self.StartPosition)) 
        self.FollowingMO = self.ModelNode.endEffector.endEffectorPoint
        
        # Objective evaluation variables
        self.current_iter = 0
        current_objectives = self.config.get_currently_assessed_objectives()
        self.max_iter = max([self.config.get_objective_data()[current_objectives[i]][1] for i in range(len(current_objectives))])
        
        
        print('>>> ... End')
        

    def onAnimateBeginEvent(self, dt):
        
        self.current_iter += 1
        self.pitch(1)
        if self.current_iter == self.max_iter:            
           
            current_objectives_names = self.config.get_currently_assessed_objectives()

            for i in range(len(current_objectives_names)):

                current_objective_name =  current_objectives_names[i]
                
                # Absolute Bending Angle 
                if "AbsoluteBendingAngle" == current_objective_name:               
                    CurrentPosition = np.array(self.FollowingMO.position.value[0])
                    Angle = np.abs(math.acos( abs(CurrentPosition[2]) / np.linalg.norm(CurrentPosition)))
                    print("Absolute angle: ", Angle)
                    self.objectives.append(Angle)
    def pitch(self,value):#turn axe x
        displacement = self.Cables.cable0.CableConstraint.value[0]
        displacement2 = self.Cables.cable1.CableConstraint.value[0]
        displacement3 = self.Cables.cable2.CableConstraint.value[0]
        displacement4 = self.Cables.cable3.CableConstraint.value[0]
        rate=abs(value)
        if value>0:
            displacement2 += rate
            displacement4 -= rate
        else:
            displacement4 += rate
            displacement2 -= rate
        self.Cables.cable0.CableConstraint.value = [displacement]
        self.Cables.cable1.CableConstraint.value = [displacement2]
        self.Cables.cable2.CableConstraint.value = [displacement3]
        self.Cables.cable3.CableConstraint.value = [displacement4]
    def roll(self,value):#turn axe z
        displacement = self.Cables.cable0.CableConstraint.value[0]
        displacement2 = self.Cables.cable1.CableConstraint.value[0]
        displacement3 = self.Cables.cable2.CableConstraint.value[0]
        displacement4 = self.Cables.cable3.CableConstraint.value[0]
        rate=abs(value)
        if value>0:
            displacement += rate
            displacement3 -= rate
        else:
            displacement3 += rate
            displacement -= rate
        self.Cables.cable0.CableConstraint.value = [displacement]
        self.Cables.cable1.CableConstraint.value = [displacement2]
        self.Cables.cable2.CableConstraint.value = [displacement3]
        self.Cables.cable3.CableConstraint.value = [displacement4]

def createScene(rootNode, config):
    
    ###############################
    ### Import required plugins ###
    ###############################
    rootNode.addObject("RequiredPlugin", name="SoftRobots")
    rootNode.addObject("RequiredPlugin", name="SofaSparseSolver")
    rootNode.addObject("RequiredPlugin", name="SofaPreconditioner")
    rootNode.addObject("RequiredPlugin", name="SofaPython3")
    rootNode.addObject('RequiredPlugin', name='SofaOpenglVisual')
    rootNode.addObject('RequiredPlugin', name="SofaMiscCollision")
    rootNode.addObject("RequiredPlugin", name="SofaBoundaryCondition")
    rootNode.addObject("RequiredPlugin", name="SofaConstraint")
    rootNode.addObject("RequiredPlugin", name="SofaEngine")
    rootNode.addObject('RequiredPlugin', name='SofaImplicitOdeSolver')
    rootNode.addObject('RequiredPlugin', name='SofaLoader')
    rootNode.addObject('RequiredPlugin', name="SofaSimpleFem")
    rootNode.addObject('RequiredPlugin', name="SofaDeformable")
    rootNode.addObject('RequiredPlugin', name="SofaGeneralLoader")
    rootNode.addObject('RequiredPlugin', name='MultiThreading')
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.AnimationLoop') # Needed to use components [FreeMotionAnimationLoop]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Detection.Algorithm') # Needed to use components [BVHNarrowPhase,BruteForceBroadPhase,CollisionPipeline]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Detection.Intersection') # Needed to use components [LocalMinDistance]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Geometry') # Needed to use components [LineCollisionModel,PointCollisionModel,TriangleCollisionModel]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Collision.Response.Contact') # Needed to use components [RuleBasedContactManager]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Constraint.Lagrangian.Correction') # Needed to use components [LinearSolverConstraintCorrection]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Constraint.Lagrangian.Solver') # Needed to use components [GenericConstraintSolver]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Engine.Select') # Needed to use components [BoxROI]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.LinearSolver.Direct') # Needed to use components [SparseLDLSolver]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Mapping.Linear') # Needed to use components [BarycentricMapping]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Mass') # Needed to use components [UniformMass]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.ODESolver.Backward') # Needed to use components [EulerImplicitSolver]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.SolidMechanics.FEM.Elastic') # Needed to use components [TetrahedronFEMForceField]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.SolidMechanics.Spring') # Needed to use components [RestShapeSpringsForceField]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.StateContainer') # Needed to use components [MechanicalObject]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Topology.Container.Constant') # Needed to use components [MeshTopology]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Topology.Container.Dynamic') # Needed to use components [TetrahedronSetTopologyContainer,TetrahedronSetTopologyModifier]  
    rootNode.addObject('RequiredPlugin', name='Sofa.Component.Visual') # Needed to use components [VisualStyle] 
    rootNode.addObject('RequiredPlugin', name='SofaCUDA')
    ##############################
    ### Visualization settings ###
    ##############################
    # rootNode.addObject('LightManager')
    # rootNode.addObject('PositionalLight', name="light1", color="0.8 0.8 0.8", position="0 60 50")                
    # rootNode.addObject('PositionalLight', name="light2", color="0.8 0.8 0.8", position="0 -60 -50") 
    rootNode.addObject('VisualStyle', displayFlags='hideWireframe showBehaviorModels hideCollisionModels hideBoundingCollisionModels showForceFields showInteractionForceFields')

    rootNode.VisualStyle.displayFlags = "showBehavior showCollisionModels"
    rootNode.getObject("VisualStyle").displayFlags = 'showForceFields showBehaviorModels showInteractionForceFields'
    ###########################
    ### Simulation settings ###
    ###########################
    rootNode.addObject('FreeMotionAnimationLoop')
    rootNode.findData('gravity').value = [0, 0,-9.8] 
    rootNode.findData('dt').value = 0.1
    # rootNode.addObject('EulerImplicitSolver', name='odesolver', firstOrder=0, rayleighMass=0.1,  rayleighStiffness=0.1)
    rootNode.addObject("GenericConstraintSolver", maxIterations=250, tolerance=1e-20)
    # MainHeader(rootNode, plugins=["SoftRobots"])
    ContactHeader(rootNode, alarmDistance=1, contactDistance=0.5, frictionCoef=8)
    Ankle(rootNode,config,"ankle")
    
    
    ##################
    ### Controller ###                            
    ##################
    rootNode.addObject(FitnessEvaluationController(name="FitnessEvaluationController", rootNode=rootNode, config=config))
    
    return rootNode

    
    
