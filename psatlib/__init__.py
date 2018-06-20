"""
psatlib -- An imported library designed for PSAT running with Python scripts.

Created by Zhijie Nie (nie@ieee.org)
Created on:         06/11/2018
Last Modified on:   06/20/2018
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

# Solves the powerflow if the case is not solved
def solve_if_not_solved():
    if get_solution_status() != 1:
        psat_command(r'Solve',error)
    if get_solution_status() != 1:
        psat_msg('Returned: Powerflow solution failed, initial powerflow case returned')
    return get_solution_status()

# Returns a list of values of specified property for buses
def get_bus_prop(subsys,t):
    p = []
    f = psat_comp_id(ctype.bs,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        c = get_bus_dat(f,error)
        if t == 'NUMBER':
            p.append(c.number)
        elif t == 'NAME':
            p.append(c.name)
        elif t == 'BASEKV':
            p.append(c.basekv)
        elif t == 'TYPE':
            p.append(c.type)
        elif t == 'VM':
            solve_if_not_solved()
            p.append(c.vmag)
        elif t == 'VA':
            solve_if_not_solved()
            p.append(c.vang)
        elif t == 'VREAL':
            solve_if_not_solved()
            p.append(c.vreal)
        elif t == 'VIMAG':
            solve_if_not_solved()
            p.append(c.vimag)
        elif t == 'AREA':
            p.append(c.area)
        elif t == 'ZONE':
            p.append(c.zone)
        elif t == 'OWNER':
            p.append(c.owner)
        more = get_next_comp(subsys,f,error)
    return p
    
# Returns loads (designed for single load item/component)
def get_loads(busnum):
    if type(busnum) == int:
        c = get_load_dat(busnum,"1",error)
        if c.status:
            mw = c.mw
            mvar = c.mw
        else:
            mw = 0.
            mvar = 0.
    else:
        mw = []
        mvar = []
        for i in range(len(busnum)):
            c = get_load_dat(busnum[i],"1",error)
            if c.status:
                mw.append(c.mw)
                mvar.append(c.mw)
            else:
                mw.append(0)
                mvar.append(0)
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
        psat_msg('Returned: The lenghth of `areanum` not equal the number of buses.')
    else:
        nar_before = get_count_comp(ctype.ar,error)
        nar_after = len(set(areanum))
        busnum = get_busnum(ctype.bs)
        for i in range(nar_after - nar_before):
            newarea = get_area_dat(1,error)
            newarea.number = nar_before + i + 1
            newarea.name = str(nar_before + i + 1)
            add_comp(newarea,error)
        for i in range(nb):
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

# Returns the summation of online loads 
def get_sum_load(subsys):
    mw = 0.
    mvar = 0.
    refmw = 0.
    refmvar = 0.
    f = psat_comp_id(ctype.ld,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        c = get_load_dat(f,error)
        if c.status:
            mw += c.mw
            mvar += c.mvar
            refmw += c.refmw
            refmvar += c.refmvar
        more = get_next_comp(subsys,f,error)
    return {'p':mw, 'q':mvar, 'pref':refmw, 'qref':refmvar}

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

# Gets a list of values of specified property for generators
def get_gen_prop(subsys,t):
    p = []
    f = psat_comp_id(ctype.gen,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        c = get_gen_dat(f,error)
        if t == 'BUS':
            p.append(c.bus)
        elif t == 'GENID':
            p.append(c.id)
        elif t == 'STATUS':
            p.append(c.status)
        elif t == 'BASEMVA':
            p.append(c.basemva)
        elif t == 'PG':
            p.append(c.mw)
        elif t == 'PMAX':
            p.append(c.mwmax)
        elif t == 'PMIN':
            p.append(c.mwmin)
        elif t == 'QG':
            p.append(c.mvar)
        elif t == 'QMAX':
            p.append(c.mvarmax)
        elif t == 'QMIN':
            p.append(c.mvarmin)
        more = get_next_comp(subsys,f,error)
    return p

# Sets the values of specified property for generators
def set_gen_prop(subsys,t,pset):
    if len(pset) != get_count_comp(ctype.gen,error):
        psat_msg('Returned: The lenghth of `pset` not equal the number of generators.')
    else:
        f = psat_comp_id(ctype.gen,1,'')
        more = get_next_comp(subsys,f,error)
        counter = -1
        while more == True:
            c = get_gen_dat(f,error)
            counter += 1
            if t == 'STATUS':
                c.status = pset[counter]
            elif t == 'BASEMVA':
                c.basemva = pset[counter]
            elif t == 'PG':
                c.mw = pset[counter]
            elif t == 'PMAX':
                c.mwmax = pset[counter]
            elif t == 'PMIN':
                c.mwmin = pset[counter]
            elif t == 'QG':
                c.mvar = pset[counter]
            elif t == 'QMAX':
                c.mvarmax = pset[counter]
            elif t == 'QMIN':
                c.mvarmin = pset[counter]           
            set_gen_dat(f,c,error)
            more = get_next_comp(subsys,f,error)

# Redispatches the generators according to the capacity (PMAX)
def redispatch(subsys, mismatch, solve):
    pmax = get_gen_prop(subsys,'PMAX')
    total_cap = sum(pmax)
    f = psat_comp_id(ctype.gen,1,'')
    more = get_next_comp(subsys,f,error)
    counter = -1
    if mismatch == None:
        tload = get_sum_load(subsys)
        mismatch = tload['p'] - tload['pref']
        psat_msg('P = %8.2f, PREF = %8.2f, MISMATCH = %8.2f' %(tload['p'], tload['pref'], mismatch))
    while more == True:
        c = get_gen_dat(f,error)
        counter += 1
        if c.status:
            at = get_bus_dat(c.bus,error)
            c.mw += mismatch * pmax[counter] / total_cap
            if c.mw < c.mwmin:
                c.mw = c.mwmin
            if c.mw > c.mwmax:
                c.mw = c.mwmax            
            if at.type != 3:
                set_gen_dat(f,c,error)
        more = get_next_comp(subsys,f,error)
    if solve:
        psat_command(r'SetSolutionAlgorithm:NR',error)
        psat_command(r'Solve',error)
    return

# Displays a list in PSAT message tab
def disp_list(l,transpose=0):
    if transpose:
        l = map(list, zip(*l))
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
            mw += c.mw
            mvar += c.mw
        more = get_next_comp('mainsub',f,error)
    return {'p': mw, 'q':mvar}
    
# Applys a set of changes to the imported case (inspired by MATPOWER)
def apply_changes(lbl, chgtbl):
    """
    Example of `chgtbl`:
    chgtbl = [[1, 'AREALOAD',  1,     'PQ', 'REP', 1000.], 
              [1, 'AREALOAD',  2,     'PQ', 'REP',  600.],
              [1, 'AREALOAD',  3,     'PQ', 'REP',  800.],
              [2,      'GEN', 10, 'STATUS', 'REP',    0 ],
              [2,     'LINE', 10, 'STATUS', 'REP',    0 ]]
    """
    chgid = [i for i, x in enumerate(chgtbl) if x[0] == lbl]
    for i in chgid:
        if chgtbl[i][1] == 'AREALOAD':
            areaload = get_load_in_area(chgtbl[i][2])
            psat_msg('LABEL#%3d  %s  %2d %s  %s [%8.2f -> %8.2f]' \
                     %(chgtbl[i][0], chgtbl[i][1], chgtbl[i][2], chgtbl[i][3], \
                     chgtbl[i][4], areaload['p'], chgtbl[i][5]))
            bn = get_busnum_in_area(chgtbl[i][2])
            for bi in range(len(bn)):
                c = get_load_dat(bn[bi], "1", error)
                if c.status:
                    if chgtbl[i][3] == 'P':
                        c.cp[0] = c.cp[0] * chgtbl[i][5] / areaload['p']
                    elif chgtbl[i][3] == 'PQ':
                        c.cp[0] = c.cp[0] * chgtbl[i][5] / areaload['p']
                        c.cq[0] = c.cq[0] * chgtbl[i][5] / areaload['p']
                    set_load_dat(bn[bi], "1", c, error)
        elif chgtbl[i][1] == 'GEN':
            return
        elif chgtbl[i][1] == 'LINE':
            return
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

# Gets a list of values of specified property for generators
def get_load_prop(subsys,t):
    p = []
    f = psat_comp_id(ctype.ld,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        c = get_load_dat(f,error)
        if t == 'BUS':
            p.append(c.bus)
        elif t == 'LOADID':
            p.append(c.id)
        elif t == 'STATUS':
            p.append(c.status)
        elif t == 'AREA':
            p.append(c.basemva)
        elif t == 'PREF':
            p.append(c.refmw)
        elif t == 'QREF':
            p.append(c.refmvar)
        elif t == 'PNOM':
            p.append(c.nommw)
        elif t == 'QNOM':
            p.append(c.nommvar)
        elif t == 'PD':
            p.append(c.mw)
        elif t == 'QD':
            p.append(c.mvar)
        more = get_next_comp(subsys,f,error)
    return p

# Sets the values of specified property for loads
def set_load_prop(subsys,t,pset):
    if len(pset) != get_count_comp(ctype.ld,error):
        psat_msg('Returned: The lenghth of `pset` not equal the number of loads.')
    else:
        f = psat_comp_id(ctype.ld,1,'')
        more = get_next_comp(subsys,f,error)
        counter = -1
        while more == True:
            c = get_load_dat(f,error)
            counter += 1
            if t == 'STATUS':
                c.status = pset[counter]
            elif t == 'AREA':
                c.area = pset[counter]
            elif t == 'PREF':
                c.refmw = pset[counter]
            elif t == 'QREF':
                c.refmvar = pset[counter]
            elif t == 'PNOM':
                c.nommw = pset[counter]
            elif t == 'QNOM':
                c.nommvar = pset[counter]
            elif t == 'PD':
                c.mw = pset[counter]
            elif t == 'QD':
                c.mvar = pset[counter]
            set_load_dat(f,c,error)
            more = get_next_comp(subsys,f,error)

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

# Generates VSAT files for transient stability analysis (psb,dyr,swi,mon)
def generate_vsa():
    return
