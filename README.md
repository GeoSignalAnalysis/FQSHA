#  FQSHA: An open-source software for Fault-Based Seismic Hazard Assessment

![FQSHA](https://github.com/GeoSignalAnalysis/FQSHA/blob/main/logo-1.png)

# The main architucture of the software:

![FQSHA](https://github.com/GeoSignalAnalysis/FQSHA/blob/main/Software_architecture.png)


This software combines the algorithm introduced by FaultQuake and the Open Quake engine to calculate the fault's seismic hazard.


# FaultQuake workflow

![FaultQuake](https://github.com/GeoSignalAnalysis/FaultQuake/blob/main/FaultQuake_workflow.png)


FQSHA is primarily developed and tested on Debian-based Linux OS systems. Therefore, we suggest using FQSHA in such environments for the best experience. While it's possible to use FQSHA on Windows and macOS, there may be challenges during compiling and running the workflow due to potential compatibility issues.

We greatly value community contributions and are steadfastly committed to continuously addressing and resolving any bugs that arise in the repository. Should you encounter any issues, please don't hesitate to contact us.


## Installation

### Create and activate a clean Conda environment – conda (for full environment including GDAL and PyQt)

```bash
conda create -n FQSHA python=3.10 -c conda-forge
conda activate FQSHA
```

##  Install geospatial dependencies via conda (critical):

```bash
conda install -c conda-forge gdal fiona pyproj pygmt pyqt

```


## Install OpenQuake from GEM’s GitHub source:


```bash
git clone https://github.com/gem/oq-engine.git
cd oq-engine
pip install .
cd ..
```


# After creating the environment and installing the necessary packages run this:

```bash
cd ../FQSHA  # Or your actual directory
pip install .[gdal,gmt,dev]

```



## How to run FQSHA 

```bash
python -m fqsha

```



## Usage 

Read documentation for more guidance on installation and running the software.



# Running the test codes by:

```bash
coverage erase
PYTHONPATH=. coverage run --include="tests/test_sactivityrate_xmlExport.py" -m pytest tests/test_sactivityrate_xmlExport.py
coverage report -m

coverage erase
PYTHONPATH=. coverage run -m pytest tests/test_gui.py
coverage report
```

## To cite: 


BibTex:
```


```

## License

This software is licensed under the GNU Affero General Public License v3.0.  
© 2025 Nasrin Tavakolizadeh and Hamzeh Mohammadigheymasi.  
See the [LICENSE](./LICENSE) file for full details.


## Contributing
If you would like to contribute to the project or have any suggestions about the code, please feel free to create Pull Requests, raise issues and contact me. 
If you have any questions about the usage of this package or find bugs in the code, please also feel free to contact me.

## Contact information 
Copyright(C) 2023 Nasrin Tavakolizadeh 
Author: Nasrin Tavakolizadeh (n.tavakolizadeh@ubi.pt), Hamzeh Mohammadigheymasi (hamzeh@ubi.pt)


