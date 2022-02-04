from os import error
import mesh_data
import math
import numpy as np
import partitions
import error_calculation
import output
import scipy
import customstats
from scipy import stats

g_debugflag=False
g_main_file="Ilasrcut"
g_nr_layers=12
def get_wez_of_all_iters(iter_phi_qs,partition_node_dict,partition_vtk_data_dict,direction=1):
	#iter_phi_qs=integer indicating which cross-section shall be evaluated
	#partition_node_dict, see read_partitions
	#partition_vtk_data_dict, see split_vtkdata
	#direction can be 1 for going outward from the center, or -1 for goinig inward
	number_eles=round(mesh_data.g_mesh_data["z"])
	cut_values=list()
	wez_values=list()
	for iter_z in range(1,number_eles+1+1):#example: 36 elements->37 nodes->iter_z goes from 1 to 37
		wez,cut=get_wez_of_iter_z(iter_z,iter_phi_qs,partition_node_dict,partition_vtk_data_dict,direction)
		cut_values.append(cut)
		wez_values.append(wez)
	return np.array(cut_values),np.array(wez_values)

def get_wez(cut_iter_values,wez_iter_values):
	#calculates wez and cut widths for each of the g_nr_layers layers
	#cut_iter_values=iterable(here np.array) of cut-widths of all iter_z-values
	#wez_iter_values=iterable(here np.array) of wez-widths of all iter_z-values
	global g_nr_layers
	nr_ele_per_layer=mesh_data.g_mesh_data["z"]/g_nr_layers
	nr_uncut_iter_z=0
	min_schnitt=math.inf
	max_schnitt=-math.inf
	wez_layer=[None for i in range(g_nr_layers)]
	schnitt_layer=[None for i in range(g_nr_layers)]

	for iter_layer in range(g_nr_layers):
		#eval layer
		schnittmean,wezmean,min_schnitt_r,max_schnitt_r,first_uncut=get_wez_of_layer(iter_layer,cut_iter_values,wez_iter_values)
		
		#reduce evaluations
		min_schnitt=min([min_schnitt,min_schnitt_r])
		max_schnitt=max([max_schnitt,max_schnitt_r])
		wez_layer[iter_layer]=wezmean
		schnitt_layer[iter_layer]=schnittmean
		if first_uncut:
			nr_uncut_iter_z=first_uncut

		continue
		nr_ele_per_layer=mesh_data.g_mesh_data["z"]/g_nr_layers
		iter_z_start=1+(iter_layer)*nr_ele_per_layer
		iter_z_end=1+(iter_layer-1)*nr_ele_per_layer
		for iter_z in range(iter_z_start,iter_z_end-1,-1):
			
			schnitt,wez=get_wez_of_iter_z(iter_z,iter_phi_qs,partition_node_dict,pview_out_allpvd)
			#current z-line has not been cut, and its the first case
			if schnitt==0.0 and nr_uncut_iter_z!=0:
				nr_uncut_iter_z=iter_z
			
	return schnitt_layer,wez_layer,max_schnitt-min_schnitt,nr_uncut_iter_z

def get_iter_lims_of_layer(layer_number):
	nr_ele_per_layer=round(mesh_data.g_mesh_data["z"]/g_nr_layers)
	iter_z_high=(layer_number+1)*nr_ele_per_layer
	iter_z_low=(layer_number)*nr_ele_per_layer
	return iter_z_low,iter_z_high+1

def get_wez_of_layer(layer_number,cut_iter_values,wez_iter_values):
	#calculate wez and cut width of a given layer
	#layer_numer=number from 0 to 11 indicating layer to be evald
	#cut_iter_values=iterable(here np.array) of cut-widths of all iter_z-values
	#wez_iter_values=iterable(here np.array) of wez-widths of all iter_z-values
	iter_z_low,iter_z_high=get_iter_lims_of_layer(layer_number)

	first_wez_uncut=None
	weight_acc=0.0
	schnitt_acc=0.0
	wez_acc=0.0
	min_schnitt=math.inf
	max_schnitt=-math.inf
	for iter_z in range(iter_z_low,iter_z_high):
		if iter_z in [iter_z_high,iter_z_low]:
			weight=0.5
		else:
			weight=1.0
		delr_schnitt=cut_iter_values[iter_z]
		delr_wez=wez_iter_values[iter_z]

		if delr_schnitt==0.0:
			first_wez_uncut=iter_z+1#+1 because iter_z starts at 0, but highest uncut should start at 1

		weight_acc+=weight
		schnitt_acc+=delr_schnitt*weight
		wez_acc+=delr_wez*weight
		min_schnitt=min([delr_schnitt,min_schnitt])
		max_schnitt=max([delr_schnitt,max_schnitt])
		if g_debugflag:
			print("iter_z: "+str(iter_z)+", in layer: "+str(layer_number)+" has wez: "+str(delr_wez)+" and cut: "+str(delr_schnitt))
	return schnitt_acc/weight_acc, wez_acc/weight_acc,min_schnitt,max_schnitt,first_wez_uncut

