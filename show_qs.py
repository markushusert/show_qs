#!/usr/bin/pvpython
# trace generated using paraview version 5.9.0

#### import the simple module from the paraview
from paraview.simple import *
from paraview.vtk.numpy_interface import dataset_adapter as dsa
from paraview.vtk.numpy_interface import algorithms as algs
from paraview import servermanager as sm
from paraview.vtk.numpy_interface import dataset_adapter as dsa

import os
import sys
import subprocess
g_script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(g_script_dir)
import mesh_data
import error_calculation
import paraview_interaction
import partitions
g_dirs={"res":"Results","post":"Post"}


def select_lower_half(pview_out_allpvd, pview_out_allpvdDisplay):

	#================================================================
	# addendum: following script captures some of the application
	# state to faithfully reproduce the visualization during playback
	#================================================================

	# get layout
	layout1 = GetLayout()


	#--------------------------------
	# saving layout sizes for layouts
	# layout/tab size in pixels
	layout1.SetSize(986, 481)


	#-----------------------------------
	# saving camera placements for views

	
	# get color transfer function/color map for 'phase'
	phaseLUT = GetColorTransferFunction('phase')

	# get opacity transfer function/opacity map for 'phase'
	phasePWF = GetOpacityTransferFunction('phase')
	# current camera placement for renderView1
	renderView1=GetActiveViewOrCreate('RenderView')
	renderView1.CameraPosition = [-1.4999999999910918e-08, 0.0006569049999999999, 0.017495072677959484]
	renderView1.CameraFocalPoint = [-1.4999999999910918e-08, 0.0006569049999999999, 0.0009]
	renderView1.CameraParallelScale = 0.004295120863916405
	renderView1.CameraParallelProjection = 1
	
	# create a frustum selection of cells
	SelectCellsThrough(Rectangle=[292, 46, 709, 207])
	
	# create a new 'Extract Selection'
	extractSelection1 = ExtractSelection(registrationName='ExtractSelection1', Input=pview_out_allpvd)

	# show data in view
	extractSelection1Display = Show(extractSelection1, renderView1,representationType='UnstructuredGridRepresentation')

	# trace defaults for the display properties.
	extractSelection1Display.Representation = 'Surface'
	extractSelection1Display.ColorArrayName = ['POINTS', 'phase']
	extractSelection1Display.LookupTable = phaseLUT
	extractSelection1Display.SelectTCoordArray = 'None'
	extractSelection1Display.SelectNormalArray = 'None'
	extractSelection1Display.SelectTangentArray = 'None'
	extractSelection1Display.OSPRayScaleArray = 'alpha'
	extractSelection1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	extractSelection1Display.SelectOrientationVectors = 'None'
	extractSelection1Display.ScaleFactor = 0.000655985
	extractSelection1Display.SelectScaleArray = 'None'
	extractSelection1Display.GlyphType = 'Arrow'
	extractSelection1Display.GlyphTableIndexArray = 'None'
	extractSelection1Display.GaussianRadius = 3.279925e-05
	extractSelection1Display.SetScaleArray = ['POINTS', 'alpha']
	extractSelection1Display.ScaleTransferFunction = 'PiecewiseFunction'
	extractSelection1Display.OpacityArray = ['POINTS', 'alpha']
	extractSelection1Display.OpacityTransferFunction = 'PiecewiseFunction'
	extractSelection1Display.DataAxesGrid = 'GridAxesRepresentation'
	extractSelection1Display.PolarAxes = 'PolarAxesRepresentation'
	extractSelection1Display.ScalarOpacityFunction = phasePWF
	extractSelection1Display.ScalarOpacityUnitDistance = 0.00012402779707906166
	extractSelection1Display.OpacityArrayName = ['POINTS', 'alpha']
	extractSelection1Display.ExtractedBlockIndex = 2

	# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
	extractSelection1Display.OSPRayScaleFunction.Points = [-752.89, 0.0, 0.5, 0.0, 79980.0, 1.0, 0.5, 0.0]

	# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
	extractSelection1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 6.78214e-07, 1.0, 0.5, 0.0]

	# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
	extractSelection1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 6.78214e-07, 1.0, 0.5, 0.0]

	ColorBy(extractSelection1Display, ('POINTS', 'phase', 'Magnitude'))

	# show color bar/color legend
	extractSelection1Display.SetScalarBarVisibility(renderView1, True)
	
	return extractSelection1,extractSelection1Display
	
