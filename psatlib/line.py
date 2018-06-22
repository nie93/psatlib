""" Line functions management."""

__author__ = "Zhijie Nie"

from psat_python27 import *

error = psat_error()


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