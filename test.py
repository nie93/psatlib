from psat_python import *
from UserScripts.psatlib import *
from UserScripts.psatlib.area import *
from UserScripts.psatlib.bus import *
from UserScripts.psatlib.generator import *
from UserScripts.psatlib.io import *
from UserScripts.psatlib.line import *
from UserScripts.psatlib.load import *
from UserScripts.psatlib.system import *


disable_engine_messages(True)
error = psat_error()

def disp_system_basics():
    psat_msg('=================== SYSTEM =====================')
    psat_msg('     BUSNUM: %s' %str(busnum))
    psat_msg(' LOADBUSNUM: %s' %str(loadbusnum))
    psat_msg('  GENBUSNUM: %s' %str(genbusnum))
    psat_msg('         PD: %s' %str(pload))
    psat_msg('         QD: %s' %str(qload))
    psat_msg('================================================')
    psat_msg('      Number of Buses: %3d' %num_of_buses)
    psat_msg('      Number of Loads: %3d' %num_of_loads)
    psat_msg('      Number of Areas: %3d' %num_of_areas)
    psat_msg(' Number of Generators: %3d' %num_of_gens)
    psat_msg('================================================')
    psat_msg('--------------------- BUS ----------------------')
    psat_msg('    BUSTYPE: 1: load bus, 2: gen bus, 3: swing bus, 4: out of service bus')
    psat_msg('[BUSNUM, TYPE, VM, VA, VREAL, VIMAG]')
    disp_list([busnum, bustype, vm, va, vreal, vimag],1)
    psat_msg('--------------------- GEN ----------------------')
    psat_msg('[BUSNUM, PGEN, QGEN]')
    disp_list([genbusnum, pgen, qgen],1)
    psat_msg('--------------------- LOAD ---------------------')
    psat_msg('[BUSNUM, PLOAD, QLOAD]')
    disp_list([loadbusnum, pload, qload],1)
    psat_msg('------------------------------------------------')
    psat_msg('sumPD:%8.2f MW, sumQD:%8.2f MVAr' %(sum(pload), sum(qload)))
    psat_msg('------------------------------------------------')


casefile_path = r'C:\\DSATools_18-SL\\Psat\\samples'
casefile_name = r'test'
psat_command('OpenPowerflow:"%s\\%s.pfb"' %(casefile_path, casefile_name), error)
solve_if_not_solved()

num_of_buses = get_count_comp(ctype.bs,error)
num_of_loads = get_count_comp(ctype.ld,error)
num_of_areas = get_count_comp(ctype.ar,error)
num_of_gens = get_count_comp(ctype.gen,error)

# sorted_busnum = get_busnum(ctype.bus)
busnum = get_bus_prop('mainsub', 'NUMBER')
bustype = get_bus_prop('mainsub', 'TYPE')
vm = get_bus_prop('mainsub', 'VM')
va = get_bus_prop('mainsub', 'VA')
vreal = get_bus_prop('mainsub', 'VREAL')
vimag = get_bus_prop('mainsub', 'VIMAG')

loadbusnum = get_load_prop('mainsub', 'BUS')
pload = get_load_prop('mainsub', 'PD')
qload = get_load_prop('mainsub', 'QD')

genbusnum = get_gen_prop('mainsub', 'BUS')
pgen = get_gen_prop('mainsub', 'PG')
qgen = get_gen_prop('mainsub', 'QG')

disp_system_basics()

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

# region [Defines Contingencies and export as XML files]
linectg = define_line_ctg('mainsub')
disp_list(linectg)
ctg2xml(casefile_path + r'\\output\\contingencies.xml', linectg)
# endregion

psat_command('SaveMessagesToFile:"%s\\psat_msg.txt"' %casefile_path, error)
psat_command(r'CloseProject',error)