def make_screenshot(extractSelection1,extractSelection1Display):
	#### disable automatic camera reset on 'Show'
	paraview.simple._DisableFirstRenderCameraReset()

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')

	# get layout
	layout1 = GetLayout()

	# layout/tab size in pixels
	layout1.SetSize(986, 481)

	# current camera placement for renderView1
	renderView1.CameraPosition = [0.0008944676433444404, 0.012937819867921191, 0.0008607683051164721]
	renderView1.CameraFocalPoint = [0.0008944676433444404, -0.00164414046, 0.0008607683051164721]
	renderView1.CameraViewUp = [0.0, 0.0, 1.0]
	renderView1.CameraParallelScale = 0.0012860993104049244
	renderView1.CameraParallelProjection = 1

	# save screenshot
	SaveScreenshot(os.path.join(g_dirs['post'],'without_edges.png'), renderView1, ImageResolution=[986, 481])

	# get active source.
	extractSelection1 = GetActiveSource()

	# get display properties
	extractSelection1Display = GetDisplayProperties(extractSelection1, view=renderView1)

	# change representation type
	extractSelection1Display.SetRepresentationType('Surface With Edges')

	# save screenshot
	SaveScreenshot(os.path.join(g_dirs['post'],'with_edges.png'), renderView1, ImageResolution=[986, 481])
def get_wez_of_layer(layer_number,iter_phi_qs,pipeline_object):
	nr_ele_per_layer=mesh_data.g_mesh_data["z"]/12
	iter_z_start=1+(layer_number-1)*nr_ele_per_layer
	iter_z_end=1+(layer_number)*nr_ele_per_layer

	for iter_z in range(iter_z_start,iter_z_end):
		if iter_z in [iter_z_start,iter_z_end]:
			weight=0.5
		else:
			weight=1.0
		get_wez_of_iter_z(iter_z,iter_phi_qs,pipeline_object)

def get_wez_of_iter_z(iter_z,iter_phi_qs,pipeline_object):
	
	iter_r_half=int(1+mesh_data.g_mesh_data["r"]/2)
	iter_r_end=1+mesh_data.g_mesh_data["r"]

	if True:
		print("pipeline_object="+str(pipeline_object))
		print(type(pipeline_object))
		print(pipeline_object.VTKObject)
		print("point_data available:"+str(pipeline_object.PointData.keys()))
		phase_data=pipeline_object.PointData['phase']
		print("shape of data:")
		print(algs.shape(phase_data))
		print("type of data:")
		print(type(phase_data))

	for iter_r in range(iter_r_half,iter_r_end):
		iter_dict={"r":iter_r,"p":iter_phi_qs,"z":iter_z}
		nodeid=mesh_data.get_node_id(iter_dict)
		print("phase of iters:"+str(iter_dict)+"is"+phase_data[nodeid-1])

def test_node_ids():
	
	test_iters={"r":mesh_data.g_mesh_data["r"]/2,"p":mesh_data.g_mesh_data["p"]/2,"z":mesh_data.g_mesh_data["z"]/2}
	print("test_iters"+str(test_iters))
	nodeid=mesh_data.get_node_id(test_iters)
	print("deducted-node: "+str(nodeid))
	node_iters=mesh_data.get_node_iter(nodeid)
	print("deducted iters"+str(node_iters))

def main():
	for dir in g_dirs.values():
		if not os.path.isdir(dir):
			os.makedirs(dir)

	#the following 2 functions are an example of accessing the data stored in the vtu-files
	
	#### disable automatic camera reset on 'Show'
	paraview.simple._DisableFirstRenderCameraReset()

	pview_out_allpvd,pview_out_allpvdDisplay,renderView1=paraview_interaction.read_data(g_dirs['res'])
	# create a frustum selection of cells
	extractSelection1,extractSelection1Display=select_lower_half(pview_out_allpvd, pview_out_allpvdDisplay)

	# hide data in view
	Hide(pview_out_allpvd, renderView1)

	# update the view to ensure updated data information
	renderView1.Update()

	make_screenshot(extractSelection1,extractSelection1Display)
	mesh_data.read_mesh_data()

	test_node_ids()
	
	iter_phi_qs=mesh_data.deduct_iter_phi_to_eval(error_calculation.g_phiqs)
	print("iter_phi_of_qs="+str(iter_phi_qs))
	get_wez_of_iter_z(1,iter_phi_qs,pview_out_allpvd)

	
if __name__ in ["__main__","__vtkconsole__"]:
	main()
	pass
else:
	print("__name__="+__name__+" did not execute script")
