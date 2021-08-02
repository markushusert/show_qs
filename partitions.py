import glob
from paraview.simple import *
from paraview.vtk.numpy_interface import dataset_adapter as dsa
from paraview.vtk.numpy_interface import algorithms as algs
from paraview import servermanager as sm
from paraview.vtk.numpy_interface import dataset_adapter as dsa
from collections import defaultdict
import os
import inspect
import sys
global nr_partitions
def read_partitions(Resultdir):
    #
    #Reads partition data from
    #
    node_partition=defaultdict(list)
    #! dict of type: {global_id:[(partion_id1,lokal_id1),..,(partion_idn,lokal_idn)]}
    #where global_id is the global id of a node, who belongs to n partitions (see Ghost-nodes)

    list_of_partition_files=get_partition_files(Resultdir)
    print("reading partition data")
    for partition_file in list_of_partition_files:
        read_partition_file(partition_file,node_partition)
    return node_partition
def get_partition_files(Resultdir):
    partition_files_pattern=os.path.join(Resultdir,"I_*"+"[0-9]"*4)
    return glob.glob(partition_files_pattern)

def read_partition_file(partition_file,node_partition):
    #node_partition=defaultdict of type list, to be filled with partition data from each file
    found_partition=False
    partition_id=int(partition_file.rsplit("_",1)[1])
    print("reading partition of: "+partition_file)
    with open(partition_file,"r") as fil:
        for line in fil:
            if line=="LOCAl to GLOBal node numbers\n":
                found_partition=True
                continue
            if found_partition:
                if line=="\n":
                    break
                linesplit=line.split()
                local_node=int(linesplit[0])
                global_node=int(linesplit[1])
                node_partition[global_node].append((partition_id,local_node))

def split_vtkdata(pvdreader):
    #splits pvdreader into mesh-and array data for each partition
    #returns dict of structure: {partition_id:(array_data,mesh_data)}
    #where mesh_data is of type:vtkmodules.vtkCommonCore.vtkPoints, and can be accessed like this
    #   mesh_data.GetPoint(n) returns a tuple of the coordinates of the nth local node
    #and array_data is of type:vtkmodules.vtkCommonDataModel.vtkPointData and can be accessed like this
    #   array_data.GetAbstractArray('array_name').GetTuple(n) returns all dimensions of 'array_name' at the nth local node

    #print(inspect.getsource(type(pvdreader)))
    if str(type(pvdreader))!="<class \'paraview.servermanager.PVDReader\'>":
        #i have only tried with this reader, but may also work with others
        print("input of function splot_vtkdata should be of type paraview.servermanager.PVDReader")
        print("instead got a "+str(type(pvdreader)))
        exit(1)


    vtk_data = sm.Fetch(pvdreader)
    vtk_data = dsa.WrapDataObject(vtk_data)
    nr_parts = vtk_data.GetNumberOfBlocks()
    return_dict={}
    for i_part in range(1,nr_parts+1):
        blockdata=vtk_data.GetBlock(i_part-1).GetBlock(0) #for some reason each block contains a single block in itself
        mesh_data=blockdata.GetPoints()
        array_data=blockdata.GetPointData()
        return_dict[i_part]=(array_data,mesh_data)
    
    return return_dict



    




