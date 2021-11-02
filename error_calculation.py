import sys
import os
import math


g_script_dir = os.path.dirname(os.path.realpath(__file__))
g_expected_result_file=os.path.join(g_script_dir,"expected_results.txt")
g_error_file_name="errors.txt"
g_signed_error_file_name="signed_errors.txt"

#in the same dir as the post-scripts is supposed to lie a file indicating the expected results of wez and cut
with open(g_expected_result_file,"r") as fil:
    lines=fil.readlines()
    for line in lines:
        if line.startswith("wez:"):
            valuestring=line.split(":",1)[1]
            try:
                g_wez_correct=[float(valuestring.split(",")[i]) for i in range(12)]
            except IndexError:
                print("provide 12 values for the wez, from bottom to top")
                raise Exception
        elif line.startswith("wez_fac:"):
            valuestring=line.split(":",1)[1]
            g_wez_fac=float(eval(valuestring))
        elif line.startswith("delr:"):
            valuestring=line.split(":",1)[1]
            g_delr=float(eval(valuestring))
        elif line.startswith("phiqs:"):
            valuestring=line.split(":",1)[1]
            g_phiqs=float(eval(valuestring))*math.pi
            
g_wez_correct=[value*g_wez_fac for value in g_wez_correct]
#print("g_delr="+str(g_delr))
#print("g_wez_correct="+str(g_wez_correct))

def rel_deviation(a,b):
    if(a>b):
        return (a-b)/a
    else:
        return (a-b)/b

def avg(list):
    return sum(list)/len(list)

def write_error_file(post_dir):
    #writes the calculated errors to a file in post_dir
    error_file=os.path.join(post_dir,g_error_file_name)
    with open(error_file,"w") as fil:
        fil.write("error_wez="+str(g_error_wez)+"\n")
        fil.write("error_delr="+str(g_error_delr)+"\n")
        fil.write("error_schicht="+str(g_error_schicht)+"\n")
        fil.write("error_ges="+str(g_error_ges)+"\n")
def write_signed_errors(error_laengs,error_quer,post_dir):
    error_file=os.path.join(post_dir,g_signed_error_file_name)
    with open(error_file,"w") as fil:
        fil.write("error_laengs="+str(error_laengs)+"\n")
        fil.write("error_quer="+str(error_quer)+"\n")
        fil.write("error_delr_signed="+str(g_error_delr_signed)+"\n")

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
    global g_wez_correct

    if layer_indices is None:
        layer_indices=[i for i in range(len(layer_values))]

    wez_expected=[g_wez_correct[i] for i in layer_indices]
    if signed:
        return avg([rel_deviation(wez,wez_correct)*abs(rel_deviation(wez,wez_correct)) for wez,wez_correct in zip(layer_values,wez_expected)])
    else:
        return avg([rel_deviation(wez,wez_correct)**2 for wez,wez_correct in zip(layer_values,wez_expected)])

def calulate_res_error(wez_ges,delr,ratio_uncut):
    #calculate resulting error by comparing given wez_ges,delr and ratio of uncut layers
    #with the expected results
    global g_error_wez,g_error_delr,g_error_schicht,g_error_ges,g_wez_correct,g_error_delr_signed

    g_error_wez=error_of_given_layers(wez_ges)
    g_error_delr=rel_deviation(delr,g_delr)**2
    g_error_delr_signed=rel_deviation(delr,g_delr)*rel_deviation(delr,g_delr)
    g_error_schicht=ratio_uncut*10#10 is chosen arbitrary
    g_error_ges=math.sqrt(g_error_delr**2+g_error_wez**2)+g_error_schicht
    print(f"error={g_error_ges}")
    return g_error_wez,g_error_delr,g_error_schicht,g_error_ges
