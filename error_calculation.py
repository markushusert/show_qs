import sys
import os
import math


g_script_dir = os.path.dirname(os.path.realpath(__file__))
expected_result_file=os.path.join(g_script_dir,"expected_results.txt")

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
        elif line.startswith("phiqs:"):
            valuestring=line.split(":",1)[1]
            g_phiqs=float(eval(valuestring))*math.pi
            
g_wez=[value*g_wez_fac for value in g_wez]
print("g_delr="+str(g_delr))
print("g_wez="+str(g_wez))
    
