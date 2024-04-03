![logo](https://i.ibb.co/5rdDr7p/header.png)

Python Image library for GASMIX EUDP Distro (PImGED) is used for handling image data collected 
during the experiments of the GASMIX project supported by EUDP, MAN ES and DTU. 

The framework is designed to handle large amounts of image data with limited computational 
resources. Several optimized function utilizing OpenCV C++, numba compilation and multithreading 
through the Joblib package, are used to speed-up computations and memory handling.

## [code pages are found here](https://benhartz.github.io/pimged-pages/)

## Before use
Intall the test code by using the following method
```
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple PImGed
```

## Example scripts and data
Get the example scripts from the [GitHub repository](https://github.com/benhartz/pimged-example), 
it is cloned by using the following command
```commandline
git clone https://github.com/benhartz/pimged-example.git
``` 


### [Download the example data from this figshare link](https://figshare.com/s/286bc4cf871abd25b1d1)


**-- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS --** 

The data folder is ~6 GB of data, as it consist of  uncompressed tiff files directly from the 
high-speed camera sensor used.

**-- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS -- -- OBS --  -- OBS --** 

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

Now it should be possible to run the `pimged_example.py` script for testing simple data 
manangement and get these plots out
![jet conc](https://i.ibb.co/dGX7NMC/jetconc.png)
![jet staistics](https://i.ibb.co/sQFtL2D/jetstatistics.png)
![Pressures](https://i.ibb.co/zQ2xTgh/pressure.png)

The `pimged_big_data_example.py` script show how to use the code for handling larger amounts of 
data to get concentrations fields

To use the POD calculation module, run `pimged_pod_example.py` for an example on use