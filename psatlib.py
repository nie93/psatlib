"""
psatlib -- An imported library designed for PSAT running with Python scripts.

Created by Zhijie Nie (nie@ieee.org)
Created on:         06/11/2018
Last Modified on:   06/14/2018
"""
__name__ = "psatlib"
__version__ = "0.1"
__author__ = "Zhijie Nie"
__author_email__ = "nie@ieee.org"
__copyright__ = "Copyright (c) 2018 Zhijie Nie"
__description__ = "psatlib is an imported library designed for PSAT running with Python scripts"

from psat_python27 import *
error = psat_error()

# Resets all load id as the ascending string of integers
def reset_loadid():
    counter = 1
    f = psat_comp_id(ctype.ld,1,'')
    c = get_load_dat(f,error)
    c.id = str(counter)
    set_load_dat(f,c,error)
    prev = get_load_dat(f,error)
    more = get_next_comp('mainsub',f,error)
    while more == True:
        c = get_load_dat(f,error)
        if samebus(prev, c):
            counter += 1
        else:
            counter = 1
        c.id = str(counter)
        set_load_dat(f,c,error)
        more = get_next_comp('mainsub',f,error)  
        prev = c

# Returns True if the two components are at the same bus
def samebus(c1,c2):
    if c1.bus == c2.bus:
        return True
    else:    
        return False

# Returns a list of bus numbers of certain type of components
def get_busnum(ct):
    f = psat_comp_id(ct,1,'')
    bn = []
    more = get_next_comp('mainsub',f,error)
    while more == True:
        bn.append(f.bus)
        more = get_next_comp('mainsub',f,error)
    bn.sort()
    return bn

# Returns loads (designed for single load item/component)
def get_loads(busnum):
    if type(busnum) == int:
        c = get_load_dat(busnum,"1",error)
        mw = c.cp[0]
        mvar = c.cq[0]
    else:
        mw = []
        mvar = []
        for i in range(len(busnum)):
            c = get_load_dat(busnum[i],"1",error)
            mw.append(c.cp[0])
            mvar.append(c.cq[0])
    return {'p':mw, 'q':mvar}

# Returns aggregated loads by area (designed for single load item/component)
def get_aggloads_by_area(areanum):
    areanum = list(set(areanum))
    areanum.sort()
    mw = [0.] * len(areanum)
    mvar = [0.] * len(areanum)
    f = psat_comp_id(ctype.ld,1,'')
    more = get_next_comp('mainsub',f,error)
    while more == True:
        c = get_load_dat(f,error)
        if c.status == 1:
            mw[areanum.index(c.area)] += c.mw
            mvar[areanum.index(c.area)] += c.mvar
        more = get_next_comp('mainsub',f,error)
    return {'area': areanum, 'p':mw, 'q':mvar}

# Set area numbers for all buses
def set_bus_areas(areanum):
    nb = get_count_comp(ctype.bs,error)
    if nb != len(areanum):
        return
    else:
        nar_before = get_count_comp(ctype.ar,error)
        nar_after = len(set(areanum))
        busnum = range(1,1+nb)            # Obselete
        # busnum = get_busnum(ctype.bs)   # Not checked yet
        for i in range(nar_after - nar_before):
            newarea = psat_area_dat()
            newarea.number = nar_before + i + 1
            newarea.name = str(nar_before + i + 1)
            add_comp(newarea,error)
        for i in range(len(areanum)):
            busdat = get_bus_dat(busnum[i],error)
            loaddat = get_load_dat(busnum[i],"1",error)
            busdat.area = areanum[i]
            loaddat.area = areanum[i]
            set_bus_dat(busnum[i],busdat,error)
            set_load_dat(busnum[i],"1",loaddat,error)

# Returns the list of area numbers
def get_areanum(busnum):
    area = []
    for i in range(len(busnum)):
        c = get_bus_dat(busnum[i],error)
        area.append(c.area)    
    return area

# Displays components information
def disp_comp_msg(ct):
    f = psat_comp_id(ct,1,'')
    more = get_next_comp('mainsub',f,error)
    while more == True:
        if f.type == ctype.ld:
            c = get_load_dat(f,error)
            msg_str = '%9s AT BUS #%3d (AREA #%2d), {P:%8.2f, Q:%8.2f}' \
                    %('LOAD', c.bus, c.area, c.mw, c.mvar)
        elif f.type == ctype.gen:
            c = get_gen_dat(f,error)
            msg_str = '%9s AT BUS #%3d, {P:%8.2f, Q:%8.2f} ST:%d' \
                    %('GENERATOR', c.bus, c.mw, c.mvar, c.status)        
        psat_msg(msg_str)
        more = get_next_comp('mainsub',f,error)

