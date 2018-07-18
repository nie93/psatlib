""" System functions management."""

__author__ = "Zhijie Nie"

from psat_python27 import *
from .bus import *
from .load import *
from .line import *


error = psat_error()

# Applys a set of changes to the imported case (inspired by MATPOWER)
def apply_changes(lbl, chgtbl):
    """
    Example of `chgtbl`:
    chgtbl = [[1, 'AREALOAD',  1,     'PQ', 'REP', 1000.], 
              [1, 'AREALOAD',  2,     'PQ', 'REP',  600.],
              [1, 'AREALOAD',  3,     'PQ', 'REP',  800.],
              [2,      'GEN', 10, 'STATUS', 'REP',    0 ],
              [2,     'LINE', 10, 'STATUS', 'REP',    0 ],
              [3,     'LOAD',  5,      'P', 'REL', 0.90 ],
              [3,     'LOAD', 11,     'PQ', 'REL', 0.95 ]]
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
        elif chgtbl[i][1] == 'LOAD':
            c = get_load_dat(chgtbl[i][2], "1", error)
            if c.status:
                if chgtbl[i][4] == 'REL':
                    if chgtbl[i][3] == 'P':
                        c.cp[0] = c.refmw * chgtbl[i][5]
                    elif chgtbl[i][3] == 'PQ':
                        c.cp[0] = c.refmw * chgtbl[i][5]
                        c.cq[0] = c.refmvar * chgtbl[i][5]
                    if c.cp[0] < 0:
                        c.cp[0] = 0
                    if c.cq[0] < 0:
                        c.cq[0] = 0
                elif chgtbl[i][4] == 'REP':
                    if chgtbl[i][3] == 'P':
                        c.cp[0] = chgtbl[i][5]
                    elif chgtbl[i][3] == 'PQ':
                        c.cp[0] = chgtbl[i][5]
                        c.cq[0] = chgtbl[i][5] * c.cq[0] / c.cp[0]
                set_load_dat(chgtbl[i][2], "1", c, error)
        elif chgtbl[i][1] == 'GEN':
            c = get_gen_dat(chgtbl[i][2], "1", error)
            if chgtbl[i][4] == 'REP':
                if chgtbl[i][3] == 'STATUS':
                    c.status = chgtbl[i][5]
            set_gen_dat(chgtbl[i][2], "1", c, error)
        elif chgtbl[i][1] == 'LINE':
            c = get_line_dat(chgtbl[i][2][0], chgtbl[i][2][1], chgtbl[i][2][2], 
                             0, error)
            if chgtbl[i][4] == 'REP':
                if chgtbl[i][3] == 'STATUS':
                    c.status = chgtbl[i][5]
            set_line_dat(chgtbl[i][2][0], chgtbl[i][2][1], chgtbl[i][2][2], 
                         0, c, error)
    return

# Redispatches the generators according to the capacity (PMAX)
def redispatch(subsys='mainsub', pgref=None, transfer=None, solve=False):
    if transfer is None:
        pmax = get_gen_prop(subsys,'PMAX')
        tcap = sum(pmax)
        f = psat_comp_id(ctype.gen,1,'')
        more = get_next_comp(subsys,f,error)
        counter = -1
        tload = sum(get_load_prop(subsys, 'PD'))
        if pgref is None:
            tloadref = sum(get_load_prop(subsys, 'PREF'))
            mismatch = tload - tloadref
            psat_msg('P = %8.2f MW, PREF = %8.2f MW, MISMATCH = %8.2f MW' %(tload, tloadref, mismatch))
            while more == True:
                c = get_gen_dat(f,error)
                counter += 1
                if c.status:
                    at = get_bus_dat(c.bus,error)
                    c.mw += mismatch * pmax[counter] / tcap
                    if c.mw < c.mwmin:
                        c.mw = c.mwmin
                    if c.mw > c.mwmax:
                        c.mw = c.mwmax            
                    if at.type != 3:
                        set_gen_dat(f,c,error)
                more = get_next_comp(subsys,f,error)
        else:
            mismatch = tload - sum(pgref)
            psat_msg('P = %8.2f MW, PREF = %8.2f MW, MISMATCH = %8.2f MW' %(tload, sum(pgref), mismatch))
            while more == True:
                c = get_gen_dat(f,error)
                counter += 1
                if c.status:
                    at = get_bus_dat(c.bus,error)
                    c.mw = pgref[counter] + mismatch * pmax[counter] / tcap
                    if c.mw < c.mwmin:
                        c.mw = c.mwmin
                    if c.mw > c.mwmax:
                        c.mw = c.mwmax            
                    if at.type != 3:
                        set_gen_dat(f,c,error)
                more = get_next_comp(subsys,f,error)
    else:
        exc_gbus = [gbus for item in transfer for gbus in item[1]]
        exc_lbus = [item[0] for item in transfer]
        
        pmax = get_gen_prop(subsys,'PMAX')
        tcap = sum(pmax)
        tload = sum(get_load_prop(subsys, 'PD'))
        restcap = sum(get_gen_prop(subsys,'PMAX', exc_gbus))
        restload = sum(get_load_prop(subsys, 'PD', exc_lbus))
        restpgref = [item[1] for item in pgref if item[0] not in exc_gbus]
        mismatch = restload - sum(restpgref)
        psat_msg('P = %8.2f MW, PREF = %8.2f MW, MISMATCH = %8.2f MW' %(restload, sum(restpgref), mismatch))

        f = psat_comp_id(ctype.gen,1,'')
        more = get_next_comp(subsys,f,error)
        while more == True:
            c = get_gen_dat(f,error)
            if c.status:
                pg = [item[1] for item in pgref if item[0] == c.bus]
                at = get_bus_dat(c.bus,error)
                if c.bus in exc_gbus:
                    lbus = [lb for lb,gb in transfer if c.bus in gb]
                    load = get_load_dat(lbus[0], '1', error)
                    c.mw = pg[0] * load.mw / load.refmw 
                    if c.mw < c.mwmin:
                        c.mw = c.mwmin
                    if c.mw > c.mwmax:
                        c.mw = c.mwmax           
                else:
                    c.mw = pg[0] + mismatch * pmax[c.bus-1] / restcap
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

# Creates snapshot of current powerflow result
def create_snapshot(r):
    l = []
    if 'Solved' in r.keys():
        l.append([get_solution_status()])
    if 'Bus' in r.keys():
        for i in r['Bus']:
            l.append(get_bus_prop('mainsub', i))
    if 'Load' in r.keys():
        for i in r['Load']:
            l.append(get_load_prop('mainsub', i))
    if 'Line' in r.keys():
        for i in r['Line']:
            l.append(get_line_prop('mainsub', i))         
    flattened = [val for sublist in l for val in sublist]
    return flattened

def create_snapshot_header(r):
    h = []
    if 'Solved' in r.keys():
        h.append(['SOLVED'])
    if 'Bus' in r.keys():
        busnum = get_bus_prop('mainsub', 'NUMBER')
        for i in r['Bus']:
            h.append(['Bus_' + str(val) + '_' + i  for val in busnum])
    if 'Load' in r.keys():
        busnum = get_load_prop('mainsub', 'BUS')
        for i in r['Load']:
            h.append(['Load_' + str(val) + '_' + i for val in busnum])
    if 'Line' in r.keys():
        frbus = get_line_prop('mainsub', 'FRBUS')
        tobus = get_line_prop('mainsub', 'TOBUS')
        lid = get_line_prop('mainsub', 'LINEID')
        lhdr = []
        for k in r['Line']:
            for i in range(len(frbus)):
                lhdr.append('Line_%d_%d_%s_%s' %(frbus[i], tobus[i], lid[i], k))
        h.append(lhdr)
	
    flattened = [val for sublist in h for val in sublist]
    return flattened