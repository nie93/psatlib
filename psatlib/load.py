""" Load functions management."""

__author__ = "Zhijie Nie"

from psat_python27 import *

error = psat_error()
  
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
