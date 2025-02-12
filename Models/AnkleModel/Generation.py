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
    gmsh.option.setNumber("General.Verbosity", 0)
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
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.model.occ.import_shapes(file)
    entities_2d = gmsh.model.occ.getEntities(2) # Aquí 3 significa que estamos listando volúmenes
    volumes = gmsh.model.occ.getEntities(dim=3)  # Aquí 3 significa que estamos listando volúmenes
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
    gmsh.model.occ.synchronize()
    return 
    
def get_collision_Mesh_top(file,totalHeight,numModules,percentageHeightBase,dimBase,origin_coord,meshResolution=0.1):
    heightModule=totalHeight/( (numModules*(1-percentageHeightBase)) + (numModules+1)*percentageHeightBase)
    heightBase=heightModule*percentageHeightBase
    heightVer=heightModule-heightBase
    gmsh.model.add("colissionMeshTop")
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", meshResolution)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", meshResolution)
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.model.occ.import_shapes(file)
    entities_2d = gmsh.model.occ.getEntities(2) # Aquí 3 significa que estamos listando volúmenes
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
    gmsh.model.occ.synchronize()
    return entities_2d

def Ankle(parentNode,config,name):
    Ankle = parentNode.addChild(name)
    from stlib3.physics.deformable import ElasticMaterialObject
    from stlib3.physics.constraints import FixedBox
    from softrobots.actuators import PullingCable
    from stlib3.physics.collision import CollisionMesh
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


def createScene(rootNode):
    import Config
    # -*- coding: utf-8 -*-
    from stlib3.scene import MainHeader,ContactHeader
    m = MainHeader(rootNode, plugins=["SoftRobots"])
    rootNode.VisualStyle.displayFlags = "showBehavior showCollisionModels"
    m.getObject("VisualStyle").displayFlags = 'showForceFields showBehaviorModels showInteractionForceFields'
    ContactHeader(rootNode, alarmDistance=1, contactDistance=0.5, frictionCoef=8)
    m.addObject('QPInverseProblemSolver', printLog=False)
    config=Config.Config()
    Ankle(rootNode,config,"Ankle")
    return rootNode