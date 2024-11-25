![logo](https://i.ibb.co/5rdDr7p/header.png)

Python Image library for GASMIX EUDP Distro (PImGED) is used for handling image data collected 
during the experiments of the GASMIX project supported by EUDP, MAN ES and DTU. 

The framework is designed to handle large amounts of image data with limited computational 
resources. Several optimized function utilizing OpenCV C++, numba compilation and multithreading 
through the Joblib package, are used to speed-up computations and memory handling.

GASMIX experiments consist of inverse seeded jet flows, where the environment is seeded and use 
a jet of clean air for negative image. From the negative image a concentration is estimated 
based on initial images before seeding and fully seeded. The PimGED package was designed to 
handle these images on local computers with data on physical external harddrives.

---

> **For more information, see the code pages --> [found here](https://benhartz.github.io/pimged-pages/) <--**

---

## Installation
A test package is created for the project, and it is possible to install it, with dependencies 
from testPyPi using the following command in the terminal for a Windows machine:
```
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple PImGed
```
---
## Example tutorial scripts and data
There are two ways to get the example scripts. Clone this repo and set the working directory 
inside the example folder. Further, external data is needed to use the examples
### Download the example data from this --> [figshare link](https://figshare.com/s/286bc4cf871abd25b1d1) <--
> **-- OBS -- -- OBS -- -- OBS --**
> 
> The data folder is ~6 GB of data, as it consist of uncompressed tiff files directly from the 
> high-speed camera sensor used.

---
### Extracted folder setup
In the example folder is located an example script on using the PImGED package and its modules. 
The data folder contain 10 datasets obtained in the GASMIX test setup along with 10 pressure 
measurments in a ziped folder for speed-up of downloading instead of many small image files.

Unzip the data folder so the folder path looks as seen here, and the `working directory`
should be set inside the example folder, with the scripts.

```
pimged-example/
|   .gitignore
|   LICENSE
|   README.md
|
|-- example/
|       pimged_example.py
|       pimged_big_data_example.py
|       pimged_pod_example.py
|
`-- data/
    `-- data/
        `-- Pressure/
        |     ...
        `-- Pictures/
              ...
```
---

### Example results
All examples are designed so they should be able to run on most computeres of todays standard 
with 16 GB of RAM. If less RAM is installed in the computer, there could be issues with running the 
examples

#### pimged_example.py

>Now it should be possible to run the `pimged_example.py` script for testing simple data 
manangement and get these plots out. AVO translate to "After Valve Opening" and there is a delay 
due to the air has to travel through the jet, valve opening delay and delay in the relays 
sending the opening signal.
> 
><img src="https://i.ibb.co/DLsWmqR/jetconc.png" alt="drawing" width="800"/>
><img src="https://i.ibb.co/34msz0d/jetstatistics.png" alt="drawing" width="800"/>
><img src="https://i.ibb.co/zQ2xTgh/pressure.png" alt="drawing" width="500"/>

#### pimged_big_data_example.py
> The `pimged_big_data_example.py` script show how to use the code for handling larger amounts 
> of data to get concentrations fields.  
> 
> **Running `pimged_big_data_example.py` stores ~8.7 GB of data on the hard drive**
> 
> The big data example should produce this plot
> 
> <img src="https://i.ibb.co/mB6c003/bigdata.png" alt="drawing" width="800"/>



#### pimged_pod_example.py
> To use the POD calculation module, run `pimged_pod_example.py` for an example on use. This 
example script takes some time to run, as it is an extensive algorithm.
> 
> **Running `pimged_pod_example.py` stores ~5.5 GB of data on the hard drive**
> 
> The following plot should be produced
> 
> <img src="https://i.ibb.co/YDfFQPJ/phase-POD-mode-1.png" alt="drawing" width="500"/>


---

## Code structure
![codestructure](https://i.ibb.co/VDNfd9X/code-structure.png)


To handle larger data amounts the code takes inspiration from Panda on datastructure and 
implement a dataset module used for loading/saving data. The data is handled by datacontainers 
with functions for manipulating the individual datatypes. With the datacontainer module implementing
versatile classes for image and pressure datahandling, with common internal functions, it is 
possible to reduce code repetition and adding datacontainers to the module. The metadata from 
data is handled and stored for the individual dataset in the same datacontainer for and sent around 
with the data. The dataset module object is then used as an input for other modules that can use 
the standardrised data setup.
 
Handling standard calculations a calculation module takes the dataset object as an input. 
When new information is calculated it can then populate the dataset object with information, 
utilizing the indirection implementation of list and numpy arrays in python. This streamline the 
collection of data in one object that can load or save the data with minimal coding.

Between the whole framework, several functions are reused with simple coding and these are 
included in a utility package with the framework. Here is sorting of list elements widely used 
in folder and filenames, checking folder paths, handling metadata etc. 

Splitting the code framework into specialized modules decouple functionality and makes it 
easy to update individual functionality in different modules, without breaking code coherence.

---
## Improvements
A re-write of the calculation module could improve useability with a design similar to that of 
the POD module. The re-design would provide more flexibility and robustness of the code. And the 
"jetparameters" module could be updated for the new code structure and made funcitioning again.

## Future work
The package design makes it possible to implement new modules and functionalities fast. The POD 
module only consist of a Phase POD rutine, but implementing a static POD or SPOD method could 
improve useability. 

## Peer review
There have been no feedback that is implemented in the code. All ideas in improvements is based on 
learnings over coding the framework and learning to handle large datasets. 

## Tests
The test setup is only done on some functions of the utils.utils module to show it is possible, 
as full writing unittest for all functions and functionality of the PImGED package is a 3 month 
project that is not time for. Further projects should include a unit test framework from the 
start for reducing the workload over time and code updates checking.

---
## Support
The code is maintained during the GASMIX project from 2022 till start of 2025 by Benjamin Hartz

After project end there are no plans for further support of the code from main authors. 

---

## Authors and acknowledgment
Created by Benjamin Hartz

Created during the GASMIX PhD project at DTU Construct under FVM, supported by EUPD and MAN ES 

---

## License
[BSD 3-Clause License](LICENSE)

Copyright (c) 2024, Benjamin Arnold Krekeler Hartz

---