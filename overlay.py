#!/usr/bin/python3
import output,error_calculation
import numpy as np
import os
g_pics_dir="Pics"
def main():
    yoffset=800
    
    for qs in error_calculation.g_qs_to_eval:
        if qs==90:
            xoffset=4300
        else:
            xoffset=4375
        #values_outside=np.genfromtxt(f"wez-values-outside{qs}.txt")
        #values_inside=np.genfromtxt(f"wez-values-inside{qs}.txt")
        overlay_file=os.path.join(g_pics_dir,output.g_overlay_file.format(qs_to_eval=qs))
        for orient in ["laengs","quer"]:
            res_file=os.path.join(g_pics_dir,f"comparison{qs}_{orient}.jpg")
            experimental_pic=output.g_experimental_qs_images.format(qs_to_eval=qs,orientation=orient)
            if os.path.isfile(experimental_pic):
                output.overlay_image(experimental_pic,overlay_file,res_file,16.9,(-xoffset,-yoffset))

if __name__=="__main__":
    main()