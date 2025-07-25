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

---

# 🛠️ Installation Guide:

You can install FQSHA in two ways:

---

## ⚙️ Linux installation: Installing on a Conda env:
Recommended if you're **just using the GUI** or integrating it into Python scripts.
```bash
# Clone the repository
conda create -n fqsha python=3.10
conda activate fqsha
git clone https://github.com/GeoSignalAnalysis/fqsha.git
cd fqsha
# Install with core dependencies
pip install .
# To include optional dependencies:
pip install .[gmt]     # for PyGMT support
conda install -c conda-forge gdal
pip install .[gdal]    # for GDAL/Fiona support
pip install .[dev]     # for testing and development
pip install fiona
conda install -c conda-forge gmt=6

# double check the numpy version if it is not equal to 1.24.04, downgrade numpy:
python -c "import numpy; print(numpy.__version__)"
pip uninstall numpy
pip install numpy==1.24.04
```

## 🚀 Running  FQSHA on Linux
### GUI Launch

```bash
python fqshaL/FQSHA.py
```

### Run from PyCharm
In an IDE of your choice, right-click `FQSHA.py` > Run.

---

---
## 🛠️ FQSHA Installation Guide (Windows 11)

This guide outlines the full setup of the FQSHA toolkit on Windows 11, including GMT, Ghostscript, and the Python environment with PyGMT and OpenQuake dependencies.

---

## ✅ 1. Install GMT (Generic Mapping Tools)

1. **Uninstall** any existing GMT 5.x installation if present.
2. Download GMT 6.x from the official website:  
   https://www.generic-mapping-tools.org/download/
3. Run the installer and install GMT to:  
   `C:\Program Files\GMT6\`
4. During installation, make sure to **check** the option to  
   **"Add GMT to the system PATH"**.

---

## ✅ 2. Install Ghostscript

1. Download the latest 64-bit Ghostscript for Windows from:  
   https://ghostscript.com/download/gsdnld.html
2. Install it to the default directory:  
   `C:\Program Files\gs\gs10.06.0\`
3. Add the following to your system `PATH` environment variable:  
   `C:\Program Files\gs\gs10.06.0\bin`

---

## ✅ 3. Configure Environment Variable for GMT (if needed)

If PyGMT cannot locate GMT automatically, manually set the following environment variable:

- **Variable name:** `GMT_LIBRARY_PATH`  
- **Value:** `C:\Program Files\GMT6\bin`

---

## ✅ 4. Clone and Navigate to the FQSHA Project

```bash
git clone https://github.com/yourusername/FQSHA.git
cd FQSHA



✅ 5. Set Up the Conda Environment


Option A: Reproduce full environment from .yml file
If you want to install using yml file (fqsha_windows_env.yml), run:

conda env create -f fqsha_windows_env.yml
conda activate fqsha_env


Option B: Manual setup: Without .yml file

conda create -n fqsha_env python=3.10
conda activate fqsha_env
conda install -c conda-forge pygmt openquake pandas
pip install -r requirements.txt


✅ 6. Run the FQSHA Toolkit

You must be inside the extracted package directory (fqsha/). Then, run:


python -m fqsha


✅ 7. Verify Installation (Optional Test)

import pygmt
fig = pygmt.Figure()
fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
fig.show()



## 📝 Notes
These commands assume you're using Anaconda Prompt.

If you see ModuleNotFoundError, make sure you're inside the correct directory (fqsha/) and the environment is activated.

The environment has been tested on Windows 11, using:

Python 3.10

GMT 6.5+

Ghostscript 10.06

PyGMT 0.10


If you want to run/debug it in **IDE**, this is recommended.

#### Step-by-step:

```bash
# Clone the repository
conda create -n fqsha python=3.10
conda activate fqsha
git clone git clone https://github.com/GeoSignalAnalysis/fqsha.git
cd fqsha

# Create and activate Conda environment
conda env create -f environment.yml
conda activate fqsha
```

Then in **PyCharm or any IDE**:
1. Open the project directory.
2. Go to **Settings > Project > Python Interpreter**
3. Set the interpreter to: `conda environments, and select fqsha`
4. You can now run `FQSHA.py` as the entry point.

---

## 🚀 Running FQSHA

### GUI Launch

```bash
python fqsha/FQSHA.py
```

### Run from PyCharm
In an IDE of your choice, right-click `FQSHA.py` > Run.

---

## 🧪 Development & Testing

```bash
coverage erase
PYTHONPATH=. coverage run --include="tests/test_sactivityrate_xmlExport.py" -m pytest tests/test_sactivityrate_xmlExport.py
coverage report -m

coverage erase
PYTHONPATH=. coverage run -m pytest tests/test_gui.py
coverage report
```


## 📂 Project Structure

```
FQSHA/
├── FQSHA.py                # Main GUI script
├── FQSHA_Functions.py      # Core logic
├── OpenQuake_input_generator.py
├── SeismicActivityRate.py
├── Mapping.py
├── input_data/             # Input files
├── output_files/           # Output folders
└── tests/                  # Test scripts
```

---


## 🛠️ Installation Guide in Windows
Follow the guidance in FQSHA_InstallationGuide_Windows.txt

The requirements are included in the fsha_windows_env.yml


## 👥 Authors

- **Nasrin Tavakolizadeh** — [n.tavakolizadeh@ubi.pt](mailto:n.tavakolizadeh@ubi.pt)
- **Hamzeh Mohammadigheymasi**

---

## 📄 License

FQSHA is distributed under the [AGPL-3.0-or-later](https://www.gnu.org/licenses/agpl-3.0.html) license.

---

## 📈 Future Enhancements

- Advanced SAR models
- Extended OpenQuake capabilities
- Validation using GEM datasets
- National-scale hazard integration


## Usage 

Read documentation for more guidance on installation and running the software.


## To cite: 


BibTex:
```


```


## Contact information 
Copyright(C) 2023 Nasrin Tavakolizadeh 
Author: Nasrin Tavakolizadeh (n.tavakolizadeh@ubi.pt), Hamzeh Mohammadigheymasi (hamzeh@ubi.pt)


