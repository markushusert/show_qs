import sys
import os
import math
import copy
import customstats
g_nr_layers=customstats.g_nr_layers
g_script_dir = os.path.dirname(os.path.realpath(__file__))
g_expected_result_file=os.path.join(g_script_dir,"expected_results.txt")
g_debugflag=False
#in the same dir as the post-scripts is supposed to lie a file indicating the expected results of wez and cut
with open(g_expected_result_file,"r") as fil:
	global g_qs_to_eval,g_expected_values_for_qs
	lines=[line for line in fil.readlines() if not line.strip().startswith("#")]
	qs_to_eval_string=lines[0].split(":")[-1]
	#only whole degrees allowed 
	g_qs_to_eval=[int(string) for string in qs_to_eval_string.split(",")]
	
	g_expected_values_for_qs={}
	arrays_to_give=("wez","cut")
	for qs in g_qs_to_eval:
		g_expected_values_for_qs[qs]={name:None for name in ["wez","delr"]}
		given_fac=False
		for line in lines:
			for name in arrays_to_give:
				if line.startswith(f"{name}{qs}:"):
					valuestring=line.split(":",1)[1]
					tokens=valuestring.split(",")
					try:
						g_expected_values_for_qs[qs][name]=[eval(tokens[i]) for i in range(12)]
					except IndexError:
						print("provide 12 values for the wez, from bottom to top")
						print(tokens)
						print(f"values provided:{[eval(tokens[i]) for i in range(12)]}")
						raise Exception
			if line.startswith(f"fac{qs}:"):
				valuestring=line.split(":",1)[1]
				fac=float(eval(valuestring))
				given_fac=True
			elif line.startswith(f"delr{qs}:"):
				valuestring=line.split(":",1)[1]
				delr=float(eval(valuestring))
				g_expected_values_for_qs[qs]["delr"]=delr
		if given_fac:
			for name in arrays_to_give:
				g_expected_values_for_qs[qs][name]=[value*fac if value else None for value in g_expected_values_for_qs[qs][name]]
			





laengs_quer_idx_dict={0:{"laengs":[0,2,4,7,9,11],"quer":[1,3,5,6,8,10]}}
laengs_quer_idx_dict[90]={}
laengs_quer_idx_dict[90]["laengs"]=laengs_quer_idx_dict[0]["quer"]
laengs_quer_idx_dict[90]["quer"]=laengs_quer_idx_dict[0]["laengs"]

def check_layer_list(layer_list):
	if len(layer_list)!=g_nr_layers:
		raise ValueError(f"lenght of layer_list must be {g_nr_layers}, recieved list: {layer_list}")

def calculate_laengs_quer_error(wez_layer,qs_to_eval):
	check_layer_list(wez_layer)
	
	#python list index starting at 0 at the bottom of the z-coord
	laengs_idx=laengs_quer_idx_dict[qs_to_eval]["laengs"]
	quer_idx=laengs_quer_idx_dict[qs_to_eval]["quer"]

	laengs_wez=[wez if i in laengs_idx else None for i,wez in enumerate(wez_layer)]
	quer_wez=[wez if i in quer_idx else None for i,wez in enumerate(wez_layer)]

	deviations_laengs=get_deviation_of_layers(laengs_wez,qs_to_eval,"wez")
	error_laengs=customstats.avg(deviations_laengs)
	if g_debugflag:
		print(f"error_of_layers:{laengs_wez} is {error_laengs}")
	
	deviations_quer=get_deviation_of_layers(quer_wez,qs_to_eval,"wez")
	error_quer=customstats.avg(deviations_quer)
	if g_debugflag:
		print(f"error_of_layers:{quer_wez} is {error_quer}")
	return error_laengs,error_quer


def error_of_given_layers(layer_values,qs_to_eval=0,signed=False,name="wez"):
	#give error of a given list of layer_values
	#layer_values
	#by comparing with expected results in g_wez_correct
	#if signed option is given the signed error of each layer is averaged
	global g_expected_values_for_qs
	deviation_of_layers=get_deviation_of_layers(layer_values,qs_to_eval,name)
	res=customstats.sqrt_MSE(deviation_of_layers)
	if g_debugflag:
		print(f"{name}-error of layers:{layer_values} is {res}")
	return res
def get_deviation_of_layers(layer_values,qs_to_eval,name_to_eval):
	wez_expected=[g_expected_values_for_qs[qs_to_eval][name_to_eval][i] for i in range(len(layer_values))]
	deviation=[customstats.rel_deviation(wez,wez_correct) for wez,wez_correct in zip(layer_values,wez_expected)]
	if g_debugflag:
		print(f"layers_simulated:{layer_values},layers_experimental:{wez_expected},deviation:{deviation}")
	return deviation
def calc_error_schicht(ratio_uncut):
	error_schicht=ratio_uncut*10#10 is chosen arbitrary
	return error_schicht

def combine_errors(error_wez,error_delr,error_schicht):
	return math.sqrt(error_delr**2+error_wez**2)+error_schicht


def calculate_res_error(wez_layer,cut_layer,qs_to_eval,error_schicht):
	#calculate resulting error by comparing given wez_layer,delr and ratio of uncut layers
	#with the expected results
	global g_expected_values_for_qs
	#
	error_wez=error_of_given_layers(wez_layer,qs_to_eval=qs_to_eval)
	error_delr=error_of_given_layers(cut_layer,qs_to_eval=qs_to_eval,name="cut")
	  
	error_ges=combine_errors(error_wez,error_delr,error_schicht)
	print(f"error{qs_to_eval}={error_ges}")
	return error_wez,error_delr,error_schicht,error_ges
