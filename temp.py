import os
import math
import subprocess
from paraview.simple import *
def select_lower_half(pview_out_allpvd):
	layout = GetLayout()
	layoutsize=layout.GetSize()
	SelectCellsThrough(Rectangle=[0, 0, layoutsize[0], int(layoutsize[1]/2)])
	extractSelection1 = ExtractSelection(registrationName='ExtractSelection1', Input=pview_out_allpvd)
	extractSelection1Display = Show(extractSelection1, GetActiveView(),representationType='UnstructuredGridRepresentation')
	# set scalar coloring
	ColorBy(extractSelection1Display, ('POINTS', 'phase', 'Magnitude'))
	return extractSelection1,extractSelection1Display
def set_camera_to_show_angled_draufsicht(angle):
	angle_plane=angle/180*math.pi
	angle_normal=angle_plane+math.pi/2
	camera=GetActiveCamera()
	camera.SetPosition((0,0,1))
	#commented line to watch on the plane
	#camera.SetPosition((math.sin(angle_normal),math.cos(angle_normal),oldheight))
	camera.SetViewUp((math.sin(angle_normal),math.cos(angle_normal),0))
	Render()
def set_camera_to_normal_to_cutting_plane(angle):
	angle_plane=angle/180*math.pi
	angle_normal=angle_plane+math.pi/2
	camera=GetActiveCamera()
	camera.SetPosition((math.sin(angle_normal),math.cos(angle_normal),0.9*10**(-3)))
	camera.SetViewUp((0,0,1))
	ResetCamera()
	camera.Zoom(2.5)
	Render()
def create_pngs(Selectiondisplay):
	renderView1 = GetActiveViewOrCreate('RenderView')
	layout=GetLayout()
	layoutsize=layout.GetSize()
	Selectiondisplay.SetRepresentationType('Surface')
	SaveScreenshot('without_edges.png', renderView1, ImageResolution=list(layoutsize))

	Selectiondisplay.SetRepresentationType('Surface With Edges')
	SaveScreenshot('with_edges.png', renderView1, ImageResolution=list(layoutsize))
def make_screenshot_of_angle(angle,pview_out_allpvd):
	#rotate mesh around z-axis
	set_camera_to_show_angled_draufsicht(angle)
	#select all elements in the lower half of the screen
	selection,selectiondisplay=select_lower_half(pview_out_allpvd)
	#hide original source
	renderView1 = GetActiveViewOrCreate('RenderView')
	Hide(pview_out_allpvd, renderView1)
	
	set_camera_to_normal_to_cutting_plane(angle)
	create_pngs(selectiondisplay)
	#delete selection after creating screenshot
	Delete(selection)
	del selection
	#show full data again
	Show(pview_out_allpvd, renderView1,representationType='UnstructuredGridRepresentation')
def read_data(data_dir):
	#function reads *.vtu files in data_dir into paraview
	#it first executes arnes pvdmake-script
	#then reads the pvdfile into paraview
	#returns data-object,display-object,and current view

	if not os.path.isdir(data_dir):
		print(".vtu-Files are expected to lie in "+os.path.abspath(data_dir))
		print("which does not exist")
		exit(1)
	try:
		subprocess.run(["pvdmake"],cwd=data_dir)
	except:
		print("error running pvdmake in "+os.path.abspath(data_dir))
		print("make sure pvdmake is executable and the dir contains vtu-files")
		raise Exception


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

def main():
	pview_out_allpvd, pview_out_allpvdDisplay,renderView1=read_data(os.getcwd())
	angle=45
	make_screenshot_of_angle(angle,pview_out_allpvd)
main()