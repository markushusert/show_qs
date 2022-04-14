import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
#ImageFile.LOAD_TRUNCATED_IMAGES = True #against error: OSError: broken data stream when reading image file
try:
	import mesh_data
	mesh_imported=True
except:
	mesh_imported=False #for to make module standalone

g_error_file_name="errors{qs_to_eval}.txt"
g_signed_error_file_name="signed_errors{qs_to_eval}.txt"
g_global_stats_file="global_stats.txt"
g_overlay_file="kerf_and_haz_overlay{qs_to_eval}.png"
g_written_output_files=[]
combined_output_file="all_outputs.txt"
g_specimen_thickness=1.8*10**(-3)
g_experimental_qs_images=os.path.dirname(os.path.abspath(__file__))+"/Pics/{qs_to_eval}_degree_{orientation}.jpg"
def write_keyword_output(output_file,stats):
	with open(output_file,"w") as fil:
		for key,val in stats.items():
			fil.write(f"{key}={val}\n")
	g_written_output_files.append(output_file)

def write_global_stats(post_dir,energy_per_mat,volume_per_mat,energy_per_phase,volume_per_phase,uncut_ratio):
	global g_written_output_files
	error_file=os.path.join(post_dir,g_global_stats_file)
	list_of_result_lists=[energy_per_mat,volume_per_mat,energy_per_phase,volume_per_phase]
	list_of_result_names=["energ_mat","vol_mat","energ_phase","vol_phase"]
	stats={"uncut_ratio":uncut_ratio}
	for list,name in zip(list_of_result_lists,list_of_result_names):
		for iter,val in enumerate(list):
			stats[f"{name}{iter+1}"]=val
	write_keyword_output(error_file,stats)
def write_error_file(post_dir,qs_to_eval,error_wez,error_delr,error_schicht,error_ges):
	
	error_file=os.path.join(post_dir,g_error_file_name.format(qs_to_eval=qs_to_eval))
	stats={f"error_wez{qs_to_eval}":error_wez,f"error_spalt{qs_to_eval}":error_delr,"error_schicht":error_schicht,f"error_ges{qs_to_eval}":error_ges}
	write_keyword_output(error_file,stats)

def write_signed_errors(post_dir,qs_to_eval,error_laengs,error_quer):
	global g_written_output_files
	error_file=os.path.join(post_dir,g_signed_error_file_name.format(qs_to_eval=qs_to_eval))
	stats={f"error_laengs{qs_to_eval}":error_laengs,f"error_quer{qs_to_eval}":error_quer}
	write_keyword_output(error_file,stats)

def combine_output_files(postdir):
	global g_written_output_files,combined_output_file
	#write content of all output-files into a single file to be read for determining cross-correlation
	
	#collect output
	output_lines=[]
	for file in g_written_output_files:
		with open(file,"r") as fil:
			fil_lines=fil.readlines()
		output_lines.extend(fil_lines)
	combined_file_content=os.path.join(postdir,combined_output_file)
	
	#write collected output
	with open(combined_file_content,"w") as fil:
		fil.writelines(output_lines)

def plot_results(post_dir,qs_to_eval,cut_iter_outside,wez_iter_outside,cut_iter_inside,wez_iter_inside):
	#plots the functions cut(z) and wez(z)
	#once with auto scaling and once with 1:1 aspect ratio
	#post_dir=directory to place plots as png
	#cut_iter_values=iterable(here np.array) of cut-widths of all iter_z-values
	#wez_iter_values=iterable(here np.array) of wez-widths of all iter_z-values
	plot_file=os.path.join(post_dir,f"kerf_and_haz{qs_to_eval}.png")
	equal_ratio_file=os.path.join(post_dir,f"kerf_and_haz_equal{qs_to_eval}.png")
	overlay_file=os.path.join(post_dir,g_overlay_file.format(qs_to_eval=qs_to_eval))
	nr_nodes=mesh_data.g_mesh_data["z"]+1 if mesh_imported else 37#for debugging 37 nodes
	y_values=np.linspace(0,g_specimen_thickness,nr_nodes)
	fig, ax = plt.subplots()
	linewidth=2
	handle_cut=plot_boundary(cut_iter_outside,y_values,ax,color="blue",label="kerf",linewidth=linewidth)
	handle_wez=plot_boundary(wez_iter_outside+cut_iter_outside,y_values,ax,color="red",label="HAZ",linewidth=linewidth)
	plot_boundary(-cut_iter_inside,y_values,ax,color="blue",linewidth=linewidth)
	plot_boundary(-wez_iter_inside-cut_iter_inside,y_values,ax,color="red",linewidth=linewidth)
	plt.legend(handles=[handle_cut,handle_wez],loc="upper right")

	ax.set_ylim((-9e-05, 0.00189))
	ax.set_xlim((-0.000255, 0.000255))#same limits so that all plots are equally sized
	ax.set_aspect('auto')
	fig.savefig(plot_file)

	ax.set_aspect('equal')
	fig.savefig(equal_ratio_file)

	ax.axis(False)
	
	ax.get_legend().remove()
	fig.savefig(overlay_file,transparent=True)
	if False:#does not work with pvpython, do overlaying afterwrds with normal python
		for orientation in ["quer","laengs"]:
			experimental_pic=g_experimental_qs_images.format(qs_to_eval=qs_to_eval,orientation=orientation)
			if os.path.isfile(experimental_pic):
				print("overlaying image")
				overlay_image(experimental_pic,overlay_file,f"comparison{qs_to_eval}.jpg",16.9,(-4350,-800))#scale and position of overlay determined manually
			else:
				print(f"could not find background picture:{experimental_pic}")

def plot_boundary(widths,y_values,ax,**kwargs):
	y_values=[y_values[i] for i in range(len(y_values)) if widths[i]]
	widths=[widths[i] for i in range(len(widths)) if widths[i]]
	handle,=ax.plot(widths,y_values,**kwargs)
	return handle
#handle_cut,=ax.plot(cut_iter_outside,y_values,color="blue",label="kerf",linewidth=linewidth)
def overlay_image(image_background,image_res,image_result,ratio,bound):
    #print(f"overlaying images:{image_background},{image_res}")
    background = Image.open(image_background)
    overlay = Image.open(image_res)
    
    width, height = background.size
    width_overlay, height_overlay = overlay.size
    for i in range(1):
        overlay=overlay.resize((round(width_overlay*ratio),round(height_overlay*ratio)))
        #overlay.resize((10000,10000))
        width_overlay, height_overlay = overlay.size
        #print(f"width:{width},height:{height},width_overlay:{width_overlay},height_overlay:{height_overlay}")
    #background = background.convert("RGBA")
    #overlay = overlay.convert("RGBA")

    background.paste(overlay,bound ,overlay)
    background.save(image_result)

def write_results(filename,cut_iter_values,wez_iter_values):
	#writes calculated widths of cut and wez to given file
	#filename=filename to write to
	#cut_iter_values=iterable(here np.array) of cut-widths of all iter_z-values
	#wez_iter_values=iterable(here np.array) of wez-widths of all iter_z-values
	with open(filename,"w") as fil:
		cut_2d=np.reshape(cut_iter_values, (-1, 1))
		wez_2d=np.reshape(wez_iter_values, (-1, 1))
		data=np.concatenate((cut_2d,wez_2d),axis=1)
		np.savetxt(fil,data,header="cut; wez (from bottom to top)")
