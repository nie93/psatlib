# psatlib

## Descriptions

`psatlib` is an imported library designed for PSAT running with Python scripts. This module has been developed and tested under Python 2.7 and Python 3.4 environment supported by PSAT.

## How To Use It (from Command Line Interface)

1. Add PSAT's bin directory (`C:\DSATools_18-SL\Psat\bin`) to `PATH` in the system environment variables in order to call `PSAT` directly using CLI.

2. Copy the folder of `psatlib` to your PSAT's python UserScripts directory (e.g. `C:\DSATools_18-SL\Psat\bin\python\UserScripts`).

3. Run Windows command line interface (`cmd.exe`), change directory (`cd`) to the Python script folder you used, then run `psat.exe` with specified `*.py` script and command line option `python` with the following command:

```sh
PSAT main_write_ctg_to_xml.py python
```


## Development Guide

* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
* [PEP-8](https://www.python.org/dev/peps/pep-0008/)
* Importing external packages (e.g. NumPy) is **NOT** recommended except for better computing performance. You may import external packages in your own scripts.

## Known Problems

### PSAT Powerflow Solution Limit

PSAT limits 3,224 powerflow solving commands within each batch.

***Solution***: Use multiple Windows batch files to execute different Python scripts in parallel. Maximum number of sessions on each workstation is 5.

### VSAT GUI Display Limit

VSAT GUI limits 2,476 scenarios in display.

***Solution***: Use `vsat_batch` for running with a large amount of scenarios.


### Problem with Python Environment

PSAT GUI returns fatal RunTime Error or could not open `psatPythonXX.dll` if Python is installed by 64-bit MSI installer.

Tested problem environment:

* Python 2.7.15 (v2.7.15:ca079a3ea3, Apr 30 2018, 16:30:26) [MSC v.1500 64 bit (AMD64)] on win32

***Solution***: Re-install Python with

* [Python 2.7.15 Windows x86 MSI installer](https://www.python.org/ftp/python/2.7.15/python-2.7.15.msi) 
* [Python 3.4.4 Windows x86 MSI installer](https://www.python.org/ftp/python/3.4.4/python-3.4.4.msi)

instead of Windows x86-64 MSI installer, despite that your OS is installed as 64-bit system.

Known feasible environments:

* Python 2.7.9  (default, Dec 10 2014, 12:24:55) [MSC v.1500 32 bit (Intel)] on win32
* Python 2.7.13 (v2.7.13:a0645b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)] on win32
* Python 2.7.15 (v2.7.15:ca079a3ea3, Apr 30 2018, 16:22:17) [MSC v.1500 32 bit (Intel)] on win32
* Python 3.4.4  (v3.4.4:737efcadf5a6, Dec 20 2015, 19:28:18) [MSC v.1600 32 bit (Intel)] on win32
