#  FQSHA: An open-source software for Fault-Based Seismic Hazard Assessment

**FQSHA** (Fault-based Quantitative Seismic Hazard Assessment) is an open-source Python software package designed to streamline fault-based PSHA (Probabilistic Seismic Hazard Assessment). It features a GUI and integrates tightly with the OpenQuake engine and GMT for modeling and visualization.

![FQSHA](https://github.com/GeoSignalAnalysis/FQSHA/blob/main/logo-1.png)

# The main architucture of the software:

![FQSHA](https://github.com/GeoSignalAnalysis/FQSHA/blob/main/Software_architecture.png)


This software combines the algorithm introduced by FaultQuake and the Open Quake engine to calculate the fault's seismic hazard.


# FaultQuake workflow

![FaultQuake](https://github.com/GeoSignalAnalysis/FaultQuake/blob/main/FaultQuake_workflow.png)


FQSHA is primarily developed and tested on Debian-based Linux OS systems. Therefore, we suggest using FQSHA in such environments for the best experience. While it's possible to use FQSHA on Windows and macOS, there may be challenges during compiling and running the workflow due to potential compatibility issues.

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

## 🛠️ Installation Guide

You can install FQSHA in two ways:

---

### ⚙️ Option 1: Install as a Standalone Python Package (with `pip`)

Recommended if you're **just using the GUI** or integrating it into Python scripts.

```bash
# Clone the repository
git clone https://github.com/yourusername/fqsha.git
cd fqsha

# Install with core dependencies
pip install .

# To include optional dependencies:
pip install .[gmt]     # for PyGMT support
pip install .[gdal]    # for GDAL/Fiona support
pip install .[dev]     # for testing and development
```

---

### 💻 Option 2: Set Up with Conda

If you want to run/debug it in **IDE**, this is recommended.

#### Step-by-step:

```bash
# Clone the repository
git clone https://github.com/yourusername/fqsha.git
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