# Scales load
def scale_loads(subsys, x):
    f = psat_comp_id(ctype.ld,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        c = get_load_dat(f,error)
        c.cp[0] = x * c.cp[0]
        c.cq[0] = x * c.cq[0]
        set_load_dat(f,c,error)
        more = get_next_comp(subsys,f,error)

# Returns the summation of loads 
def get_sum_load(subsys):
    mw = 0.
    mvar = 0.
    f = psat_comp_id(ctype.ld,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        loaddat = get_load_dat(f,error)
        mw += loaddat.mw
        mvar += loaddat.mvar
        more = get_next_comp(subsys,f,error)
    return {'p':mw, 'q':mvar}

# Returns the summation of generators outputs
def get_sum_genoutput(subsys):
    mw = 0.
    mvar = 0.
    f = psat_comp_id(ctype.gen,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        gendat = get_gen_dat(f,error)
        mw += gendat.mw
        mvar += gendat.mvar
        more = get_next_comp(subsys,f,error)
    return {'p':mw, 'q':mvar}

# Returns the summation of fixed shunt reactive power injection
def get_sum_fxshmvar(subsys):
    mvar = 0.
    f = psat_comp_id(ctype.fxsh,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        fxshdat = get_fx_shunt_dat(f,error)
        mvar += fxshdat.mvar
        more = get_next_comp(subsys,f,error)
    return mvar

# Rescales generator outputs (fixed shunt reactive power injection considered)
def rescale_gens(subsys):
    genoutput = get_sum_genoutput(subsys)
    load = get_sum_load(subsys)
    fxshmvar = get_sum_fxshmvar(subsys)
    xp = load['p'] / genoutput['p'] 
    xq = load['q'] / (genoutput['q'] + fxshmvar)
    f = psat_comp_id(ctype.gen,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        c = get_gen_dat(f,error)
        c.mw = xp * c.mw
        c.mvar = xq * c.mvar
        set_gen_dat(f,c,error)
        more = get_next_comp(subsys,f,error)

# Gets a list of maximum active power outputs for generators
def get_gen_pmax(subsys):
    pmax = []
    f = psat_comp_id(ctype.gen,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        c = get_gen_dat(f,error)
        pmax.append(c.mwmax)
        more = get_next_comp(subsys,f,error)
    return pmax

# Sets maximum active power outputs for generators
def set_gen_pmax(subsys,pmax):
    if len(pmax) != get_count_comp(ctype.gen,error):
        psat_msg('Returned: The lenghth of `pmax` not equal the number of generators.')
    else:
        f = psat_comp_id(ctype.gen,1,'')
        more = get_next_comp(subsys,f,error)
        counter = -1
        while more == True:
            c = get_gen_dat(f,error)
            counter += 1
            c.mwmax = pmax[counter]
            set_gen_dat(f,c,error)
            more = get_next_comp(subsys,f,error)

# Redispatches the generators according to the capacity (PMAX)
def redispatch(subsys, mismatch, solve):
    pmax = get_gen_pmax(subsys)
    total_cap = sum(pmax)
    f = psat_comp_id(ctype.gen,1,'')
    more = get_next_comp(subsys,f,error)
    counter = -1
    while more == True:
        c = get_gen_dat(f,error)
        counter += 1
        c.mwmax += mismatch * pmax[counter] / total_cap
        set_gen_dat(f,c,error)
        more = get_next_comp(subsys,f,error)
    if solve:
        psat_command(r'SetSolutionAlgorithm:NR',error)
        psat_command(r'Solve',error)
    return

# Displays a list in PSAT message tab
def disp_list(l):
    for i in range(len(l)):
        psat_msg(str(l[i]))

# Returns a list of bus numbers in a specified area
def get_busnum_in_area(areanum):
    f = psat_comp_id(ctype.bs,1,'')
    bn = []
    more = get_next_comp('mainsub',f,error)
    while more == True:
        c = get_bus_dat(f,error)
        if c.area == areanum:
            bn.append(c.number)
        more = get_next_comp('mainsub',f,error)
    bn.sort()
    return bn

# Returns the load in a specified area
def get_load_in_area(areanum):
    f = psat_comp_id(ctype.ld,1,'')
    mw = 0.
    mvar = 0.
    more = get_next_comp('mainsub',f,error)
    while more == True:
        c = get_load_dat(f,error)
        if (c.area == areanum and c.status == 1):
            mw += c.cp[0]
            mvar += c.cq[0]
        more = get_next_comp('mainsub',f,error)
    return {'p': mw, 'q':mvar}
    
# Applys a set of changes to the imported case (inspired by MATPOWER)
def apply_changes(lbl, chgtbl):
    chgid = [i for i, x in enumerate(chgtbl) if x[0] == lbl]
    for i in chgid:
        # psat_msg('LABEL#%3d  %s  %2d %s  %s [%8.2f -> %8.2f]' \
        #          %(chgtbl[i][0], chgtbl[i][1], chgtbl[i][2], chgtbl[i][3], \
        #            chgtbl[i][4], areaload['p'], chgtbl[i][5]))
        if chgtbl[i][1] == 'AREALOAD':
            areaload = get_load_in_area(chgtbl[i][2])
            bn = get_busnum_in_area(chgtbl[i][2])
            for bi in range(len(bn)):
                c = get_load_dat(bn[bi], "1", error)
                if chgtbl[i][3] == 'P':
                    c.cp[0] = c.cp[0] * chgtbl[i][5] / areaload['p']
                elif chgtbl[i][3] == 'PQ':
                    c.cp[0] = c.cp[0] * chgtbl[i][5] / areaload['p']
                    c.cq[0] = c.cq[0] * chgtbl[i][5] / areaload['p']
                set_load_dat(bn[bi], "1", c, error)
        elif chgtbl[i][1] == 'BUSLOAD':
            return
    return

# Returns a list of components' ids of specified type whose bus numbers are in the list of bn
def get_comp_id(ct,bn):
    cid = []
    if type(bn) != list:
        bn = [bn]
    f = psat_comp_id(ct,1,'')    
    more = get_next_comp('mainsub',f,error)
    while more == True:
        if bool(set([f.bus,f.bus2, f.bus3, f.bus4]) & set(bn)):
            cid.append(f)
        more = get_next_comp('mainsub',f,error)
    return cid

# Returns a list of psat component data according to psat_comp_id
def get_comp_dat(cid):  
    c = []
    if type(cid) != list:
        cid = [cid]
    for i in range(len(cid)):
        if cid[i].type == ctype.bs:
            c.append(get_bus_dat(cid[i],error))
        elif cid[i].type == ctype.gen:
            c.append(get_gen_dat(cid[i],error))
        elif cid[i].type == ctype.ld:
            c.append(get_load_dat(cid[i],error))
        elif cid[i].type == ctype.fxsh:
            c.append(get_fix_shunt_dat(cid[i],error))
        elif cid[i].type == ctype.swsh:
            c.append(get_sw_shunt_dat(cid[i],error))
        elif cid[i].type == ctype.ln:
            c.append(get_line_dat(cid[i],error))
        elif cid[i].type == ctype.fxtr:
            c.append(get_fx_trans_dat(cid[i],error))
        elif cid[i].type == ctype.ultc:
            c.append(get_2w_trans_dat(cid[i],error))
        elif cid[i].type == ctype.twtr:
            c.append(get_3w_trans_dat(cid[i],error))
        elif cid[i].type == ctype.fxsc:
            c.append(get_fx_sercomp_dat(cid[i],error))
        elif cid[i].type == ctype.vrsc:
            c.append(get_fx_sercomp_dat(cid[i],error))
        elif cid[i].type == ctype.stcpr:
            c.append(get_stcpr_dat(cid[i],error))
        elif cid[i].type == ctype.dcbs:
            c.append(get_dcbus_dat(cid[i],error))
        elif cid[i].type == ctype.cnvrtr:
            c.append(get_converter_dat(cid[i],error))
        elif cid[i].type == ctype.vsc:
            c.append(get_vsc_dat(cid[i],error))
        elif cid[i].type == ctype.dcln:
            c.append(get_dcline_dat(cid[i],error))
        elif cid[i].type == ctype.dcbrkr:
            c.append(get_dcbrkr_dat(cid[i],error))
        elif cid[i].type == ctype.zseq:
            c.append(get_z_seq_coupling_dat(cid[i],error))
    return c

# Returns a list of flow on transmission lines
def get_branch_flow(brnum):
    
    bf = []

    return

# Returns a list of flow on fixed transformers
def get_fxtr_flow(brnum):
    return

# Returns a list of flow on adjustable (two-winding) transformers
def get_ultc_flow(brnum):
    return

# Returns a list of flow on three-winding transformers
def get_twtr_flow(brnum):
    return

# Generates TSAT files for transient stability analysis (psb,dyr,swi,mon)
def generate_tsa(path,psb,dyr,swi,mon):
    return
