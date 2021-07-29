#!/usr/bin/pvpython
# trace generated using paraview version 5.9.0

#### import the simple module from the paraview
from paraview.simple import *
import os
import subprocess
g_

def read_data():
	subprocess.run(["pvdmake"])
	# create a new 'PVD Reader'
	pview_out_allpvd = PVDReader(registrationName='pview_out_all.pvd', FileName='/mnt/E46A96EC6A96BAAE/work/FEAP/feapnefm/taurus_rechnung/speedup/16proc/coarse/Results/pview_out_all.pvd')
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
	SaveScreenshot('./without_edges.png', renderView1, ImageResolution=[986, 481])

	# get active source.
	extractSelection1 = GetActiveSource()

	# get display properties
	extractSelection1Display = GetDisplayProperties(extractSelection1, view=renderView1)

	# change representation type
	extractSelection1Display.SetRepresentationType('Surface With Edges')

	# layout/tab size in pixels
	layout1.SetSize(986, 481)

	# current camera placement for renderView1
	renderView1.CameraPosition = [0.0008944676433444404, 0.012937819867921191, 0.0008607683051164721]
	renderView1.CameraFocalPoint = [0.0008944676433444404, -0.00164414046, 0.0008607683051164721]
	renderView1.CameraViewUp = [0.0, 0.0, 1.0]
	renderView1.CameraParallelScale = 0.0012860993104049244
	renderView1.CameraParallelProjection = 1

	# save screenshot
	SaveScreenshot('./with_edges.png', renderView1, ImageResolution=[986, 481])


#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

pview_out_allpvd,pview_out_allpvdDisplay,renderView1=read_data()

# set scalar coloring
#ColorBy(pview_out_allpvdDisplay, ('POINTS', 'phase', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
#HideScalarBarIfNotNeeded(vtkBlockColorsLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
#pview_out_allpvdDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
#pview_out_allpvdDisplay.SetScalarBarVisibility(renderView1, True)



# create a frustum selection of cells
extractSelection1,extractSelection1Display=select_lower_half(pview_out_allpvd, pview_out_allpvdDisplay)

# hide data in view
Hide(pview_out_allpvd, renderView1)

# update the view to ensure updated data information
renderView1.Update()



#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

# get layout
layout1 = GetLayout()

#--------------------------------
# saving layout sizes for layouts



make_screenshot(extractSelection1,extractSelection1Display)
