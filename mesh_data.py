import sys
import os
import math
g_input_dir=os.getcwd()
g_mesh_file="MESH_lasrcut"

def read_mesh_data():
    with open(g_mesh_file,"r") as fil:
        lines=fil.readlines()
    result_dict={key:None for key in ["r","p","z"]}
    for line in lines:
        if line.lstrip().startswith("cmes"):
            for key in result_dict.keys():
                arguments=line.split(",")
                if arguments[1]==key:
                    result_dict[key]=int(arguments[2])
    return result_dict
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



if __name__=="__main__":
    global g_mesh_data
    g_mesh_data=read_mesh_data()
    print(g_mesh_data)
    ele_id=get_ele_id({"r":2,"p":16,"z":26})
    new_id_dict=get_ele_iter(ele_id)
    print("new_id_dict="+str(new_id_dict))