def get_wez_of_iter_z(iter_z,iter_phi_qs,partition_node_dict,partition_vtk_data_dict,direction):
	#get wez and cut-width of a given cross_section(integer iter_phi_qs) and a given height(integer iter_z)
	#partition_node_dict, dict as returned by partitions.read_partitions
	#partition_vtk_data_dict, dict as returned by partitions.split_vtkdata
	#direction on of -1,or 1 to go either inwards or outwards
	if direction not in [1,-1]:
		raise Exception(f"direction was {direction}, must be one of {[1,-1]}")
	iter_r_half=int(1+mesh_data.g_mesh_data["r"]/2)
	iter_r_end=1+mesh_data.g_mesh_data["r"]#plus 1 because one more node than elements

	if direction==1:
		limr=iter_r_end+1
	else:
		limr=0
	list_of_values=[0.0,0.0]
	
	for iter_r in range(iter_r_half,limr,direction):
		iter_dict={"r":iter_r,"p":iter_phi_qs,"z":iter_z}
		nodeid=mesh_data.get_node_id(iter_dict)		
		phase_of_node=partitions.get_array_value_of_global_id(partition_node_dict,partition_vtk_data_dict,nodeid,'phase')
		
		if iter_r != 1:
			delr_preceeding=mesh_data.g_delr_array[iter_r-2]
		else:
			delr_preceeding=0.0
		if iter_r !=iter_r_end:
			delr_following=mesh_data.g_delr_array[iter_r-1]
		else:
			delr_following=0.0
		delr_node=(delr_following+delr_preceeding)/2
		if iter_r ==iter_r_half:
			delr_node=delr_node/2
		if False:
			print(f"iter_z:{iter_z},iter_r: "+str(iter_r)+"phase: "+str(phase_of_node)+" delr_node: "+str(delr_node))
		already_considered_vol_ratio=0.0
		for current_phase in range(1,-1,-1):
			list_of_values[current_phase]+=delr_node*(1-already_considered_vol_ratio)*phase_of_node[current_phase]
			already_considered_vol_ratio+=phase_of_node[current_phase]
	return tuple(list_of_values)
	

def get_totally_cut_layers(spaltbreite):
	return [i for i in range(g_nr_layers) if all(spaltbreite[j] for j in range(*get_iter_lims_of_layer(i)))]

