# psatlib

## Descriptions
`psatlib` is an imported library designed for PSAT running with Python scripts.


## How To Use It (Command Line Interface)
1. Copy the whole folder of `psatlib` to your PSAT's python userscripts directory (e.g. `C:\DSATools_18-SL\Psat\bin\python\UserScripts`).

2. Open command window (`cmd.exe`), change directory to the Python script folder you used, then type in

```
PSAT test.py python
```


## Development Guide
* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
* [PEP-8](https://www.python.org/dev/peps/pep-0008/)
* Importing external packages (e.g. NumPy) is **NOT** recommended except for better computing performance. You may import external packages in your own scripts.


## List of Functions
* get_busnum(ctype)

## Known Bugs

### Problem with Python 2.7.x Environment
PSAT GUI returns RunTime Error or could not open `psatPython27.dll` if Python 2.7 is installed by 64-bit MSI installer.

Tested environment:
* Python 2.7.15 (v2.7.15:ca079a3ea3, Apr 30 2018, 16:30:26) [MSC v.1500 64 bit (AMD64)] on win32 

#### Solution
Re-install Python 2.7.x with Python's [Windows x86 MSI installer](https://www.python.org/ftp/python/2.7.15/python-2.7.15.msi) instead of Windows x86-64 MSI installer, despite that your OS is installed as 64-bit system.

Known feasible environments:
* Python 2.7.9 (default, Dec 10 2014, 12:24:55) [MSC v.1500 32 bit (Intel)] on win32 
* Python 2.7.13 (v2.7.13:a0645b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)] on win32 
* Python 2.7.15 (v2.7.15:ca079a3ea3, Apr 30 2018, 16:22:17) [MSC v.1500 32 bit (Intel)] on win32 
