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

## Data info
In the example folder is located an example script on using the PImGED package and its modules. 
The data folder contain 20 datasets obtained in the GASMIX test setup along with 20 pressure 
measurments. ####### **OBS** ####### The data folder is 11 GB of data, as it consist of 
uncompressed tiff files directly from the high-speed camera sensor used.