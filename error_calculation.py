import sys
import os
import math
import copy

g_script_dir = os.path.dirname(os.path.realpath(__file__))
g_expected_result_file=os.path.join(g_script_dir,"expected_results.txt")


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


laengs_quer_idx_dict={0:{"laengs":[0,2,4,7,9,11],"quer":[1,3,5,6,8,10]}}
laengs_quer_idx_dict[90]={}
laengs_quer_idx_dict[90]["laengs"]=laengs_quer_idx_dict[0]["quer"]
laengs_quer_idx_dict[90]["quer"]=laengs_quer_idx_dict[0]["laengs"]
def calculate_laengs_quer_error(wez_layer,qs_to_eval):
    #python list index starting at 0 at the bottom of the z-coord
    laengs_schichten=laengs_quer_idx_dict[qs_to_eval]["laengs"]
    quer_schichten=laengs_quer_idx_dict[qs_to_eval]["quer"]

    laengs_wez=[wez_layer[i] for i in laengs_schichten]
    quer_wez=[wez_layer[i] for i in quer_schichten]

    error_laengs=error_of_given_layers(laengs_wez,laengs_schichten,qs_to_eval,True)
    error_quer=error_of_given_layers(quer_wez,laengs_schichten,qs_to_eval,True)
    return error_laengs,error_quer

def error_of_given_layers(layer_values,layer_indices=None,qs_to_eval=0,signed=False):
    #give error of a given list of layer_values and their corresponding layer_indices
    #by comparing with expected results in g_wez_correct
    #if signed option is given the signed error of each layer is averaged
    global g_expected_values_for_qs

    if layer_indices is None:
        layer_indices=[i for i in range(len(layer_values))]

    wez_expected=[g_expected_values_for_qs[qs_to_eval]["wez"][i] for i in layer_indices]
    if signed:
        return avg([rel_deviation(wez,wez_correct)*abs(rel_deviation(wez,wez_correct)) for wez,wez_correct in zip(layer_values,wez_expected)])
    else:
        return avg([rel_deviation(wez,wez_correct)**2 for wez,wez_correct in zip(layer_values,wez_expected)])

def calc_error_schicht(ratio_uncut):
    error_schicht=ratio_uncut*100#100 is chosen arbitrary
    return error_schicht

def combine_errors(error_wez,error_delr,error_schicht):
    return math.sqrt(error_delr**2+error_wez**2)+error_schicht


def calculate_res_error(wez_layer,delr,qs_to_eval,error_schicht):
    #calculate resulting error by comparing given wez_layer,delr and ratio of uncut layers
    #with the expected results
    global g_expected_values_for_qs
    #
    error_wez=error_of_given_layers(wez_layer,qs_to_eval=qs_to_eval)
    error_delr=rel_deviation(delr,g_expected_values_for_qs[qs_to_eval]["delr"])*abs(rel_deviation(delr,g_expected_values_for_qs[0]["delr"]))
    
    error_ges=combine_errors(error_wez,error_delr,error_schicht)
    print(f"error{qs_to_eval}={error_ges}")
    return error_wez,error_delr,error_schicht,error_ges
