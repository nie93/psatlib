""" Line functions management."""

__author__ = "Zhijie Nie"

from psat_python27 import *

error = psat_error()


# Defines line contingencies (all lines by default)
def define_line_ctg(subsys, lid=None):
    ctg = []
    if lid == None:
        f = psat_comp_id(ctype.ln,1,'')
        more = get_next_comp(subsys,f,error)
        while more == True:
            c = get_line_dat(f,error)
            ctg.append(['Line', c.frbus, c.tobus, '%s ' %c.id])
            more = get_next_comp(subsys,f,error)
    return ctg

# Returns a list of values of specified property for lines
def get_line_prop(subsys,t):
    p = []
    f = psat_comp_id(ctype.ln,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        c = get_line_dat(f,error)
        if t == 'FRBUS':
            p.append(c.frbus)
        elif t == 'TOBUS':
            p.append(c.tobus)
        elif t == 'LINEID':
            p.append(c.id)
        elif t == 'STATUS':
            p.append(c.status)
        elif t == 'RSR':
            p.append(c.rsr)
        elif t == 'XSR':
            p.append(c.xsr)
        elif t == 'GCH':
            p.append(c.gch)
        elif t == 'BCH':
            p.append(c.bch)
        elif t == 'GFR':
            p.append(c.gfr)
        elif t == 'BFR':
            p.append(c.bfr)
        elif t == 'GTO':
            p.append(c.gto)
        elif t == 'BTO':
            p.append(c.bto)
        elif t == 'PFR':
            p.append(c.pfr)
        elif t == 'QFR':
            p.append(c.qfr)
        elif t == 'IFR':
            p.append(c.ifr)
        elif t == 'PTO':
            p.append(c.pto)
        elif t == 'QTO':
            p.append(c.pto)
        elif t == 'ITO':
            p.append(c.ito)
        more = get_next_comp(subsys,f,error)
    return p
