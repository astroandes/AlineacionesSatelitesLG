import numpy as np
import glob
import os
def load_summary(filename):
    dtype=[('minr', 'f8'),
           ('maxr', 'f8'), 
           ('ca_ratio', 'f8'),
           ('ba_ratio', 'f8'),
           ('a', 'f8'),
           ('center', 'f8'),
           ('width', 'f8'),
           ('mu', 'f8')]
    summary = np.loadtxt(filename, dtype=dtype)    
    return summary

def load_experiment(input_path="../data/mstar_selected_summary/vmax_sorted/", n_sat=11, full_data=False):
    files = glob.glob(input_path+"M31_group_*_nsat_{}.dat".format(n_sat))
    group_id = []
    for f in files:
        i = int(f.split("_")[-3])
        if i not in group_id:
            group_id.append(i)
    #print(group_id, len(group_id))

    n_groups = len(group_id)
    
    fields = ['width','mu', 'a', 'ba_ratio', 'ca_ratio']
    M31_all = {}
    MW_all = {}
    if full_data:
        for field in fields:
            M31_all[field] = np.empty((0))
            MW_all[field] = np.empty((0))
            M31_all[field+'_random'] = np.empty((0))
            MW_all[field+'_random'] = np.empty((0))
    else:
        for field in fields:
            M31_all[field] = np.ones(n_groups)
            MW_all[field] = np.ones(n_groups)
            M31_all[field+'_sigma'] = np.ones(n_groups)
            MW_all[field+'_sigma'] = np.ones(n_groups)
        
            M31_all[field+'_random'] = np.ones(n_groups)
            MW_all[field+'_random'] = np.ones(n_groups)
            M31_all[field+'_random_sigma'] = np.ones(n_groups)
            MW_all[field+'_random_sigma'] = np.ones(n_groups)

    for g in range(n_groups):
        MW_summary = {}
        M31_summary = {}
    
        filename_MW = os.path.join(input_path,"MW_group_{}_nsat_{}.dat".format(group_id[g],n_sat))
        filename_M31 = os.path.join(input_path,"M31_group_{}_nsat_{}.dat".format(group_id[g],n_sat))

        MW_summary[g] = load_summary(filename_MW)
        M31_summary[g] = load_summary(filename_M31)
    
    
    for field in fields:
        a = np.empty((0))
        b = np.empty((0))
        a_random = np.empty((0))
        b_random = np.empty((0))
        
        for g in range(n_groups):
            data = M31_summary[i]
            a = np.append(a, data[field][0])
            a_random = np.append(a_random, data[field][1:101])
        
            data = MW_summary[i]
            b = np.append(b, data[field][0])
            b_random = np.append(b_random, data[field][1:101])
                #print('a_random {} iter: {} {}'.format(field, i, a_random))
           
            if full_data:
                M31_all[field] = np.append(M31_all[field], a)
                MW_all[field] = np.append(MW_all[field], b)
                M31_all[field+'_random'] = np.append(M31_all[field+'_random'], a_random)
                MW_all[field+'_random'] = np.append(MW_all[field+'_random'], b_random)
            else:
                M31_all[field][g] = np.average(a)
                MW_all[field][g] = np.average(b)
                M31_all[field+'_sigma'][g] = np.std(a)
                MW_all[field+'_sigma'][g] = np.std(b)
                M31_all[field+'_random'][g] = np.average(a_random)
                MW_all[field+'_random'][g] = np.average(b_random)
                M31_all[field+'_random_sigma'][g] = np.std(a_random)
                MW_all[field+'_random_sigma'][g] = np.std(b_random)
                
    return M31_all, MW_all


for n_sat in range(11, 16):
    print("OBSERVATIONS - NSAT = {}".format(n_sat))
    in_path = "../data/obs_summary/"
    M31_obs_stats, MW_obs_stats = load_experiment(input_path=in_path, n_sat=n_sat, full_data=False)

    fields = ['width','ba_ratio', 'ca_ratio']
    print("M31 values\nField & Physical & Random & Normalized")
    for field in fields:
        print(field, M31_obs_stats[field], M31_obs_stats[field+'_random'], 
          (M31_obs_stats[field]-M31_obs_stats[field+'_random'])/M31_obs_stats[field+'_random_sigma'])
    print()
    print("MW values\nField & Physical & Random & Normalized")
    for field in fields:
        print(field, MW_obs_stats[field], MW_obs_stats[field+'_random'], 
          (MW_obs_stats[field]-M31_obs_stats[field+'_random'])/MW_obs_stats[field+'_random_sigma'])
    print()
    print()