# -*- coding: utf-8 -*-
'''
Programa para crear una malla básica en GMSH usando la API de Python.

Por: Alejandro Hincapié G.º
'''

import gmsh

# %% Para comenzar a usar funciones de la API de GMSH se debe incializar:

gmsh.initialize()

# %% Con este comando se activa la opción de que GMSH imprima mensajes en la
#    consola, ya que por defecto no lo hace: 

gmsh.option.setNumber("General.Terminal", 1)

# %% Podemos crear un nuevo modelo con la siguiente línea. Esta línea es opcio-
#    nal, si no se usa el programa genera un modelo "Unnamed" por defecto.

gmsh.model.add("modelo_1")

# %% Se crean las primeras entidades: Los puntos (dimensión 0):

# En este programa se usará el kernel de geometría que trae por defecto el
# GMSH, no es el único, pero para este caso funciona bastante bien.

# Sintaxis: gmsh.model.geo.addPoint(x, y, z, tm, tag)
#           tm = Tamaño de malla en el punto

tm = 2  # Tamaño de malla a utilizar en todos los puntos
tmr = 0.3  # Tamaño de malla refinada (alrededor del agujero)

P1=gmsh.model.occ.addPoint(0,  0,  0, tm, 1)  # Punto 1 coord (0,0,0)
P2=gmsh.model.occ.addPoint(40, 0,  0, tm, 2)  # Punto 2 coord (40,0,0) ...
P3=gmsh.model.occ.addPoint(40, 20, 0, tm, 3)
P4=gmsh.model.occ.addPoint(0,  20, 0, tm, 4)

# Se deben definir 3 puntos que permitan crear luego el círculo. El centro, un
# punto a la izquierda y otro a la derecha:

r = 3  # radio del círculo

P5=gmsh.model.occ.addPoint(20, 10, 0, tm, 5)    # Punto central del círculo
P6=gmsh.model.occ.addPoint(20+r, 10, 0, tmr, 6)
P7=gmsh.model.occ.addPoint(20-r, 10, 0, tmr, 7)

# %% Se crean las siguientes entidades: Las curvas (dimensión 1):

# Primero las líneas rectas de los bordes:
# Sintaxis: gmsh.model.geo.addLine(punto inicial, punto final, tag)

gmsh.model.occ.addLine(P1, P2, 1)  # Éste sería el borde inferior
gmsh.model.occ.addLine(P2, P3, 2)  # ...
gmsh.model.occ.addLine(P3, P4, 3)
gmsh.model.occ.addLine(P4, P1, 4)

# Ahora los arcos de circunferencia para el agujero (se deben crear 2 arcos, ya
# que el kernel built-in no permite crear arcos con un ángulo mayor a 180°)
# Sintaxis: gmsh.model.geo.addCircle(p. inicial, p. centro, p. final, tag)

gmsh.model.occ.addCircleArc(P6, P5, P7, P5)  # Arco superior
gmsh.model.occ.addCircleArc(P7, P5, P6, P6)  # Arco inferior

# %% Ahora se define la siguiente entidad: La superficie (dimensión 2):

# Para definir superficies, primero se deben definir 'Curve Loops' que las
# limiten. En este caso un Curve Loop será el borde exterior, y el otro será
# el agujero.

gmsh.model.occ.addCurveLoop([1, 2, 3, 4], 1)
gmsh.model.occ.addCurveLoop([5, 6], 2)

# Ahora sí se puede definir la superficie, así:
#Sintaxis: gmsh.model.geo.addPlaneSurface([Lista de Curve Loops], tag), donde:
#          En la lista de Curve Loops el primer elemento es el loop que define
#          el contorno de la superficie, los demás son agujeros dentro de ella.

gmsh.model.occ.addPlaneSurface([1, 2], 1)

# %% Ahora se crean los grupos físicos que se requieran
#Por defecto, si hay grupos físicos definidos, GMSH solo reporta elementos fini-
#tos que pertenezcan a algún grupo físico. En este caso se crearán dos:
#    - Una superficie física que contenga nuestra superficie creada
#    - Una curva física que contenga el borde inferior

# Sintaxis: gmsh.model.addPhysicalGroup(dimensión, lista de entidades, tag)

s = gmsh.model.addPhysicalGroup(2, [1]) # En este caso no se especifica tag
gmsh.model.setPhysicalName(2, s, "Mi superficie")  # Se puede definir un nombre

gmsh.model.addPhysicalGroup(1, [1], 101)  # Puedo especificar tag manualmente 
gmsh.model.setPhysicalName(1, 101, "Borde inferior")

# %% Antes de mallar, se debe sincronizar la representación CAD del GMSH con el
#    modelo actual:

gmsh.model.occ.synchronize()

# %% Ahora sí se procede a crear la malla:

gmsh.model.mesh.generate(2)

gmsh.option.setNumber('Mesh.SurfaceFaces', 1)  # Ver las "caras" de los elementos finitos 2D
gmsh.option.setNumber('Mesh.Points', 1)        # Ver los nodos de la malla


# Y finalmente guardar la malla
filename = 'ejm_1.msh'
gmsh.write(filename)

# Podemos visualizar el resultado en la interfaz gráfica de GMSH
gmsh.fltk.run()

# %% Tras finalizar el proceso se recomienda usar este comando
gmsh.finalize()

# %% Podemos graficar la malla para ver el resultado:

# from leer_GMSH import plot_msh  # Funciones para leer y graficar la malla

# plot_msh(filename, '2D', True, True, True)