def qs_statistics(qs,spalt_breite,schnitt_mean,wez_layer_outside,wez_layer_inside,cut_iter_outside,cut_iter_inside):
	#qs=integer of qs to eval
	#wez_mean=average of outside and inside wez per layer
	#spalt_breite=sum of outside and inside cut per layer
	#wez_layer_outside=list of g_nr_layers wez-values from bottom to top
	#wez_layer_inside= list of g_nr_layers wez-values on the inside
	#cut_iter_values=np.array of cut-values for each iter-z on the outside
	#cut_iter_inside=np.array of cut-values for each iter-z on the outside
	#delr difference in cut-width upside vs downside on the outside
	#delr_inside same but on the inside

	stats={}
	stats["spaltbreite_oben"]=cut_iter_outside[-1]+cut_iter_inside[-1]
	stats["spaltbreite_unten"]=cut_iter_outside[0]+cut_iter_inside[0]
	stats["mean_wez"]=customstats.avg(spalt_breite)
	stats["cut_mean"]=customstats.avg(schnitt_mean)
	mean_wez_outside=customstats.avg(wez_layer_outside)
	mean_wez_inside=customstats.avg(wez_layer_inside)
	stats["wez_ratio_out_in"]=mean_wez_outside/mean_wez_inside
	
	#wez_of_totally_cut_layers=[wez_mean[i] for i in layers_wich_are_totally_cut]
	stats["slope_wez"]=customstats.calc_slope(spalt_breite)
	stats["slope_cut"]=customstats.calc_slope(schnitt_mean)
	
	laengs_quer_idx_of_qs=error_calculation.laengs_quer_idx_dict.get(qs)
	if laengs_quer_idx_of_qs:
		laengs_idx=laengs_quer_idx_of_qs["laengs"]
		quer_idx=laengs_quer_idx_of_qs["quer"]
		laengs_wez=[wez if i in laengs_idx else None for i,wez in enumerate(spalt_breite)]
		quer_wez=[wez if i in quer_idx else None for i,wez in enumerate(spalt_breite)]

		stats["mean_laengs"]=customstats.avg(laengs_wez)
		stats["mean_quer"]=customstats.avg(quer_wez)
		stats["max_laengs_min_quer"]=customstats.emax(laengs_wez)/customstats.emin(quer_wez)
		stats["max_quer_min_laengs"]=customstats.emax(quer_wez)/customstats.emin(laengs_wez)
		stats["slope_laengs"]=customstats.calc_slope(laengs_wez)
		stats["slope_quer"]=customstats.calc_slope(quer_wez)
	
	stats={key+str(qs):val for key,val in stats.items()}
	return stats
def get_used_material_file(): 
	with open(g_main_file,"r") as fil:
		lines=fil.readlines()
	for line in lines:
		if line.lower().startswith("include,"):
			included_file=line.split(",")[-1].strip()
			if included_file.lower().startswith("mat"):
				return included_file

def get_material_data(params):
	used_material_file=get_used_material_file()
	with open(used_material_file,"r") as fil:
		lines=fil.readlines()
	return_dict={param:None for param in params}
	for line in lines:
		for param in params:
			if param in line:
				value=float(line.split(" ")[-1].strip())
				return_dict[param]=value
				break
	return return_dict
def get_nr_uncut_iter_z(partition_vtk_data_dict,partition_node_dict):
	iter_r=int(mesh_data.g_mesh_data["r"]/2)#nodes in the middle
	iter_phi_0_deg=mesh_data.deduct_iter_phi_to_eval(0.0)
	iter_phi_90_deg=mesh_data.deduct_iter_phi_to_eval(1/2.0)
	
	for iter_z in range(mesh_data.g_mesh_data["z"],0,-1):#loop from top to bottom
		iter_z_is_cut=True
		for iter_phi in range(iter_phi_0_deg,iter_phi_90_deg+1):#only loop over inner phis
			nodeid=mesh_data.get_node_id({"r":iter_r+1,"z":iter_z+1,"p":iter_phi+1})
			phase_of_node=partitions.get_array_value_of_global_id(partition_node_dict,partition_vtk_data_dict,nodeid,'phase')
			if any(phase!=1.0 for phase in phase_of_node):
				iter_z_is_cut=False
				break
		if not iter_z_is_cut:
			return iter_z
	#no uncut iter_z was found
	return 0

def dummy():
	return float("0.1")
