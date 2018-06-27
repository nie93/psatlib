import os
import datetime
import random
# import numpy as np

from psat_python import *
from UserScripts.psatlib import *
from UserScripts.psatlib.area import *
from UserScripts.psatlib.bus import *
from UserScripts.psatlib.generator import *
from UserScripts.psatlib.io import *
from UserScripts.psatlib.line import *
from UserScripts.psatlib.load import *
from UserScripts.psatlib.system import *


# Displays basics information 
def disp_system_basics():
    psat_msg('     BUSNUM: %s' %str(busnum))
    psat_msg(' LOADBUSNUM: %s' %str(loadbusnum))
    psat_msg('  GENBUSNUM: %s' %str(genbusnum))
    psat_msg('    AREANUM: %s' %str(areanum))
    psat_msg('         PD: %s' %str(pload0))
    psat_msg('         QD: %s' %str(qload0))
    psat_msg('[0]AREA_NUM: %s' %str(areaload0['area']))
    psat_msg('[0] AREA_PD: %s' %str(areaload0['p']))
    psat_msg('[0] AREA_QD: %s' %str(areaload0['q']))
    psat_msg(r'================================================')
    psat_msg('      Number of Buses: %3d' %num_of_buses)
    psat_msg('      Number of Loads: %3d' %num_of_loads)
    psat_msg('      Number of Areas: %3d' %num_of_areas)
    psat_msg(' Number of Generators: %3d' %num_of_gens)
    psat_msg(r'================================================')
    psat_msg('sumPG:%8.2f MW, sumQG:%8.2f MVAr' %(sum_genoutput0['p'], sum_genoutput0['q']))
    psat_msg('sumPD:%8.2f MW, sumQD:%8.2f MVAr' %(sum(pload0), sum(qload0)))

# Creates change table regarding to different loadding conditions
def create_chgtbl(busnum, n, exclude=None):
    chgtbl = []
    for i in range(n):
        for bi in busnum:
            rndscale = random.gauss(1.5, 0.4)
            # rndscale = random.uniform(0.9, 1.1)
            if exclude is not None:
                if bi not in exclude:
                    chgtbl.append([i+1, 'LOAD', bi, 'PQ', 'REL', rndscale])
            else:
                chgtbl.append([i+1, 'LOAD', bi, 'PQ', 'REL', rndscale])
    return chgtbl


psat_msg(str(datetime.datetime.now()))
error = psat_error()
disable_engine_messages(True)  # ???

# region [Import Powerflow Case - case33bw] 
casefile_path = r'C:\\YOUR_PROJ_FOLDER'
casefile_name = r'case33bw'
save_folder = 'testsave'
output_folder = 'output'
psat_command('OpenPowerflow:"%s\\%s.pfb"' %(casefile_path, casefile_name), error)
solve_if_not_solved()

reset_loadid()
# endregion

# region [Case Parameters Initialization]
busnum = get_busnum(ctype.bs)
loadbusnum = get_busnum(ctype.ld)
genbusnum = get_busnum(ctype.gen)
areanum = get_bus_prop('mainsub', 'AREA')
pload0 = get_load_prop('mainsub', 'PD')
qload0 = get_load_prop('mainsub', 'QD')
areaload0 = get_aggloads_by_area(areanum)

num_of_buses = get_count_comp(ctype.bs,error)
num_of_loads = get_count_comp(ctype.ld,error)
num_of_areas = get_count_comp(ctype.ar,error)
num_of_gens = get_count_comp(ctype.gen,error)

sum_genoutput0 = get_sum_genoutput('mainsub')

psat_msg(r'=================== SYSTEM =====================')
psat_msg('PDSUM = %8.2f MW' %sum(pload0))
psat_msg('QDSUM = %8.2f MVAr' %sum(qload0))

disp_system_basics()

# endregion


# region [Testing Environment]
psat_msg(r'=================== TESTING ====================')
zipload_busnum = [18]


num_of_cases = int(5e1)

queried = {'Bus':['VM'], \
           'Load':['PD', 'QD'], \
          }

hdr = create_snapshot_header(queried)

for kk in range(4):
	chgtbl = create_chgtbl(loadbusnum, num_of_cases)

	loglist = []
	for i in range(num_of_cases):
		apply_changes(i+1, chgtbl)
		solve_if_not_solved()
		loglist.append(create_snapshot(queried))
	list2csv(r'%s\\%s\\test_prezip_snapshots_%02d.csv' %(casefile_path, output_folder, kk+1), loglist, 0, hdr)

	loglist = []
	for i in range(num_of_cases):
		apply_changes(i+1, chgtbl)
		apply_zipload(zipload_busnum, {'kp': 0.5, 'ki': 0.25, 'kz': 0.25})
		solve_if_not_solved()
		loglist.append(create_snapshot(queried))
	list2csv(r'%s\\%s\\test_postzip_snapshots_%02d.csv' %(casefile_path, output_folder, kk+1), loglist, 0, hdr)


psat_msg(r'================= DONE TESTING =================')
# psat_command(r'CloseProject',error)
# psat_command(r'SaveMessagesToFile:"%s\\%s\\psat_msg.txt"' %(casefile_path, output_folder), error)