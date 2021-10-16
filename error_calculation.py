import sys
import os
import math


g_script_dir = os.path.dirname(os.path.realpath(__file__))
g_expected_result_file=os.path.join(g_script_dir,"expected_results.txt")
g_error_file_name="errors.txt"

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

def calulate_res_error(wez_ges,delr,ratio_uncut):
    #calculate resulting error by comparing given wez_ges,delr and ratio of uncut layers
    #with the expected results
    global g_error_wez,g_error_delr,g_error_schicht,g_error_ges,g_wez_correct

    g_error_wez=avg([rel_deviation(wez,wez_correct)**2 for wez,wez_correct in zip(wez_ges,g_wez_correct)])
    g_error_delr=rel_deviation(delr,g_delr)**2
    g_error_schicht=ratio_uncut*10#10 is chosen arbitrary
    g_error_ges=math.sqrt(g_error_delr**2+g_error_wez**2)+g_error_schicht
    print(f"error={g_error_ges}")
    return g_error_wez,g_error_delr,g_error_schicht,g_error_ges
