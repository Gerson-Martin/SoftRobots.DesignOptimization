# -*- coding: utf-8 -*-
'''
Programa para crear una malla básica en GMSH usando la API de Python.

Por: Alejandro Hincapié G.º
'''

import gmsh
import numpy as np

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

gmsh.model.geo.addPoint(0,  0,  0, tm, 1)  # Punto 1 coord (0,0,0)
gmsh.model.geo.addPoint(0, 50,  0, tm, 2)  # Punto 2 coord (40,0,0) ...
gmsh.model.geo.addPoint(10, 50, 0, tm, 3)
gmsh.model.geo.addPoint(10,  40, 0, tm, 4)
gmsh.model.geo.addPoint(20,  40,  0, tm, 5)  # Punto 1 coord (0,0,0)
gmsh.model.geo.addPoint(20, 50,  0, tm, 6)  # Punto 2 coord (40,0,0) ...
gmsh.model.geo.addPoint(30, 50, 0, tm, 7)
gmsh.model.geo.addPoint(30,  0, 0, tm, 8)

# Se deben definir 3 puntos que permitan crear luego el círculo. El centro, un
# punto a la izquierda y otro a la derecha:


# %% Se crean las siguientes entidades: Las curvas (dimensión 1):

# Primero las líneas rectas de los bordes:
# Sintaxis: gmsh.model.geo.addLine(punto inicial, punto final, tag)

gmsh.model.geo.addLine(1, 2, 1)  # Éste sería el borde inferior
gmsh.model.geo.addLine(2, 3, 2)  # ...
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 5, 4)
gmsh.model.geo.addLine(5, 6, 5)  # Éste sería el borde inferior
gmsh.model.geo.addLine(6, 7, 6)  # Éste sería el borde inferior
gmsh.model.geo.addLine(7, 8, 7)  # ...
gmsh.model.geo.addLine(8, 1, 8)


# %% Ahora se define la siguiente entidad: La superficie (dimensión 2):

# Para definir superficies, primero se deben definir 'Curve Loops' que las
# limiten. En este caso un Curve Loop será el borde exterior, y el otro será
# el agujero.

gmsh.model.geo.addCurveLoop([1, 2, 3, 4, 5, 6, 7, 8], 1)
SurfaceTag =gmsh.model.geo.addPlaneSurface([1],1)
#    modelo actual:
RevolveDimTags = gmsh.model.geo.revolve([(1,SurfaceTag)], 0,0,0, 1,0,0, np.pi)

gmsh.model.geo.synchronize()

# %% Ahora sí se procede a crear la malla:

gmsh.model.mesh.generate(1)


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