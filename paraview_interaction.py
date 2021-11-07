import os
from paraview.simple import *
from paraview.vtk.numpy_interface import dataset_adapter as dsa
from paraview.vtk.numpy_interface import algorithms as algs
from paraview import servermanager as sm
from paraview.vtk.numpy_interface import dataset_adapter as dsa
import subprocess

def read_data(data_dir):
	#function reads *.vtu files in data_dir into paraview
	#it first executes arnes pvdmake-script
	#then reads the pvdfile into paraview
	#returns data-object,display-object,and current view

	if not os.path.isdir(data_dir):
		print(".vtu-Files are expected to lie in "+os.path.abspath(data_dir))
		print("which does not exist")
		exit(1)
	os.chdir(data_dir)
	try:
		subprocess.run(["pvdmake"])
	except:
		print("error running pvdmake in "+os.path.abspath(data_dir))
		print("make sure pvdmake is executable and the dir contains vtu-files")
		raise Exception
	os.chdir('../')


	# create a new 'PVD Reader'
	data_path=os.path.join(data_dir,'pview_out_all.pvd')
	
	pview_out_allpvd = PVDReader(registrationName='pview_out_all.pvd', FileName=data_path)
	pview_out_allpvd.PointArrays = ['temperatur',  'maxtemp', 'phase',  'evaporation', 'energie']

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')
	
	#set time to last timestep
	renderView1.ViewTime=pview_out_allpvd.TimestepValues[-1]
	# show data in view
	pview_out_allpvdDisplay = Show(pview_out_allpvd, renderView1,representationType='UnstructuredGridRepresentation')
	
	# get the material library
	materialLibrary1 = GetMaterialLibrary()

	# update the view to ensure updated data information
	renderView1.Update()

	
	return pview_out_allpvd, pview_out_allpvdDisplay,renderView1