#  FQSHA: An open-source software for Fault-Based Seismic Hazard Assessment

![FQSHA](https://github.com/GeoSignalAnalysis/FQSHA/blob/main/logo-1.png)

# The main architucture of the software:

![FQSHA](https://github.com/GeoSignalAnalysis/FQSHA/blob/main/Software_architecture.png)


This software combines the algorithm introduced by FaultQuake and the Open Quake engine to calculate the fault's seismic hazard.


# FaultQuake workflow

![FaultQuake](https://github.com/GeoSignalAnalysis/FaultQuake/blob/main/FaultQuake_workflow.png)


FQSHA is primarily developed and tested on Debian-based Linux OS systems. Therefore, we suggest using FQSHA in such environments for the best experience. While it's possible to use FQSHA on Windows and macOS, there may be challenges during compiling and running the workflow due to potential compatibility issues.

We greatly value community contributions and are steadfastly committed to continuously addressing and resolving any bugs that arise in the repository. Should you encounter any issues, please don't hesitate to contact us.

We implement the FQSHA workflow using a conda environment:

## Installation
The installation guides for these environments are provided below:

```bash
conda env create -f environment.yml
conda activate FQSHA
```

## If someone experiences slow environment creation, they can add:


```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
```




## How to run FQSHA 
```bash
conda activate FQSHA
python ./FQSHA.py

```


## Usage 

Read documentation for more guidance on installationa and running.
 

## To cite: 


BibTex:
```


```

## License 
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. For more details, see in the license file.

## Contributing
If you would like to contribute to the project or have any suggestions about the code, please feel free to create Pull Requests, raise issues and contact me. 
If you have any questions about the usage of this package or find bugs in the code, please also feel free to contact me.

## Contact information 
Copyright(C) 2023 Nasrin Tavakolizadeh 
Author: Nasrin Tavakolizadeh (n.tavakolizadeh@ubi.pt), Hamzeh Mohammadigheymasi (hamzeh@ubi.pt)


