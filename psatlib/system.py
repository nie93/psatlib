""" System functions management."""

__author__ = "Zhijie Nie"

from psat_python27 import *
from . import bus
from . import load

error = psat_error()

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

# Redispatches the generators according to the capacity (PMAX)
def redispatch(subsys, mismatch, solve):
    psat_msg('inside system.py')
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
