import os
import numpy as np
import matplotlib.pyplot as plt
import mesh_data

g_error_file_name="errors{qs_to_eval}.txt"
g_signed_error_file_name="signed_errors{qs_to_eval}.txt"
g_global_stats_file="global_stats.txt"
g_written_output_files=[]
combined_output_file="all_outputs.txt"
g_specimen_thickness=1.8*10**(-3)
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
    stats={f"error_wez{qs_to_eval}":error_wez,f"error_delr{qs_to_eval}":error_delr,"error_schicht":error_schicht,f"error_ges{qs_to_eval}":error_ges}
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

def plot_results(post_dir,qs_to_eval,cut_iter_values,wez_iter_values):
	#plots the functions cut(z) and wez(z)
	#once with auto scaling and once with 1:1 aspect ratio
	#post_dir=directory to place plots as png
	#cut_iter_values=iterable(here np.array) of cut-widths of all iter_z-values
	#wez_iter_values=iterable(here np.array) of wez-widths of all iter_z-values
	plot_file=os.path.join(post_dir,f"kerf_and_haz{qs_to_eval}.png")
	equal_ratio_file=os.path.join(post_dir,f"kerf_and_haz_equal{qs_to_eval}.png")

	y_values=np.linspace(0,g_specimen_thickness,mesh_data.g_mesh_data["z"]+1)
	fig, ax = plt.subplots()
	linewidth=0.5
	handle_cut,=ax.plot(cut_iter_values,y_values,color="red",label="kerf",linewidth=linewidth)
	handle_wez,=ax.plot(wez_iter_values,y_values,color="blue",label="HAZ",linewidth=linewidth)
	plt.legend(handles=[handle_cut,handle_wez])

	ax.set_aspect('auto')
	fig.savefig(plot_file)

	ax.set_aspect('equal')
	fig.savefig(equal_ratio_file)


def write_results(filename,cut_iter_values,wez_iter_values):
	#writes calculated widths of cut and wez to given file
	#filename=filename to write to
	#cut_iter_values=iterable(here np.array) of cut-widths of all iter_z-values
	#wez_iter_values=iterable(here np.array) of wez-widths of all iter_z-values
	with open(filename,"w") as fil:
		cut_2d=np.reshape(cut_iter_values, (-1, 1))
		wez_2d=np.reshape(wez_iter_values, (-1, 1))
		data=np.concatenate((cut_2d,wez_2d),axis=1)
		np.savetxt(fil,data,header="cut; wez")