""" Bus functions management."""

__author__ = "Zhijie Nie"

# from psat_python27 import *
import sys

if sys.version_info[0] == 2:
    if sys.version_info[1] == 5:
	    from psat_python25 import *
    elif sys.version_info[1] == 7:
	    from psat_python27 import *
elif sys.version_info[0] == 3:
    from psat_python34 import *

error = psat_error()

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

# Returns a list of values of specified property for buses
def get_bus_prop(subsys,t,include_type=[1,2,3,4]):
    p = []
    f = psat_comp_id(ctype.bs,1,'')
    more = get_next_comp(subsys,f,error)
    while more == True:
        c = get_bus_dat(f,error)
        if c.type in include_type:
            if t == 'NUMBER':
                p.append(c.number)
            elif t == 'NAME':
                p.append(c.name)
            elif t == 'BASEKV':
                p.append(c.basekv)
            elif t == 'TYPE':
                p.append(c.type)
            elif t == 'VM':
                p.append(c.vmag)
            elif t == 'VA':
                p.append(c.vang)
            elif t == 'VREAL':
                p.append(c.vreal)
            elif t == 'VIMAG':
                p.append(c.vimag)
            elif t == 'AREA':
                p.append(c.area)
            elif t == 'ZONE':
                p.append(c.zone)
            elif t == 'OWNER':
                p.append(c.owner)
        more = get_next_comp(subsys,f,error)
    return p

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
            newarea.name = str(newarea.number)
            psat_command(r'InsertData:Area;%d;%s;Disabled;No;Null;0;1' %(newarea.number,newarea.name),error)
        for i in range(nb):
            busdat = get_bus_dat(busnum[i],error)
            loaddat = get_load_dat(busnum[i],"1",error)
            busdat.area = areanum[i]
            loaddat.area = areanum[i]
            set_bus_dat(busnum[i],busdat,error)
            set_load_dat(busnum[i],"1",loaddat,error)

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

