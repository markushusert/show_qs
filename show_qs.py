#!/usr/bin/pvpython
# trace generated using paraview version 5.9.0

#### import the simple module from the paraview
from paraview.simple import *
from paraview.vtk.numpy_interface import dataset_adapter as dsa
from paraview.vtk.numpy_interface import algorithms as algs
from paraview import servermanager as sm
from paraview.vtk.numpy_interface import dataset_adapter as dsa
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import sys
import subprocess
import getopt
import evaluate
g_script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(g_script_dir)
import mesh_data
import error_calculation
import paraview_interaction
import partitions
g_debugflag=False
g_dirs={"res":"Results","post":"Post"}
g_specimen_thickness=1.8*10**(-3)


def select_lower_half(pview_out_allpvd, pview_out_allpvdDisplay):
	#the following function was recorded in paraview and selects the lower half of the mesh, in order to create querschliff-pictures

	# get layout
	layout1 = GetLayout()


	#--------------------------------
	# saving layout sizes for layouts
	# layout/tab size in pixels
	layout1.SetSize(986, 481)

	
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
	#the following function was recorded in paraview and creates the crossection-pictures based one the selected lower half
	
	
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




def test_node_ids():
	
	test_iters={"r":mesh_data.g_mesh_data["r"]/2,"p":mesh_data.g_mesh_data["p"]/2,"z":mesh_data.g_mesh_data["z"]/2}
	print("test_iters"+str(test_iters))
	nodeid=mesh_data.get_node_id(test_iters)
	print("deducted-node: "+str(nodeid))
	node_iters=mesh_data.get_node_iter(nodeid)
	print("deducted iters"+str(node_iters))
def plot_results(post_dir,cut_iter_values,wez_iter_values):
	#plots the functions cut(z) and wez(z)
	#once with auto scaling and once with 1:1 aspect ratio
	#post_dir=directory to place plots as png
	#cut_iter_values=iterable(here np.array) of cut-widths of all iter_z-values
	#wez_iter_values=iterable(here np.array) of wez-widths of all iter_z-values
	plot_file=os.path.join(post_dir,"kerf_and_haz.png")
	equal_ratio_file=os.path.join(post_dir,"kerf_and_haz_equal.png")

	y_values=np.linspace(0,g_specimen_thickness,mesh_data.g_mesh_data["z"]+1)
	fig, ax = plt.subplots()
	linewidth=0.5
	handle_cut,=ax.plot(cut_iter_values,y_values,color="red",label="kerf",linewidth=linewidth)
	handle_wez,=ax.plot(wez_iter_values,y_values,color="blue",label="HAZ",linewidth=linewidth)
	plt.legend(handles=[handle_cut,handle_wez])

	ax.set_aspect('auto')
	fig.savefig(plot_file)

	ax.set_aspect('equal')
	fig.savefig(equal_ratio_file)


def write_results(filename,cut_iter_values,wez_iter_values):
	#writes calculated widths of cut and wez to given file
	#filename=filename to write to
	#cut_iter_values=iterable(here np.array) of cut-widths of all iter_z-values
	#wez_iter_values=iterable(here np.array) of wez-widths of all iter_z-values
	with open(filename,"w") as fil:
		cut_2d=np.reshape(cut_iter_values, (-1, 1))
		wez_2d=np.reshape(wez_iter_values, (-1, 1))
		data=np.concatenate((cut_2d,wez_2d),axis=1)
		np.savetxt(fil,data,header="cut; wez")

def main():
	#create all required dirs as empty, if not already present
	for dir in g_dirs.values():
		if not os.path.isdir(dir):
			os.makedirs(dir)
	
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

	#test_node_ids()
	
	iter_phi_qs=mesh_data.deduct_iter_phi_to_eval(error_calculation.g_qs_to_eval[0])
	if g_debugflag:
		print("iter_phi_of_qs="+str(iter_phi_qs))

	partition_node_dict=partitions.read_partitions(g_dirs['res'])
	partition_vtk_data_dict=partitions.split_vtkdata(pview_out_allpvd)

	mesh_data.deduct_element_length(partition_vtk_data_dict,partition_node_dict)

	energy_per_mat,volume_per_mat,energy_per_phase,volume_per_phase=evaluate.global_evaluation(partition_vtk_data_dict,partition_node_dict)
	error_calculation.write_global_stats(g_dirs['post'],energy_per_mat,volume_per_mat,energy_per_phase,volume_per_phase)

	#evaluation of a qs
	cut_iter_values,wez_iter_values=evaluate.get_wez_of_all_iters(iter_phi_qs,partition_node_dict,partition_vtk_data_dict)
	write_results(os.path.join(g_dirs['post'],"wez-values.txt"),cut_iter_values,wez_iter_values)
	plot_results(g_dirs['post'],cut_iter_values,wez_iter_values)

	schnitt_ges,wez_ges,delr,highest_uncut_iter_z=evaluate.get_wez(cut_iter_values,wez_iter_values)
	write_results(os.path.join(g_dirs['post'],"wez-layer.txt"),schnitt_ges,wez_ges)
	ratio_uncut=highest_uncut_iter_z/(mesh_data.g_mesh_data["z"]+1)
	#print(get_wez_of_iter_z(24,iter_phi_qs,partition_node_dict,partition_vtk_data_dict))
	if g_debugflag:
		print("schnitt="+str(schnitt_ges))
		print("wez="+str(wez_ges))
		print("delr="+str(delr))
		print("highest_uncut_iter_z="+str(highest_uncut_iter_z))

	error_laengs,error_quer=error_calculation.calculate_laengs_quer_error(wez_ges)
	
	error_wez,error_delr,error_schicht,error_ges=error_calculation.calulate_res_error(wez_ges,delr,ratio_uncut)
	error_calculation.write_error_file(g_dirs['post'],error_wez,error_delr,error_schicht,error_ges)
	error_calculation.write_signed_errors(error_laengs,error_quer,g_dirs['post'])
def parse_arguments():
	given_options=sys.argv[1:]
	parsed_options=getopt.getopt(given_options,"h",["help"])
	for arg,value in parsed_options[0]:
		if arg in ("-h","--help"):
			print_helptext()

def print_helptext():
	helptext=(
		"-------------------PROGRAM-DESCRIPTION----------------\n"
		"this program postprocesses the lasrcut-calculation by measuring wez and cut-width.\n"
		"using those values, it calculates the resulting errors.\n"
		"also pictures of the cross-section will be created.\n"
		"currently only the last available timestep is evaluated.\n"
		"\n"
		"usage:\n"
		"\tstart post program by executing \"show_qs.py\" in the folder from where you sent the calculation to the taurus.\n"
		"\n"
		"requirements:\n"
		"\tscript needs to be executed via pvpython, see the shebang"
		"\n"
		"required files:"
		"\tpartition_files: \"./Results/I_lasrcut_0001\" and so on\n"
		"\tparaview_files: \"*.vtu\""
		"\tMESH-file: \"./MESH_lasrcut\"\n"
		f"\tthe correct values of wez have to be indicated in {error_calculation.g_expected_result_file}"
	)
	print(helptext)
	exit()
if __name__ in ["__main__","__vtkconsole__"]:
	parse_arguments()
	main()
	pass
else:
	print("__name__="+__name__+" did not execute script")
