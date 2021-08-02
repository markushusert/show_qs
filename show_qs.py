#!/usr/bin/pvpython
# trace generated using paraview version 5.9.0

#### import the simple module from the paraview
from paraview.simple import *
from paraview.vtk.numpy_interface import dataset_adapter as dsa
from paraview.vtk.numpy_interface import algorithms as algs
from paraview import servermanager as sm
from paraview.vtk.numpy_interface import dataset_adapter as dsa
import os
import subprocess
g_script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(g_script_dir)
import mesh_data
import error_calculation

g_dirs={"res":"Results","post":"Post"}

def read_data():
	os.chdir(g_dirs['res'])
	subprocess.run(["pvdmake"])
	os.chdir('../')
	# create a new 'PVD Reader'
	data_path=os.path.join(g_dirs['res'],'pview_out_all.pvd')
	
	pview_out_allpvd = PVDReader(registrationName='pview_out_all.pvd', FileName=data_path)
	pview_out_allpvd.PointArrays = ['temperatur',  'maxtemp', 'phase',  'evaporation']

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')

	# show data in view
	pview_out_allpvdDisplay = Show(pview_out_allpvd, renderView1,representationType='UnstructuredGridRepresentation')
	
	# get the material library
	materialLibrary1 = GetMaterialLibrary()

	# update the view to ensure updated data information
	renderView1.Update()

	
	return pview_out_allpvd, pview_out_allpvdDisplay,renderView1
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
def debugfun(pview_out_allpvd,pview_out_allpvdDisplay):
	print(type(pview_out_allpvd))
	print(type(pview_out_allpvdDisplay))
	print(pview_out_allpvd.PointData.keys())
	#print(type(pview_out_allpvd.PointData.VTKObject))
	#print(type(pview_out_allpvdDisplay.PointData.VTKObject))
	fieldinfo=pview_out_allpvd.GetPointDataInformation()
	print(fieldinfo)
	phasearrayinfo=fieldinfo['phase']
	print(type(phasearrayinfo))
	vtk_data = sm.Fetch(pview_out_allpvd)
	print("vtk data after fetch:"+str(type(vtk_data)))
	vtk_data = dsa.WrapDataObject(vtk_data)
	print("vtk data wrap:"+str(type(vtk_data)))
	phasedata = vtk_data.PointData['phase']
	print("phasedata:"+str(type(phasedata))+", shape:"+str(algs.shape(phasedata)))
	nr_blocks=vtk_data.GetNumberOfBlocks()
	print("number of blocks"+str(nr_blocks))
	grid=vtk_data.GetBlock(0).GetBlock(0)
	print("grid:"+str(type(grid)))	
	coordinates=grid.GetPoints()
	print("coordinates:"+str(type(coordinates))+", shape:"+str(algs.shape(coordinates)))
	print("number of points:"+str(coordinates.GetNumberOfPoints()))
	print("first point"+str(coordinates.GetPoint(0)))
	print("second point"+str(coordinates.GetPoint(1)))
	pointdata_of_block=grid.GetPointData ()
	print("pointdata of block"+str(type(pointdata_of_block)))
	phasedata_of_block=pointdata_of_block.GetAbstractArray('phase')
	print("phasedata of block"+str(type(phasedata_of_block))+", shape:"+str(algs.shape(phasedata_of_block)))
	print("phase of first point in block"+str(phasedata_of_block.GetTuple(0)))
	phasedata_of_block_w=dsa.WrapDataObject(phasedata_of_block)
	print("phasedata of block wrapped"+str(type(phasedata_of_block_w)))
	pointdata_of_block_w=dsa.WrapDataObject(pointdata_of_block)
	print("pointdata of block wrapped"+str(type(pointdata_of_block)))

	number_of_points_accum=0
	for iter_block in range(vtk_data.GetNumberOfBlocks()):
		blockdata=vtk_data.GetBlock(iter_block).GetBlock(0)
		number_of_points=blockdata.GetPoints().GetNumberOfPoints()
		number_of_points_accum+=number_of_points
		print("block "+str(iter_block)+" contains "+str(number_of_points)+" points")
	print("number of points accumulated over all blocks: "+str(number_of_points_accum))
	#print("number of blocks of coordinates"+str(coordinates.GetNumberOfBlocks()))
def main():
	global renderView1
	for dir in g_dirs.values():
		if not os.path.isdir(dir):
			os.makedirs(dir)
	
	#### disable automatic camera reset on 'Show'
	paraview.simple._DisableFirstRenderCameraReset()

	pview_out_allpvd,pview_out_allpvdDisplay,renderViewtemp=read_data()
	renderView1=renderViewtemp

	#the following 2 functions are an example of accessing the data stored in the vtu-files
	if True:
		debugfun(pview_out_allpvd,pview_out_allpvdDisplay)
	

	exit()
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
