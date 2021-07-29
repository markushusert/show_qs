import sys
import os
import math

expected_result_file="expected_results.txt"
g_Post_dir="Post"

if not(os.path.isdir(g_Post_dir)):
    os.makedirs(g_Post_dir)

with open(expected_result_file,"r") as fil:
    lines=fil.readlines()
    for line in lines:
        if line.startswith("wez:"):
            valuestring=line.split(":",1)[1]
            try:
                g_wez=[float(valuestring.split(",")[i]) for i in range(12)]
            except IndexError:
                print("provide 12 values for the wez, from bottom to top")
                raise Exception
        elif line.startswith("wez_fac:"):
            valuestring=line.split(":",1)[1]
            g_wez_fac=float(eval(valuestring))
        elif line.startswith("delr:"):
            valuestring=line.split(":",1)[1]
            g_delr=float(eval(valuestring))
g_wez=[value*g_wez_fac for value in g_wez]
print("g_delr="+str(g_delr))
print("g_wez="+str(g_wez))
    
