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
## Installation
---

## 🚀 Features

- GUI for computing fault-based Seismic Activity Rates (SAR)
- Integration with [OpenQuake](https://github.com/gem/oq-engine) for hazard calculations
- GMT visualization of hazard maps
- Modular design suitable for extensions
- Optional support for PyGMT, GDAL, and Fiona
- GUI built with PyQt5
---

## 🛠 Installation Instructions

You can install FQSHA in two ways:

---

## 🚀 Running  FQSHA on Linux

This guide helps install FQSHA and its dependencies across platforms. **Python 3.10 or higher is required**.

---

# Clone the repository
```
conda create -n fqsha python=3.10
conda activate fqsha
git clone https://github.com/GeoSignalAnalysis/fqsha.git
cd fqsha  # You should be in the directory of the downloaded folder for the installation.
```

### ✅ 1. Core Installation

Install the main package using pip:

```bash
pip install .
```

---

### ⚠️ 2. NumPy Compatibility Warning

> **IMPORTANT:** You must use `numpy==1.24.4`  
> This version is required for compatibility with OpenQuake and GDAL.  
> Newer versions (e.g., 2.x) are **not compatible** and may cause runtime errors.

Check your version:

```bash
python -c "import numpy; print(numpy.__version__)"
```

If the version is not `1.24.4`, run:

```bash
pip uninstall numpy
pip install numpy==1.24.4
```

---

### 🔁 3. Optional Features

#### 🗺️ PyGMT for Mapping

Enable GMT-based visualization using PyGMT:

```bash
pip install .[gmt]
```

---

#### 🧪 Development and Testing

Install tools for unit testing and coverage:

```bash
pip install .[dev]
```

---

### 🧭 4. GDAL and Fiona (Required for GIS and Shapefiles)

> ⚠️ On **Linux/Ubuntu**, do **not** install GDAL via pip. It may fail to build native dependencies.  
> Always use **Conda** to install GDAL and Fiona:

```bash
conda install -c conda-forge 'gdal>=3.6,<3.9' fiona sqlite
```

---

### 🌍 5. Install GMT for PyGMT

If using PyGMT, install GMT version 6 using Conda:

```bash
conda install -c conda-forge gmt=6
```

> On Linux, PyGMT may not find the GMT library automatically. Set this environment variable if needed:

```bash
export GMT_LIBRARY_PATH=$(gmt --show-libdir)
```

---

## ✅ Summary Table

| Component        | How to Install                                      |
|------------------|-----------------------------------------------------|
| Core             | `pip install .`                                     |
| NumPy (required) | `pip install numpy==1.24.4`                         |
| PyGMT support    | `pip install .[gmt]` + `conda install gmt=6`        |
| GDAL/Fiona       | `conda install -c conda-forge gdal fiona sqlite`    |
| Development      | `pip install .[dev]`                                |

---

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

## 📧 Contact

For bug reports or feature requests, please open an issue on [GitHub](https://github.com/GeoSignalAnalysis/fqsha).

Lead Developers:
- Nasrin Tavakolizadeh (n.tavakolizadeh@ubi.pt)
- Hamzeh Mohammadigheymasi
- Nuno Pombo

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


```


## Contact information 
Copyright(C) 2023 Nasrin Tavakolizadeh 
Author: Nasrin Tavakolizadeh (n.tavakolizadeh@ubi.pt), Hamzeh Mohammadigheymasi (hamzeh@ubi.pt)


