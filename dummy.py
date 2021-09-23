#!/usr/bin/pvpython
# trace generated using paraview version 5.9.0

#### import the simple module from the paraview
from paraview.simple import *
import os
import mesh_data
import error_calculation
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()
resultdir="Results"
filename='temp.vtu'

mesh_data.read_mesh_data()

abspath=os.path.join(os.getcwd(),resultdir,filename)
# create a new 'XML Unstructured Grid Reader'
data = XMLUnstructuredGridReader(registrationName=filename, FileName=[abspath])
data.PointArrayStatus = ['temperatur', 'heat_ext', 'volumen', 'alpha', 'maxtemp', 'phase', 'energie', 'heatflow', 'evaporation']

# Properties modified on data
data.PointArrayStatus = ['phase']

data.UpdatePipeline()

#read mesh data
mesh_data.g_mesh_data=mesh_data.read_mesh_data()
nodeid=mesh_data.get_node_id({"r":mesh_data.g_mesh_data["r"]/2,"p":mesh_data.g_mesh_data["p"]/2,"z":mesh_data.g_mesh_data["z"]/2})
print("deducted-none: "+str(nodeid))