def global_evaluation(partition_vtk_data_dict,partition_node_dict):

	delr_array=mesh_data.g_delr_array
	r_array=mesh_data.g_r_array
	delphi_array=mesh_data.g_delphi_array
	delz_array=mesh_data.g_delz_array

	
	energy_per_phase=[0.0 for i in range(3)]
	volume_per_phase=[0.0 for i in range(3)]
	
	#0-> energy adsorbed by matrix, 1-> energy adsorbed by faser,sum of energy adsorbed
	energy_per_mat=[0.0 for i in range(3)]
	#0->evaporated matrix vol, 1-> evaporated faser vol, 2-> total evaporated vol
	evaporated_volume=[0.0 for i in range(3)]

	mat_data=get_material_data(["VF","cm","cf","cco2","rco2","rm","rf","T1","T2","E1","E2"])
	VF=mat_data["VF"]
	volume_ratios=[1-VF,VF]
	capacities=[mat_data["cm"]*mat_data["rm"],mat_data["cf"]*mat_data["rf"]]
	temps_dampf=[mat_data["T1"],mat_data["T2"]]
	enths_dampf=[mat_data["E1"],mat_data["E2"]]

	for iter_r in range(mesh_data.g_mesh_data["r"]+1):#+1 because loop over nodes not elements
		if iter_r == 0:
			delr=delr_array[iter_r]/2
			radius=r_array[iter_r]+delr/2
		elif iter_r == mesh_data.g_mesh_data["r"]:
			delr=delr_array[iter_r-1]/2
			radius=r_array[iter_r]-delr/2
		else:
			delr=(delr_array[iter_r-1]+delr_array[iter_r])/2
			radius=r_array[iter_r]
		for iter_z in range(mesh_data.g_mesh_data["z"]+1):
			if iter_z == 0:
				delz=delz_array[iter_z]/2	
			elif iter_z == mesh_data.g_mesh_data["z"]:
				delz=delz_array[iter_z-1]/2
			else:
				delz=(delz_array[iter_z-1]+delz_array[iter_z])/2
			for iter_phi in range(mesh_data.g_mesh_data["p"]):
				if iter_phi in [0,mesh_data.g_mesh_data["p"]]:
					delphi=(delphi_array[0]+delphi_array[mesh_data.g_mesh_data["p"]-1])/2
				else:
					delphi=(delphi_array[iter_phi]+delphi_array[iter_phi-1])/2
				
				volume_of_node=radius*delr*delz*delphi
				nodeid=mesh_data.get_node_id({"r":iter_r+1,"p":iter_phi+1,"z":iter_z+1})
				phase_of_node=partitions.get_array_value_of_global_id(partition_node_dict,partition_vtk_data_dict,nodeid,'phase')
				energy_of_node=volume_of_node*partitions.get_array_value_of_global_id(partition_node_dict,partition_vtk_data_dict,nodeid,'energie')[0]
				temp_of_node=partitions.get_array_value_of_global_id(partition_node_dict,partition_vtk_data_dict,nodeid,'temperatur')[0]
				#ratio for each phase [0=undamaged, 1=matrix gone, 2=faser gone]
				ratio_phase=[1.0-phase_of_node[0],phase_of_node[0]*(1.0-phase_of_node[1]),phase_of_node[0]*phase_of_node[1]]
				#ratio for how much
				ratio_mat=[(1-VF)*(1.0-phase_of_node[0]),VF*(1.0-phase_of_node[1]),(1-VF)*(phase_of_node[0])+VF*(phase_of_node[1])]
				# ratio for how much volume of the node is evaporated
				# 0=matrix-volume, 1=faser-volume, 2=both
				ratio_evap=[(1-VF)*(phase_of_node[0]),VF*(phase_of_node[1])]
				
				for i in range(2):
					evaporated_volume[i]+=volume_of_node*ratio_evap[i]
					energy_per_mat[i]+=volume_of_node*volume_ratios[i]*(
						capacities[i]*temps_dampf[i]
						+enths_dampf[i]*phase_of_node[i]
						+capacities[i]*(temp_of_node-temps_dampf[i])*(1-phase_of_node[i])
						)
				energy_per_mat[2]+=energy_of_node
				
				for i in range(3):
					volume_per_phase[i]+=volume_of_node*ratio_phase[i]
					energy_per_phase[i]+=energy_of_node*ratio_phase[i]
					
	evaporated_volume[2]=evaporated_volume[0]+evaporated_volume[1]
	glob_stats={}
	glob_stats.update({"vol_phase"+str(i):val for i,val in enumerate(volume_per_phase)})
	glob_stats.update({"energ_phase"+str(i):val for i,val in enumerate(energy_per_phase)})
	glob_stats.update({"energ_mat"+str(i):val for i,val in enumerate(energy_per_mat[:2])})
	glob_stats.update({"energ_ges":energy_per_mat[2]})
	glob_stats.update({"evap_vol_mat"+str(i):val for i,val in enumerate(evaporated_volume[:2])})
	glob_stats.update({"evap_vol_ges":evaporated_volume[2]})

	return glob_stats
def get_uncut_ratio(nr_uncut_iter_z):
	if nr_uncut_iter_z==0:
		to_ret= 0.0
	elif nr_uncut_iter_z==mesh_data.g_mesh_data["z"]:
		to_ret=1.0
	else:
		eles_not_cut=(nr_uncut_iter_z-1)+0.5
		to_ret= eles_not_cut/(mesh_data.g_mesh_data["z"])
	return to_ret