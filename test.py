from psat_python import *
from UserScripts.psatlib import *

disable_engine_messages(True)
error = psat_error()

psat_command(r'OpenPowerflow:"C:\\DSATools_18-SL\\Tsat\\compload\\compload.pfb"',error)

psat_command(r'Solve',error)

num_of_buses = get_count_comp(ctype.bs,error)
num_of_loads = get_count_comp(ctype.ld,error)
num_of_areas = get_count_comp(ctype.ar,error)
num_of_gens = get_count_comp(ctype.gen,error)

busnum = range(1,1+num_of_buses)
pload0 = get_loads_mw(busnum)
qload0 = get_loads_mvar(busnum)

psat_msg('      Number of Buses: %3d' %num_of_buses)
psat_msg('      Number of Loads: %3d' %num_of_loads)
psat_msg('      Number of Areas: %3d' %num_of_areas)
psat_msg(' Number of Generators: %3d' %num_of_gens)

psat_msg(str(busnum))
psat_msg(str(pload0))
psat_msg(str(qload0))

c = get_load_dat(1,"1",error)
psat_msg(str(c.cp[0]))
psat_msg(str(c.cp[1]))
psat_msg(str(c.cp[2]))
psat_msg(str(c.cp[3]))

# psat_command(r'CloseProject',error)