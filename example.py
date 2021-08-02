#!/usr/bin/pvpython
import paraview_interaction
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
import paraview_interaction
import partitions

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
	pointdata_of_block=grid.GetPointData()
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
	
	resultdir="Results"
	pview_out_allpvd,pview_out_allpvdDisplay,renderView1=paraview_interaction.read_data(resultdir)
	debugfun(pview_out_allpvd,pview_out_allpvdDisplay)
	partitions.g_partition_dict=partitions.read_partitions(resultdir)
	print("partitions of node 1")
	print(partitions.g_partition_dict[1])


	partitioned_data=partitions.split_vtkdata(pview_out_allpvd)
	local_nodes_to_print=100
	for key,value in partitioned_data.items():
		for local_id in range(local_nodes_to_print):
			try:
				position=value[1].GetPoint(local_id)
				array=value[0].GetAbstractArray('phase').GetTuple(local_id)
				print("partition "+str(key)+", local node"+str(local_id)+", array value"+str(array)+", position"+str(position))
			except ValueError:
				break
		
		

if __name__=="__main__":
    main()
