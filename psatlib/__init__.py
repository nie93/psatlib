"""
psatlib -- An imported library designed for PSAT running with Python scripts.

Created by Zhijie Nie (nie@ieee.org)
Created on:         06/11/2018
Last Modified on:   09/30/2018
"""
__name__ = "psatlib"
__version__ = "0.1"
__author__ = "Zhijie Nie"
__author_email__ = "nie@ieee.org"
__copyright__ = "Copyright (c) 2018 Zhijie Nie"
__description__ = "psatlib is an imported library designed for PSAT running with Python scripts"

import sys

if sys.version_info[0] == 2:
    if sys.version_info[1] == 5:
	    from psat_python25 import *
    elif sys.version_info[1] == 7:
	    from psat_python27 import *
elif sys.version_info[0] == 3:
    from psat_python34 import *

psat_msg(str(sys.version_info[0]))
psat_msg(str(sys.version_info[1]))
psat_msg(str(sys.version_info[2]))
error = psat_error()

# Sets customized PSAT solving environment variables
def set_psat_env(algo='NR', iter=20, failopt=0, flat=False, msgdisabled=False):
    psat_command(r'SetSolutionAlgorithm:%s' %algo, error)
    psat_command(r'SetSolutionParameter:MaxIterations;%d' %iter, error)
    psat_command(r'SetSolutionParameter:SolutionTolerance;1', error)
    if flat:
        psat_command(r'SetSolutionParameter:FlatStart;FLAT', error)        
    set_solution_failure_option(failopt)
    disable_engine_messages(msgdisabled)
    return

# Returns True if the two components are at the same bus
def samebus(c1,c2):
    if c1.bus == c2.bus:
        return True
    else:    
        return False

# Solves the powerflow if the case is not solved
def solve_if_not_solved(flat=False):
    if get_solution_status() == 0:
        if flat:
            psat_command(r'SetSolutionParameter:FlatStart;FLAT', error)
        psat_msg('Imported case is not solved, initializing powerflow solution using NR method.')
        psat_command(r'SetSolutionAlgorithm:NR',error)
        psat_command(r'Solve',error)
    if get_solution_status() != 1:
        psat_msg('Returned: Powerflow solution failed, initial powerflow case returned')
    return get_solution_status()

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

# Returns the summation of fixed shunt reactive power injection (will be replaced by get_fxsh_prop())
def get_sum_fxshmvar(subsys):
    mvar = 0.
    f = psat_comp_id(ctype.fxsh,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        fxshdat = get_fx_shunt_dat(f,error)
        mvar += fxshdat.mvar
        more = get_next_comp(subsys,f,error)
    return mvar

# Displays a list in PSAT message tab
def disp_list(l,transpose=0):
    if transpose:
        l = list(zip(*l))
    for i in l:
        psat_msg(str(i))

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

# Generates VSAT files for transient stability analysis (psb,dyr,swi,mon)
def generate_vsa():
    return
