from psat_python import *
from UserScripts.psatlib import *

disable_engine_messages(True)
error = psat_error()

psat_command(r'OpenPowerflow:"C:\\DSATools_18-SL\\Psat\\samples\\test.pfb"',error)
# psat_command(r'OpenPowerflow:"C:\\DSATools_18-SL\\Tsat\\compload\\compload.pfb"',error)
reset_loadid()
psat_command(r'Solve',error)

num_of_buses = get_count_comp(ctype.bs,error)
num_of_loads = get_count_comp(ctype.ld,error)
num_of_areas = get_count_comp(ctype.ar,error)
num_of_gens = get_count_comp(ctype.gen,error)

busnum = range(1,1+num_of_buses)
load0 = get_loads(busnum)

psat_msg('      Number of Buses: %3d' %num_of_buses)
psat_msg('      Number of Loads: %3d' %num_of_loads)
psat_msg('      Number of Areas: %3d' %num_of_areas)
psat_msg(' Number of Generators: %3d' %num_of_gens)

psat_msg('[BUSNUM, PLOAD, QLOAD]')
l = [busnum, load0['p'], load0['q']]
l = map(list, zip(*l))
disp_list(l)

# psat_command(r'CloseProject',error)