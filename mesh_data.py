import sys
import os
import math
import glob
g_input_dir=os.getcwd()
g_mesh_file="MESH_lasrcut"

def read_mesh_data():
    global g_mesh_data
    with open(g_mesh_file,"r") as fil:
        lines=fil.readlines()
    g_mesh_data={key:None for key in ["r","p","z","start","dp_in","np_in"]}
    for line in lines:
        if line.lstrip().startswith("cmes"):
            for key in g_mesh_data.keys():
                arguments=line.split(",")
                if arguments[1]==key:
                    if key=="start":#start needed to find start of phi-variable
                        idx_to_read=3
                        g_mesh_data[key]=float(arguments[idx_to_read])
                    else:
                        idx_to_read=2
                        g_mesh_data[key]=int(arguments[idx_to_read])
                    if key=="p":
                        g_mesh_data["dp_in"]=float(arguments[5])#inner area of phi
                        g_mesh_data["np_in"]=float(arguments[3])#number of elemnts in inner area

def get_ele_iter(ele_id):
    id_dict={key:None for key in ["r","p","z"]}
    id_dict["r"]=(ele_id-1)%g_mesh_data["r"]+1
    id_dict["p"]=math.floor(((ele_id-1)/g_mesh_data["r"]))%g_mesh_data["p"]+1
    id_dict["z"]=math.floor(((ele_id-1)/g_mesh_data["r"])/g_mesh_data["p"])%g_mesh_data["z"]+1
    return id_dict
def get_ele_id(ele_id_dict):
    ele_id=ele_id_dict["r"]+(ele_id_dict["p"]-1)*g_mesh_data["r"]+(ele_id_dict["z"]-1)*g_mesh_data["r"]*g_mesh_data["p"]
    return ele_id

def get_node_id(node_id_dict):
    node_id=node_id_dict["r"]+(node_id_dict["p"]-1)*(g_mesh_data["r"]+1)+(node_id_dict["z"]-1)*(g_mesh_data["r"]+1)*g_mesh_data["p"]
    return node_id
def get_node_iter(node_id):
    id_dict={key:None for key in ["r","p","z"]}
    id_dict["r"]=(node_id-1)%(g_mesh_data["r"]+1)+1
    id_dict["p"]=math.floor(((node_id-1)/(g_mesh_data["r"]+1)))%g_mesh_data["p"]+1
    id_dict["z"]=math.floor(((node_id-1)/(g_mesh_data["r"]+1))/g_mesh_data["p"])%(g_mesh_data["z"]+1)+1
    return id_dict

def deduct_iter_phi_to_eval(angle_of_qs):
    #angle_of_qs=angle in radians
    #angle=start+dp_in*iter/np_in
    #->iter=(angle-start)*np_in/dp_in
    return int((angle_of_qs-g_mesh_data["start"])*g_mesh_data["np_in"]/g_mesh_data["dp_in"])

if __name__=="__main__":
    
    read_mesh_data()
    print(g_mesh_data)
    ele_id=get_ele_id({"r":2,"p":16,"z":26})
    new_id_dict=get_ele_iter(ele_id)
    print("new_id_dict="+str(new_id_dict))

