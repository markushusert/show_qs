import math
import scipy

g_nr_layers=12
g_debug=False
#statistical operators, must support None as iterable element
def avg(list):
    list_filtered=[num for num in list if num is not None]
    res=sum(list_filtered)/len(list_filtered)
    if g_debug:
        print(f"avg of list {list} is {res}")
    return res
def sqrt_MSE(list):
    res=math.sqrt(sum(i*i for i in list if i is not None))
    if g_debug:
        print(f"sqrt_MSE of list {list} is {res}")
    return res
def emax(list):
    res=max(i for i in list if i is not None)
    if g_debug:
        print(f"max of list {list} is {res}")
    return res
def emin(list):
    res=min(i for i in list if i is not None)
    if g_debug:
        print(f"min of list {list} is {res}")
    return res
def calc_slope(list,idx=None):
	import output
	if idx is None:
		idx=[i for i in range(len(list))]
	list_filtered=[num for num in list if num is not None]
	z_vals=[(i+0.5)/g_nr_layers*output.g_specimen_thickness for i in idx if list[i] is not None]
	res=scipy.stats.linregress(list_filtered,z_vals)
	slope=res[0]
	if g_debug:
		print(f"list={list},list_filtered={list_filtered},z_vals={z_vals}")
	return slope
def rel_deviation(a,b):
    if a is None or b is None:
        res= None
    else:
        if(a>b):
            res= (a-b)/b
        else:
            res= (a-b)/a
    if g_debug:
        print(f"dev of {a} and {b} is {res}")
    return res