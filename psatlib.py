"""
psatlib -- An imported library designed for PSAT running with Python scripts.
"""
__name__ = "psatlib"
__version__ = "0.1"
__author__ = "Zhijie Nie"
__author_email__ = "nie@ieee.org"
__copyright__ = "Copyright (c) 2018 Zhijie Nie"
__description__ = "psatlib is an imported library designed for PSAT running with Python scripts"

from psat_python27 import *

error = psat_error()

# Returns active power loads
def get_loads_mw(busnum):
	mw = []
	for i in range(len(busnum)):
		c = get_load_dat(busnum[i],"1",error)
		mw.append(c.cp[0])	
	return mw

# Returns reactive power loads
def get_loads_mvar(busnum):
	mvar = []
	for i in range(len(busnum)):
		c = get_load_dat(busnum[i],"1",error)
		mvar.append(c.cq[0])
	return mvar

# Assigns area numbers to all buses
def assign_bus_areas(areanum):
	nb = get_count_comp(ctype.bs,error)
	nar_before = get_count_comp(ctype.ar,error)
	nar_after = len(set(areanum))
	busnum = range(1,1+nb)
	for i in range(nar_after - nar_before):
		newarea = psat_area_dat()
		newarea.number = nar_before + i + 1
		newarea.name = str(nar_before + i + 1)
		add_comp(newarea,error)
	for i in range(len(areanum)):
		c = get_bus_dat(busnum[i],error)
		c.area = areanum[i]
		set_bus_dat(busnum[i],c,error)

# Returns area numbers
def get_areas(busnum):
	area = []
	for i in range(len(busnum)):
		c = get_bus_dat(busnum[i],error)
		area.append(c.area)	
	return area