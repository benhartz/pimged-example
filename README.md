![logo](https://i.ibb.co/5rdDr7p/header.png)

Python Image library for GASMIX EUDP Distro (PImGED) is used for handling image data collected 
during the experiments of the GASMIX project supported by EUDP, MAN ES and DTU. 

The framework is designed to handle large amounts of image data with limited computational 
resources. Several optimized function utilizing OpenCV C++, numba compilation and multithreading 
through the Joblib package, are used to speed-up computations and memory handling.

## [code pages are found here](https://benhartz.github.io/pimged-pages/)

## Installation
A test package is created for the project, and it is possible to install it, with dependencies 
from testPyPi using the following command in the terminal for a Windows machine:
```
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple PImGed
```

## Example scripts and data

### Get example scripts
Get the example scripts from the [GitHub repository](https://github.com/benhartz/pimged-example), it is cloned by using the following command
```commandline
git clone https://github.com/benhartz/pimged-example.git
``` 


### [Download the example data from this figshare link](https://figshare.com/s/286bc4cf871abd25b1d1)


**-- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS --** 

The data folder is ~6 GB of data, as it consist of  uncompressed tiff files directly from the 
high-speed camera sensor used.

**-- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS --** 

### Folder setup
In the example folder is located an example script on using the PImGED package and its modules. 
The data folder contain 10 datasets obtained in the GASMIX test setup along with 10 pressure 
measurments in a ziped folder for speed-up of downloading instead of many small image files.

Unzip the data folder so the folder path looks as seen here

```
pimged-example/
  .gitignore
  LICENSE
  README.md
  example/
    pimged_example.py
    pimged_big_data_example.py
    pimged_pod_example.py
  data/
    data/
     Pressure/
      ...
     Pictures/
      ...
```
The working directory should be set inside the example folder, with the scripts.

### Example results
#### pimged_example.py
Now it should be possible to run the `pimged_example.py` script for testing simple data 
manangement and get these plots out. AVO translate to "After Valve Opening" and there is a delay 
due to the air has to travel through the jet, valve opening delay and delay in the relays 
sending the opening signal. 
![jet conc](https://i.ibb.co/dGX7NMC/jetconc.png)
![jet staistics](https://i.ibb.co/sQFtL2D/jetstatistics.png)
![Pressures](https://i.ibb.co/zQ2xTgh/pressure.png)

#### pimged_big_data_example.py
The `pimged_big_data_example.py` script show how to use the code for handling larger amounts of 
data to get concentrations fields. 

**-- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS --** 

Running `pimged_big_data_example.py` stores ~8.7 GB of data on the hard drive

**-- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS --** 

The big data example should produce this plot
![Big data example](https://i.ibb.co/Ss9tr1D/bigdata.png)


#### pimged_pod_example.py
To use the POD calculation module, run `pimged_pod_example.py` for an example on use. This 
example script takes some time to run, as it is an extensive algorithm. 

**-- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS --** 

Running `pimged_pod_example.py` stores ~5.5 GB of data on the hard drive

**-- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS --** 

The following plot should be produced
![POD mode](https://i.ibb.co/qDVCn6X/phase-POD-mode-1.png)

---

## Support
The code is maintained during the GASMIX project from 2022 till start of 2025 by Benjamin Hartz

After project end there are no plans for further support of the code from main authors. 


## Authors and acknowledgment
Created by Benjamin Hartz

Created during the GASMIX PhD project at DTU Construct under FVM, supported by EUPD and MAN ES 

## License
[BSD 3-Clause License](LICENSE)

Copyright (c) 2024, Benjamin Arnold Krekeler Hartz

---