# -*- coding: utf-8 -*-
"""Shape generation for the SensorFinger"""

__authors__ = "sescaidanavarro, tnavez"
__contact__ = "stefan.escaida@uoh.cl, tanguy.navez@inria.fr"
__version__ = "1.0.0"
__copyright__ = "(c) 2020, Inria"
__date__ = "Oct 28 2022"

import gmsh
import numpy as np
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def createSectionBase(radious,height,origin_coord,meshResolution=0.1):
    x_origin=origin_coord[0]
    y_origin=origin_coord[1]
    z_origin=origin_coord[2]
    points=[]
    points.append(gmsh.model.occ.addPoint(x_origin, y_origin, z_origin,meshResolution))
    points.append(gmsh.model.occ.addPoint(x_origin+radious, y_origin, z_origin,meshResolution))
    points.append(gmsh.model.occ.addPoint(x_origin+radious, y_origin, z_origin+height,meshResolution))
    points.append(gmsh.model.occ.addPoint(x_origin, y_origin, z_origin+height,meshResolution))
    # Crear líneas entre los puntos
    lines = [gmsh.model.occ.addLine(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
    # Cerrar el contorno creando una superficie
    surface = gmsh.model.occ.addCurveLoop(lines)
    profile = gmsh.model.occ.addPlaneSurface([surface])
    # Sincronizar para que Gmsh conozca la geometría
    gmsh.model.occ.synchronize()
    return profile


def createSectionVertebra(radious,height,origin_coord,meshResolution):
    x_origin=origin_coord[0]
    y_origin=origin_coord[1]
    z_origin=origin_coord[2]
    points=[]
    points.append(gmsh.model.occ.addPoint(x_origin, y_origin, z_origin,meshResolution))
    points.append(gmsh.model.occ.addPoint(x_origin+radious, y_origin, z_origin,meshResolution))
    points.append(gmsh.model.occ.addPoint(x_origin+radious, y_origin, z_origin+height,meshResolution))
    points.append(gmsh.model.occ.addPoint(x_origin, y_origin, z_origin+height,meshResolution))
    # Crear líneas entre los puntos
    lines = [gmsh.model.occ.addLine(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
    # Cerrar el contorno creando una superficie
    surface = gmsh.model.occ.addCurveLoop(lines)
    profile = gmsh.model.occ.addPlaneSurface([surface])
    ps = gmsh.model.addPhysicalGroup(2, surface)
    # Sincronizar para que Gmsh conozca la geometría
    gmsh.model.occ.synchronize()
    return profile

def createBase(radious,height,origin_coord,meshResolution=0.1):
    sectionbase=createSectionBase(radious,height,origin_coord,meshResolution)
    base=gmsh.model.occ.revolve([(2,sectionbase)],*origin_coord, 0, 0, 1,np.pi*2)
    # Sincronizar para que Gmsh conozca la geometría
    gmsh.model.occ.synchronize()
    return base 

def createVertebra(radious,height,origin_coord,meshResolution=0.1):
    sectionVertebra=createSectionBase(radious,height,origin_coord,meshResolution)
    vertebra=gmsh.model.occ.revolve([(2,sectionVertebra)],*origin_coord,0,0,1,np.pi*2)
    # Sincronizar para que Gmsh conozca la geometría
    gmsh.model.occ.synchronize()
    return vertebra

def createModule(dimBase,heightBase,dimVer,heightVer,origin_coord,meshResolution=0.1):
    base=createBase(dimBase/2,heightBase,origin_coord,meshResolution)
    x_origin=origin_coord[0]
    y_origin=origin_coord[1]
    z_origin=origin_coord[2]+heightBase
    vertebra=createVertebra(dimVer/2,heightVer,[x_origin,y_origin,z_origin],meshResolution)
    module,_=gmsh.model.occ.fuse([base[1]],[vertebra[1]])
    gmsh.model.occ.synchronize()
    return module

def CreateAnkleModel(dimBase,dimVer,percentageHeightBase,numModules,totalHeight,origin_coord,meshResolution=0.1):
    heightModule=float(totalHeight/( (numModules*(1-percentageHeightBase)) + (numModules+1)*percentageHeightBase))
    heightBase=float(heightModule*percentageHeightBase)
    heightVer=float(heightModule-heightBase)
    model=createModule(dimBase,heightBase,dimVer,heightVer,origin_coord,meshResolution)
    new_origin_coord=origin_coord
    for i in range(int(numModules-1)):
        new_origin_coord[2]=new_origin_coord[2]+heightModule
        newModule=createModule(dimBase,heightBase,dimVer,heightVer,origin_coord,meshResolution)
        model,_=gmsh.model.occ.fuse(model,newModule)
        if i==numModules-2:
            new_origin_coord[2]=new_origin_coord[2]+heightModule
            newModule=createBase(dimBase/2,heightBase,new_origin_coord,meshResolution)
            print(newModule)
            model,_=gmsh.model.occ.fuse(model,[newModule[1]])
    return model

def calculate_cables(dimBase,margin,percentageHeightBase,numModules,totalHeight,origin_coord,numberCables):
    heightModule=float(totalHeight/( (numModules*(1-percentageHeightBase)) + (numModules+1)*percentageHeightBase))
    heightBase=float(heightModule*percentageHeightBase)
    initialheightJoints=origin_coord[2]+heightBase/2
    separationFromCenter=(dimBase-margin)/2
    #find bases postions of each cable
    anglePircing=360.0/numberCables
    pointsXY=generatePointsXY(separationFromCenter,anglePircing)
    list_points=[]
    print(numModules,"modelooooooooo", type(numModules))
    for j in range(len(pointsXY)):
        nextLink=initialheightJoints
        points=[]
        for i in range(numModules+1):
            points.append([*pointsXY[j],float(nextLink)])
            nextLink=nextLink+heightModule
        list_points.append(points)
    return list_points

def generatePointsXY(radio, paso):
    points = []
    for theta in np.arange(0, 360+paso, paso):  # De 0 a 360 grados con un paso de 1 grado
        # Convertir theta de grados a radianes
        theta_rad = float(np.radians(theta))
        # Calcular x e y
        x = radio * (np.cos(theta_rad))
        y = radio * (np.sin(theta_rad))
        points.append([float(x), float(y)])
    return points
def calculate_Box(dimBase,percentageHeightBase,numModules,totalHeight,origin_coord):
    boxPoints=[]
    heightModule=float(totalHeight/( (numModules*(1-percentageHeightBase)) + (numModules+1)*percentageHeightBase))
    heightBase=float(heightModule*percentageHeightBase)
    boxPoints=[ float(-dimBase/2),float(-dimBase/2) , float(-heightBase/2),
              float(dimBase/2), float(dimBase/2) , float(heightBase/2)]
    return boxPoints

def get_collision_Mesh_low(file,totalHeight,numModules,percentageHeightBase,dimBase,origin_coord,meshResolution=0.1):
    heightModule=totalHeight/( (numModules*(1-percentageHeightBase)) + (numModules+1)*percentageHeightBase)
    heightBase=heightModule*percentageHeightBase
    heightVer=heightModule-heightBase
    gmsh.model.add("colissionMeshLow")
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", meshResolution)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", meshResolution)
    gmsh.model.occ.import_shapes(file)
    entities_2d = gmsh.model.occ.getEntities(2) # Aquí 3 significa que estamos listando volúmenes
    print("lista de entidades 2d de Openscade",entities_2d)  # Imprime una lista de pares (dimensión, tag)
    volumes = gmsh.model.occ.getEntities(dim=3)  # Aquí 3 significa que estamos listando volúmenes
    print(volumes)  # Imprime una lista de pares (dimensión, tag)
    gmsh.model.occ.remove(volumes) 
    # Creamos la caja 3D
    cubos=[]
    for i in range(numModules):
        xmin, xmax = -dimBase/2, dimBase/2
        ymin, ymax = -dimBase/2, dimBase/2
        zmin, zmax = heightBase+i*heightModule-heightBase/3,heightBase+i*heightModule+heightVer/3
        id_new_cubo=gmsh.model.occ.addBox(xmin, ymin, zmin, xmax-xmin, ymax-ymin, zmax-zmin,tag=100+i)
        cubos.append((3,id_new_cubo))
    gmsh.model.occ.intersect(entities_2d, cubos, removeObject=True, removeTool=True)
    dim=2
    entities_2d = gmsh.model.occ.getEntities(dim) # Aquí 3 significa que estamos listando volúmenes
    print("Entidades despues de interseccion:",entities_2d)  # Imprime una lista de pares (dimensión, tag)
    gmsh.model.occ.synchronize()
    return 
    
def get_collision_Mesh_top(file,totalHeight,numModules,percentageHeightBase,dimBase,origin_coord,meshResolution=0.1):
    heightModule=totalHeight/( (numModules*(1-percentageHeightBase)) + (numModules+1)*percentageHeightBase)
    heightBase=heightModule*percentageHeightBase
    heightVer=heightModule-heightBase
    gmsh.model.add("colissionMeshTop")
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", meshResolution)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", meshResolution)
    gmsh.model.occ.import_shapes(file)
    entities_2d = gmsh.model.occ.getEntities(2) # Aquí 3 significa que estamos listando volúmenes
    print("lista de entidades 2d de Openscade",entities_2d)  # Imprime una lista de pares (dimensión, tag)
    volumes = gmsh.model.occ.getEntities(dim=3)  # Aquí 3 significa que estamos listando volúmenes
    gmsh.model.occ.remove(volumes) 
    # Creamos la caja 3D
    cubos=[]
    for i in range(numModules):
        xmin, xmax = -dimBase/2, dimBase/2
        ymin, ymax = -dimBase/2, dimBase/2
        zmin, zmax = heightModule+i*heightModule-heightVer/3,heightModule+i*heightModule+heightBase/3
        id_new_cubo=gmsh.model.occ.addBox(xmin, ymin, zmin, xmax-xmin, ymax-ymin, zmax-zmin,tag=100+i)
        cubos.append((3,id_new_cubo))
    gmsh.model.occ.intersect(entities_2d, cubos, removeObject=True, removeTool=True)
    dim=2
    entities_2d = gmsh.model.occ.getEntities(dim) # Aquí 3 significa que estamos listando volúmenes
    print("Entidades despues de interseccion:",entities_2d)  # Imprime una lista de pares (dimensión, tag)
    gmsh.model.occ.synchronize()
    return entities_2d

###################
import Sofa.Core
import numpy as np
import socket
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
class AnkleController(Sofa.Core.Controller):
    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, args, kwargs)
        self.cable = args[0][0]
        self.cable2 = args[0][1]
        self.cable3 = args[0][2]
        self.cable4 = args[0][3]
        self.endeffector=args[1]
        self.dts=0.02
        self.t=0
        self.error=np.array([0,0,0])
        self.realPosition=np.array(self.endeffector.position.value)[0]
        self.rate=10
        self.name = "AnkleController"
        #self.start_conection()
        
    def start_conection(self):
        print("Esperando conexión de MATLAB...")
        self.conn, self.addr = server_socket.accept()
        print(f"Conectado a: {self.addr}")
    def send(self,positionEndEffector):
        
        posiciones_robot = {'posiciones': positionEndEffector}  # Aquí colocarías los datos reales de SOFA
        posiciones_json = json.dumps(posiciones_robot)
        # Enviar posiciones a MATLAB
        self.conn .sendall(posiciones_json.encode('utf-8'))
        
    def receive(self):
        datos_control = self.conn.recv(1024).decode('utf-8')
        controlSignal = json.loads(datos_control)
        print(f"Acciones de control recibidas: {controlSignal}")
        return controlSignal["actuadores"]
    
    # def onAnimateBeginEvent(self, event): # called at each begin of animation step
    #     self.t=self.t+self.dts
    #     self.realPosition=np.array(self.endeffector.position.value)[0]
    #     self.send(self.realPosition.tolist())
    #     self.error=self.receive()
    #     print(type(self.error),"-----------------------------------------------------------")
    #     if self.error[0]!=0:
    #         self.pitch(self.error[0])

    #     if self.error[2]!=0:
    #         self.roll(self.error[2])
    def pitch(self,value):#turn axe x
        displacement = self.cable.CableConstraint.value[0]
        displacement2 = self.cable2.CableConstraint.value[0]
        displacement3 = self.cable3.CableConstraint.value[0]
        displacement4 = self.cable4.CableConstraint.value[0]
        rate=abs(value)
        if value>0:
            displacement2 += rate
            displacement4 -= rate
        else:
            displacement4 += rate
            displacement2 -= rate
        self.cable.CableConstraint.value = [displacement]
        self.cable2.CableConstraint.value = [displacement2]
        self.cable3.CableConstraint.value = [displacement3]
        self.cable4.CableConstraint.value = [displacement4]
    def roll(self,value):#turn axe z
        displacement = self.cable.CableConstraint.value[0]
        displacement2 = self.cable2.CableConstraint.value[0]
        displacement3 = self.cable3.CableConstraint.value[0]
        displacement4 = self.cable4.CableConstraint.value[0]
        rate=abs(value)
        if value>0:
            displacement += rate
            displacement3 -= rate
        else:
            displacement3 += rate
            displacement -= rate
        self.cable.CableConstraint.value = [displacement]
        self.cable2.CableConstraint.value = [displacement2]
        self.cable3.CableConstraint.value = [displacement3]
        self.cable4.CableConstraint.value = [displacement4]
    
    def onKeypressedEvent(self, e):
        import Sofa.constants.Key as Key
        displacement = self.cable.CableConstraint.value[0]
        displacement2 = self.cable2.CableConstraint.value[0]
        displacement3 = self.cable3.CableConstraint.value[0]
        displacement4 = self.cable4.CableConstraint.value[0]
        rate=100
        if e["key"] == Key.rightarrow:
            displacement += rate
            displacement3 -= rate

        elif e["key"] == Key.leftarrow:
            displacement3 += rate
            displacement -= rate

        if e["key"] == Key.uparrow:
            displacement2 += rate
            # displacement4 -= rate

        elif e["key"] == Key.downarrow:
            displacement4 += rate
            # displacement2 -= rate
        # print("C1",displacement)
        self.cable.CableConstraint.value = [displacement]
        self.cable2.CableConstraint.value = [displacement2]
        self.cable3.CableConstraint.value = [displacement3]
        self.cable4.CableConstraint.value = [displacement4]
# ###################

def Ankle(parentNode,config,name):
    Ankle = parentNode.addChild(name)
    from stlib3.physics.deformable import ElasticMaterialObject
    from stlib3.physics.constraints import FixedBox
    from softrobots.actuators import PullingCable
    from stlib3.physics.collision import CollisionMesh

    config.print_variables()
    filename_volume=config.get_mesh_filename(mode = "Volume", refine = 0, 
                                                        generating_function = CreateAnkleModel, 
                                                        dimBase=config.dimBase,dimVer=config.dimVer,percentageHeightBase=config.percentageHeightBase,
                                                        numModules=config.numModules,totalHeight=config.totalHeight,origin_coord=config.origin_coord,
                                                        meshResolution=config.meshResolution)
    filename_surface=config.get_mesh_filename(mode = "Surface", refine = 0, 
                                                        generating_function = CreateAnkleModel, 
                                                        dimBase=config.dimBase,dimVer=config.dimVer,percentageHeightBase=config.percentageHeightBase,
                                                        numModules=config.numModules,totalHeight=config.totalHeight,origin_coord=config.origin_coord,
                                                        meshResolution=config.meshResolution)
    filename_step=config.get_mesh_filename(mode = "Step", refine = 0, 
                                                        generating_function = CreateAnkleModel, 
                                                        dimBase=config.dimBase,dimVer=config.dimVer,percentageHeightBase=config.percentageHeightBase,
                                                        numModules=config.numModules,totalHeight=config.totalHeight,origin_coord=config.origin_coord,
                                                        meshResolution=config.meshResolution)
    filename_collision_low=config.get_mesh_filename(mode = "Surface", refine = 0, 
                                                        generating_function = get_collision_Mesh_low, file=filename_step,
                                                        dimBase=config.dimBase,percentageHeightBase=config.percentageHeightBase,
                                                        numModules=config.numModules,totalHeight=config.totalHeight,origin_coord=config.origin_coord,
                                                        meshResolution=config.meshResolution)
    filename_collision_top=config.get_mesh_filename(mode = "Surface", refine = 0, 
                                                        generating_function = get_collision_Mesh_top, file=filename_step,
                                                        dimBase=config.dimBase,percentageHeightBase=config.percentageHeightBase,
                                                        numModules=config.numModules,totalHeight=config.totalHeight,origin_coord=config.origin_coord,
                                                        meshResolution=config.meshResolution)
    print(filename_step,filename_collision_low,filename_collision_top)
    femAnkle = ElasticMaterialObject(Ankle,
                                    volumeMeshFileName=filename_volume,
                                    poissonRatio=config.PoissonRation,
                                    youngModulus=config.YoungsModulus,
                                    totalMass=config.totalMass,
                                    surfaceColor=config.surfaceColor,
                                    surfaceMeshFileName=filename_surface,
                                    rotation=config.rotation,
                                    translation=config.translation,
                                    scale=[1.0, 1.0, 1.0])
    
    Ankle.addChild(femAnkle)
    ##create box
    FixedBox(femAnkle,
             doVisualization=True,
             atPositions=calculate_Box(dimBase=config.dimBase,percentageHeightBase=config.percentageHeightBase,numModules=config.numModules,
                                       totalHeight=config.totalHeight,origin_coord=config.origin_coord))
    #create cables
    cable =femAnkle.addChild("cables")
    cables=[]
    list_points=calculate_cables(dimBase=config.dimBase,margin=config.margin,percentageHeightBase=config.percentageHeightBase,
                                 numModules=config.numModules,totalHeight=config.totalHeight,origin_coord=config.origin_coord,numberCables=config.numberCables)
    for i in range(len(list_points)):
        cables.append(PullingCable(cable, valueType="force",name="cable"+str(i),cableGeometry=list_points[i]))
    CollisionMesh(femAnkle,
                  surfaceMeshFileName=filename_surface, name="part0", collisionGroup=[1, 2])

    CollisionMesh(femAnkle,
                  surfaceMeshFileName=filename_collision_low,
                  name="CollisionMeshAuto1", collisionGroup=[1])

    CollisionMesh(femAnkle,
                  surfaceMeshFileName=filename_collision_top,
                  name="CollisionMeshAuto2", collisionGroup=[2])
    #create the endeffector
    effector = femAnkle.addChild('endEffector')
    endeffectorPoint=config.origin_coord
    endeffectorPoint[2]=endeffectorPoint[2]+config.totalHeight
    effector.addObject('MechanicalObject', position=endeffectorPoint,name="endEffectorPoint")
    effector.addObject('BarycentricMapping', mapForces=False, mapMasses=False)
    effector.addObject("Monitor",template="Vec3d",name="endEffector",listening="1",indices="100",showPositions="1",PositionsColor="1 1 0 1",
                       TrajectoriesPrecision="0.1",TrajectoriesColor="1 1 0 1",sizeFactor="1")
    Ankle.addObject(AnkleController(cables,effector.endEffectorPoint))


def createScene(rootNode):
    import Config
    # -*- coding: utf-8 -*-
    from stlib3.scene import MainHeader,ContactHeader

    m = MainHeader(rootNode, plugins=["SoftRobots"])
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
    rootNode.addObject('RequiredPlugin', name='MultiThreading') # Needed to use components [ParallelBVHNarrowPhase,ParallelBruteForceBroadPhase,ParallelTetrahedronFEMForceField] 
    rootNode.addObject('RequiredPlugin', name='SofaValidation') # Needed to use components [Monitor] 
    rootNode.VisualStyle.displayFlags = "showBehavior showMapping"
    # m.getObject("VisualStyle").displayFlags = 'showForceFields showBehaviorModels showInteractionForceFields'
    ContactHeader(rootNode, alarmDistance=1, contactDistance=0.5, frictionCoef=8)
    config=Config.Config()
    Ankle(rootNode,config,"Ankle")
    return rootNode