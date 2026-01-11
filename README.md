#  FQSHA: An open-source software for Fault-Based Seismic Hazard Assessment
**FQSHA** (Fault-based Quantitative Seismic Hazard Assessment) is an open-source Python software package designed to streamline fault-based PSHA (Probabilistic Seismic Hazard Assessment). It features a GUI and integrates tightly with the OpenQuake engine and GMT for modeling and visualization.
![FQSHA](https://github.com/GeoSignalAnalysis/FQSHA/blob/main/logo-1.png)

# The main architucture of the software:

![FQSHA](https://github.com/GeoSignalAnalysis/FQSHA/blob/main/Software_architecture.png)

This software combines the algorithm introduced by FaultQuake and the Open Quake engine to calculate the fault's seismic hazard.

# FaultQuake workflow

![FaultQuake](https://github.com/GeoSignalAnalysis/FaultQuake/blob/main/FaultQuake_workflow.png)


FQSHA has been developed and tested both on Debian-based Linux OS systems and Windows 11. While it's possible to use FQSHA on macOS, there may be challenges during compiling and running the workflow due to potential compatibility issues.

We greatly value community contributions and are steadfastly committed to continuously addressing and resolving any bugs that arise in the repository. Should you encounter any issues, please don't hesitate to contact us.

## 🛠 Installation Instructions Linux (Ubuntu)

You can install FQSHA and all dependencies (including GDAL, GMT, and OpenQuake) in one step using Conda.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GeoSignalAnalysis/fqsha.git
   cd fqsha
   ```

2. **Create the Conda Environment**:
   ```bash
   conda env create -f environment.yml
   ```

3. **Activate the Environment**:
   ```bash
   conda activate fqsha
   ```

This will install:
- Core FQSHA package (in editable mode)
- OpenQuake Engine, PyGMT, GDAL, Fiona
- Compatible NumPy version
- All development and testing tools

---
---

## 6. To Run FQSHA in Ubuntu

```bash
python fqshaL/FQSHA.py
 
```

## 📂 Project Structure

```
fqsha/
├── fqsha/                    # Core source code
├── input_data/               # User inputs (fault data, config)
├── FQSHA_output/             # Auto-generated outputs (OpenQuake, maps)
├── tests/                    # Unit tests
├── FQSHA.py                  # GUI Launcher
├── README.md
├── pyproject.toml
```

---

## 📜 License

This project is licensed under the **AGPL-3.0-or-later** license. See the [LICENSE](./LICENSE) file for details.


## 📈 Future Enhancements

- Advanced SAR models
- Extended OpenQuake capabilities
- Validation using GEM datasets
- National-scale hazard integration


## 🛠️ Installation Guide in Windows
Follow the guidance in FQSHA_InstallationGuide_Windows.txt

The requirements are included in the fsha_windows_env.yml



## Usage 

Read documentation for more guidance on installation and running the software.


## To cite: 


BibTex:
```
@article{FQSHA2025,
title = {FQSHA: An open-source Python software for fault-based seismic hazard assessment},
journal = {SoftwareX},
volume = {32},
pages = {102339},
year = {2025},
issn = {2352-7110},
doi = {https://doi.org/10.1016/j.softx.2025.102339},
url = {https://www.sciencedirect.com/science/article/pii/S235271102500305X},
author = {Nasrin Tavakolizadeh and Hamzeh Mohammadigheymasi and Nuno Pombo},
}

```


## Contact information 
Copyright(C) 2023 Nasrin Tavakolizadeh 
Author: Nasrin Tavakolizadeh (n.tavakolizadeh@ubi.pt), Hamzeh Mohammadigheymasi (hamzeh@ubi.pt)


