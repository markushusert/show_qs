import sys
import os
import math
import copy

g_script_dir = os.path.dirname(os.path.realpath(__file__))
g_expected_result_file=os.path.join(g_script_dir,"expected_results.txt")
g_error_file_name="errors.txt"
g_signed_error_file_name="signed_errors.txt"
g_global_stats_file="global_stats.txt"

#in the same dir as the post-scripts is supposed to lie a file indicating the expected results of wez and cut
with open(g_expected_result_file,"r") as fil:
    global g_qs_to_eval,g_expected_values_for_qs
    lines=fil.readlines()
    qs_to_eval_string=lines[0].split(":")[-1]
    #only whole degrees allowed 
    g_qs_to_eval=[int(string) for string in qs_to_eval_string.split(",")]
    
    g_expected_values_for_qs={}
    for qs in g_qs_to_eval:
        g_expected_values_for_qs[qs]={name:None for name in ["wez","delr"]}
        given_results=False
        for line in lines:
            if line.startswith(f"wez{qs}:"):
                valuestring=line.split(":",1)[1]
                given_results=True
                try:
                    wez_correct=[float(valuestring.split(",")[i]) for i in range(12)]
                except IndexError:
                    print("provide 12 values for the wez, from bottom to top")
                    raise Exception
            elif line.startswith(f"wez_fac{qs}:"):
                valuestring=line.split(":",1)[1]
                wez_fac=float(eval(valuestring))
            elif line.startswith(f"delr{qs}:"):
                valuestring=line.split(":",1)[1]
                delr=float(eval(valuestring))
        if given_results:
            wez_correct=[value*wez_fac for value in wez_correct]
            g_expected_values_for_qs[qs]["wez"]=copy.copy(wez_correct)
            g_expected_values_for_qs[qs]["delr"]=delr

def rel_deviation(a,b):
    if(a>b):
        return (a-b)/a
    else:
        return (a-b)/b

def avg(list):
    return sum(list)/len(list)
def write_global_stats(post_dir,energy_per_mat,volume_per_mat,energy_per_phase,volume_per_phase):
    error_file=os.path.join(post_dir,g_global_stats_file)
    list_of_result_lists=[energy_per_mat,volume_per_mat,energy_per_phase,volume_per_phase]
    list_of_result_names=["energ_mat","vol_mat","energ_phase","vol_phase"]
    with open(error_file,"w") as fil:
        for list,name in zip(list_of_result_lists,list_of_result_names):
            for iter,val in enumerate(list):
                fil.write(f"{name}{iter+1}={val}"+"\n")
def write_error_file(post_dir,error_wez,error_delr,error_schicht,error_ges):
    #writes the calculated errors to a file in post_dir
    error_file=os.path.join(post_dir,g_error_file_name)
    with open(error_file,"w") as fil:
        fil.write("error_wez="+str(error_wez)+"\n")
        fil.write("error_delr="+str(error_delr)+"\n")
        fil.write("error_schicht="+str(error_schicht)+"\n")
        fil.write("error_ges="+str(error_ges)+"\n")
        
def write_signed_errors(error_laengs,error_quer,post_dir):
    error_file=os.path.join(post_dir,g_signed_error_file_name)
    with open(error_file,"w") as fil:
        fil.write("error_laengs="+str(error_laengs)+"\n")
        fil.write("error_quer="+str(error_quer)+"\n")

def calculate_laengs_quer_error(wez_ges):
    #python list index starting at 0 at the bottom of the z-coord
    laengs_schichten=[0,2,4,7,9,11]
    quer_schichten=[1,3,5,6,8,10]

    laengs_wez=[wez_ges[i] for i in laengs_schichten]
    quer_wez=[wez_ges[i] for i in quer_schichten]

    error_laengs=error_of_given_layers(laengs_wez,laengs_schichten,True)
    error_quer=error_of_given_layers(quer_wez,laengs_schichten,True)
    return error_laengs,error_quer

def error_of_given_layers(layer_values,layer_indices=None,signed=False):
    #give error of a given list of layer_values and their corresponding layer_indices
    #by comparing with expected results in g_wez_correct
    #if signed option is given the signed error of each layer is averaged
    global g_expected_values_for_qs

    if layer_indices is None:
        layer_indices=[i for i in range(len(layer_values))]

    wez_expected=[g_expected_values_for_qs[0]["wez"][i] for i in layer_indices]
    if signed:
        return avg([rel_deviation(wez,wez_correct)*abs(rel_deviation(wez,wez_correct)) for wez,wez_correct in zip(layer_values,wez_expected)])
    else:
        return avg([rel_deviation(wez,wez_correct)**2 for wez,wez_correct in zip(layer_values,wez_expected)])


def calulate_res_error(wez_ges,delr,ratio_uncut):
    #calculate resulting error by comparing given wez_ges,delr and ratio of uncut layers
    #with the expected results
    global g_expected_values_for_qs
    #
    error_wez=error_of_given_layers(wez_ges)
    error_delr=rel_deviation(delr,g_expected_values_for_qs[0]["delr"])*abs(rel_deviation(delr,g_expected_values_for_qs[0]["delr"]))
    error_schicht=ratio_uncut*100#100 is chosen arbitrary
    error_ges=math.sqrt(error_delr**2+error_wez**2)+error_schicht
    print(f"error={error_ges}")
    return error_wez,error_delr,error_schicht,error_ges
