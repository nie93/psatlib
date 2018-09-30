""" Generator functions management."""

__author__ = "Zhijie Nie"

import sys

if sys.version_info[0] == 2:
    if sys.version_info[1] == 5:
	    from psat_python25 import *
    elif sys.version_info[1] == 7:
	    from psat_python27 import *
elif sys.version_info[0] == 3:
    from psat_python34 import *

error = psat_error()

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
def get_gen_prop(subsys,t, exclude=[]):
    p = []
    f = psat_comp_id(ctype.gen,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        c = get_gen_dat(f,error)
        if c.bus not in exclude:
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


# Gets a list of values of specified properties for generators
def get_gen_props(subsys,*args):
    l = []
    f = psat_comp_id(ctype.gen,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        c = get_gen_dat(f,error)
        p = []
        for t in args:
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
        l.append(p)
        more = get_next_comp(subsys,f,error)
    return l

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

# Returns the summation of generators outputs (will be replaced)
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
