import sys
import os
import math
glob_input__dir=os.getcwd()
glob_mesh_file="MESH_lasrcut"

def read_mesh_data():
    with open(glob_mesh_file,"r") as fil:
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
    id_dict["r"]=(ele_id-1)%glob_mesh_data["r"]+1
    id_dict["p"]=math.floor(((ele_id-1)/glob_mesh_data["r"]))%glob_mesh_data["p"]+1
    id_dict["z"]=math.floor(((ele_id-1)/glob_mesh_data["r"])/glob_mesh_data["p"])%glob_mesh_data["z"]+1
    return id_dict

def get_ele_id(ele_id_dict):
    ele_id=ele_id_dict["r"]+(ele_id_dict["p"]-1)*glob_mesh_data["r"]+(ele_id_dict["z"]-1)*glob_mesh_data["r"]*glob_mesh_data["p"]
    return ele_id

if __name__=="__main__":
    global glob_mesh_data
    glob_mesh_data=read_mesh_data()
    print(glob_mesh_data)
    ele_id=get_ele_id({"r":2,"p":16,"z":26})
    new_id_dict=get_ele_iter(ele_id)
    print("new_id_dict="+str(new_id_dict))

