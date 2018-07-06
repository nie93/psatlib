""" VSAT's IO functions management."""

__author__ = "Zhijie Nie"

import os
import fnmatch


# Writes VSADAT Files for Batch Run
def write_vsadat(filename, filepath):
    with open('%s\\%s' %(filepath, filename), 'wb') as f:        
        for name in os.listdir(filepath):
            if fnmatch.fnmatch(name, '*.snr'):
                f.write('1\n')
                f.write(name.replace('.snr', '') + '\n')
                f.write('%s\n' %name)
    f.close()
    return       

# Writes Scenario Files
def write_snr(filepath, prmprefix):
    for name in os.listdir(filepath):
        if fnmatch.fnmatch(name, '*.pfb'):
            name = name.replace('.pfb', '')
            with open(filepath + '\\%s.snr' %name, 'wb') as f:
                f.write("[VSAT 5.x Scenario]\n")
                f.write("{Description}\n")
                f.write("  %s\n" %name)
                f.write("{End Description}\n\n")
                f.write("PFB File = '%s.pfb'\n" %name)
                f.write("Parameter File = '%s.prm'\n" %prmprefix)
                f.write("Transfer File = '%s.trf'\n" %prmprefix)
                f.write("Contingency File = '%s.ctg'\n" %prmprefix)
                f.write("[End]")
                f.close()
    return

    # [VSAT 5.x Scenario]
    # {Description}
    #    IEEE_39_bus_mod_notsolved_001
    # {End Description}

    # PFB File = 'IEEE_39_bus_mod_notsolved_001.pfb'
    # Parameter File = 'IEEE_39_bus.prm'
    # Transfer File = 'IEEE_39_bus.trf'
    # Criteria File = 'IEEE_39_bus.crt'
    # Contingency File = 'IEEE_39_bus.ctg'
    # [End]


# Writes Contengency Files
def write_ctg(filename, ctg):
    with open(filename, 'wb') as f:
        f.write("[VSAT 5.0 CONTINGENCY]\n")
        for i in range(len(ctg)):
            f.write("\n{Contingency Must Run}\n")
            f.write("  Contingency name = '%s_Tripped_%d_%d_%s'\n" \
                    %(ctg[i][0], ctg[i][1], ctg[i][2], ctg[i][3]))
            f.write("  Outage Branch = %d  %d '%s'\n" \
                    %(ctg[i][1], ctg[i][2], ctg[i][3]))
            f.write("{End contingency}\n")
        f.write("\n[END]\n")
    f.close()
    return

    # [VSAT 5.0 CONTINGENCY]

    # {Contingency Must Run}
    #   Contingency name = 'LINE_TRIP_27_53'
    #   Outage Branch = 27  53 '1'
    # {End contingency}
    
    # {Contingency Must Run}
    #   Contingency name = 'LINE_TRIP_33_38'
    #   Outage Branch = 33  38 '1'
    # {End contingency}
    
    # {Contingency Must Run}
    #   Contingency name = 'LINE_TRIP_52_55'
    #   Outage Branch = 52  55 '1'
    # {End contingency}
    
    # [END]