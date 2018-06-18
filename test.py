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

busnum = get_busnum(ctype.bs)
load0 = get_loads(busnum)

psat_msg('      Number of Buses: %3d' %num_of_buses)
psat_msg('      Number of Loads: %3d' %num_of_loads)
psat_msg('      Number of Areas: %3d' %num_of_areas)
psat_msg(' Number of Generators: %3d' %num_of_gens)

psat_msg('[BUSNUM, PLOAD, QLOAD]')
l = [busnum, load0['p'], load0['q']]
l = map(list, zip(*l))
disp_list(l)

test_busnum = [1, 2]
gen_idobj = get_comp_id(ctype.gen, test_busnum)
load_idobj = get_comp_id(ctype.ld, test_busnum)
bus_idobj = get_comp_id(ctype.bus, test_busnum)
fxtr_idobj = get_comp_id(ctype.fxtr, test_busnum)
line_idobj = get_comp_id(ctype.ln, test_busnum)

psat_msg(' Length of GEN_IDOBJ: %3d' %len(gen_idobj))
psat_msg('Length of LOAD_IDOBJ: %3d' %len(load_idobj))
psat_msg('Length of LINE_IDOBJ: %3d' %len(line_idobj))
psat_msg(' Length of BUS_IDOBJ: %3d' %len(bus_idobj))

load_compobj = get_comp_dat(load_idobj)

psat_msg(str(type(load_compobj[0])))

# psat_command(r'CloseProject',error)