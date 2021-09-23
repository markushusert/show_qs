import glob
from paraview.simple import *
from paraview.vtk.numpy_interface import dataset_adapter as dsa
from paraview.vtk.numpy_interface import algorithms as algs
from paraview import servermanager as sm, vtk
from paraview.vtk.numpy_interface import dataset_adapter as dsa
from collections import defaultdict
import os
import inspect
import sys
global nr_partitions

import collections
class KeyBasedDefaultDict(collections.defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = self.default_factory(key)
        return self[key]

def read_partitions(Resultdir):
    #
    #Reads partition data from
    #
    
    #! dict of type: {global_id:[(partion_id1,lokal_id1),..,(partion_idn,lokal_idn)]}
    #where global_id is the global id of a node, who belongs to n partitions (see Ghost-nodes)

    list_of_partition_files=get_partition_files(Resultdir)
    print("reading partition data")
    if len(list_of_partition_files):
        node_partition=defaultdict(list)
        #parallele rechnung
        for partition_file in list_of_partition_files:
            read_partition_file(partition_file,node_partition)
    else:
        def get_default_partition(nodeid):
            return [(1,nodeid)]
        node_partition=KeyBasedDefaultDict(get_default_partition)
        pass
    return node_partition
def get_partition_files(Resultdir):
    partition_files_pattern=os.path.join(Resultdir,"I_*"+"[0-9]"*4)
    return glob.glob(partition_files_pattern)

def read_partition_file(partition_file,node_partition):
    #node_partition=defaultdict of type list, to be filled with partition data from each file
    #matches each global-node to a list of tuples of its partitions and local ids
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

def get_array_value_of_global_id(node_partition,data_split_into_partitions,global_id,arrayname):
    #node_partition: dict as returned by read_partitions
    #data_split_into_partitions: dict as returned by split_vtkdata()

    #one global node may exist in several partitions (ghost nodes)

    local_adresses_of_global_node=node_partition[global_id]
    set_of_array_values=set()
    for partition_id,local_id in local_adresses_of_global_node:
        partition_data=data_split_into_partitions[partition_id]
        if arrayname=="coords":
            array_value=partition_data[1].GetPoint(local_id-1)
        else:
            array_value=partition_data[0].GetAbstractArray(arrayname).GetTuple(local_id-1)
        if False: #no checking the other occurences, since all ghost nodes should have the same value
            return array_value
        else:
            set_of_array_values.add(array_value)

    
    if len(set_of_array_values)>1:
        print("ERROR, different values for ghost nodes of global node"+str(global_id))
        print("partitions and local nodes: "+str(local_adresses_of_global_node))
        print("detected values: "+str(set_of_array_values))
    elif len(set_of_array_values)==0:
        print("ERROR no data found for node "+str(global_id))
    else:
        for value in set_of_array_values:
            return value


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
    print(str(type(vtk_data)))
    #if serial calculation we do not have a composite dataset but a unstructuredgrid directly
    if str(type(vtk_data)).endswith("vtkUnstructuredGrid'>"):
        return_dict={}
        return_dict[1]=(vtk_data.GetPointData(),vtk_data.GetPoints())
        return return_dict
    else:
        vtk_data = dsa.WrapDataObject(vtk_data)
        
        nr_parts = vtk_data.GetNumberOfBlocks()
        return_dict={}
        for i_part in range(1,nr_parts+1):
            blockdata=vtk_data.GetBlock(i_part-1).GetBlock(0) #for some reason each block contains a single block in itself
            mesh_data=blockdata.GetPoints()
            array_data=blockdata.GetPointData()
            return_dict[i_part]=(array_data,mesh_data)
        return return_dict



    




