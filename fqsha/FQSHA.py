# FQSHA - Fault-based Seismic Hazard Assessment Toolkit
# Copyright (C) 2025 Tavakolizadeh et al., (2025)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


"""
Created on October 2024

@authors: Nasrin Tavakolizadeh, Hamzeh Mohammadigheymasi
"""
# import self
from fontTools.merge import layout
from openquake.hazardlib.valid import mag_scale_rel

from .SeismicActivityRate import momentbudget, sactivityrate  # Import the function
from .FQSHA_Functions import export_faults_to_xml
from .OpenQuake_input_generator import gmpe_generate_xml
from .OpenQuake_input_generator import source_model_logic_tree
from .OpenQuake_input_generator import generate_job_ini
from .Mapping import create_contour_map_with_faults
import sys, argparse, json


from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets

import os
import subprocess
import glob
global faults

class FQSHAWindow(QtWidgets.QWidget):
    """
    GUI widget that displays a general description of the FQSHA software.

    This window presents basic information about the tool, its connection to OpenQuake,
    and its underlying methodology as described in Tavakolizadeh et al. (2024).
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information")
        self.setGeometry(100, 100, 600, 400)

        self.input_file_var = None
        self.faults = None

        layout = QtWidgets.QVBoxLayout()

        # Define info text as a formatted paragraph
        info_text = (
            "This software calculates fault hazard based on the methodology described in Tavakolizadeh et al., 2024, "
            "and the tool 'FaultQuake'. It directly connects to the OpenQuake engine for hazard assessment."
        )

        scroll_area = QtWidgets.QScrollArea()
        self.label = QtWidgets.QLabel(info_text)
        self.label.setWordWrap(True)

        scroll_area.setWidget(self.label)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)
        self.setLayout(layout)


class InfoWindow(QtWidgets.QWidget):
    """
    GUI widget that displays an example input fault file in JSON format.

    This window helps users understand the required input data structure and fields
    needed to run FQSHA properly.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information")
        self.setGeometry(100, 100, 600, 400)
        layout = QtWidgets.QVBoxLayout()
        info_text = """
        {
            {
    "ZFF": {
        "ScR": "WC94-R",
        "year_for_calculations": 2024,
        "Length": 109,
        "Dip": 40,
        "upperSeismoDepth": 5,
        "lowerSeismoDepth": 12,
        "SRmin": 1.36,
        "SRmax": 2.04,
        "Mobs": 6.4,
        "sdMobs": 0.05,
        "Last_eq_time": 1497,
        "SCC": 0.205,
        "ShearModulus": 3,
        "StrainDrop": 3,
        "Mmin": 5.5,
        "b-value": 0.9,
        "fault_rake": 90,
        "fault_trace": [
            [56.8364270795421, 27.3840232526968],
            [56.7842390191582, 27.3923258986669],
            [56.7237483128042, 27.3958841755113],
            [56.6525827759171, 27.3946980832298],
            [56.618186099755, 27.3935119909484],
            [56.6122556383477, 27.3935119909484],
            [56.5861616081558, 27.3792788835709],
          .
          .
          .
        ]
    },
    .
    .
    .
        }
        """
        scroll_area = QtWidgets.QScrollArea()
        self.label = QtWidgets.QLabel(info_text)
        self.label.setWordWrap(True)
        scroll_area.setWidget(self.label)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        self.setLayout(layout)



class Scale_Window(QtWidgets.QWidget):
    """
    GUI widget displaying supported magnitude scaling relationship codes.

    Explains the available options for the 'ScR' field in the input fault file,
    including relationships by Wells & Coppersmith, Leonard, and others.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information")
        self.setGeometry(100, 100, 600, 400)
        layout = QtWidgets.QVBoxLayout()

        info_text = """
        set ScR in the input file as follows:

        Wells and Coppersmith (1984) relationships:
        WC94-N - normal faults
        WC94-R - reverse faults
        WC94-S - strike slip faults
        WC94-A - all the kinematics

        Leonard (2010) relationships:
        Le10-D - dip slip faults
        Le10-S - strike slip faults
        Le10-SCR - stable continental regions

        Volcanic context relationships (Azzaro et al., 2015; Villamor et al.,
        2001):
        Volc - all the kinematics
        
        Please note that the magScaleRel parameter specified in the manual inputs is utilized for hazard assessment.        """

        scroll_area = QtWidgets.QScrollArea()
        self.label = QtWidgets.QLabel(info_text)
        self.label.setWordWrap(True)
        scroll_area.setWidget(self.label)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        self.setLayout(layout)


class OutWindow(QtWidgets.QWidget):
    """
    GUI widget that describes the output files produced by the FQSHA tool.

    It includes information about exported XML source models, activity rates,
    magnitude distributions, and hazard maps generated by OpenQuake.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information")
        self.setGeometry(100, 100, 600, 400)

        layout = QtWidgets.QVBoxLayout()

        # Define info text as a single, formatted paragraph
        info_text = (
            "The outputs of this software include fault .xml files in a format compatible with the OpenQuake engine, "
            "annual cumulative rates, a plot illustrating the potential maximum magnitude calculations, and hazard "
            "maps generated using the OpenQuake algorithm."
        )

        scroll_area = QtWidgets.QScrollArea()
        self.label = QtWidgets.QLabel(info_text)
        self.label.setWordWrap(True)

        scroll_area.setWidget(self.label)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)
        self.setLayout(layout)


def browse_file(self):
    """
    Opens a file dialog for selecting a JSON input file.

    Loads the selected fault model file and stores it in the `self.faults` variable.
    """
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(None, "Select the input file:", "Choose one:",
                                               "JSON files (*.json);;All files (*)", options=options)
    if file_path:
        print("Selected file:", file_path)
        self.input_file_var = file_path

        # Load the selected JSON file
        try:
            with open(file_path, 'r') as f:
                self.faults = json.load(f)

            if self.faults:
                print(f"Loaded JSON data: {len(self.faults)} faults found.")
        except Exception as e:
            print("Error loading JSON file:", e)



def run_seismic_and_export(self):
    print("SeismicActivityRate called (mock implementation).")


class Ui_Frame(object):
    """
    Main GUI class for setting up and running the FQSHA workflow.

    Provides a complete interface for selecting GMPEs, input parameters, 
    magnitude scaling relationships, and running the seismic activity rate computation
    and OpenQuake-based hazard calculations.
    """
    def __init__(self, Project_foldername=None):
        self.Project_foldername = Project_foldername
        self.inputs = {}  # Initialize the inputs dictionary
        self.faults = {}




    def get_output_directory(self):
        folder_name = self.textEdit_13.toPlainText().strip() or "FQSHA_output"  # Use default if no input
        main_output_directory = os.path.join(os.getcwd(), folder_name)
        sources_directory = os.path.join(main_output_directory, "Sources")
        return main_output_directory, sources_directory




    def collect_inputs(self):
        # Collect data from checkboxes
        self.inputs['AbrahamsonEtAl2014'] = self.checkBox.isChecked()
        self.inputs['BooreEtAl2014'] = self.checkBox_2.isChecked()
        self.inputs['CampbellBozorgnia2014'] = self.checkBox_3.isChecked()
        self.inputs['ChiouYoungs2014'] = self.checkBox_4.isChecked()
        self.inputs['YoungsEtAl1997SSlab'] = self.checkBox_5.isChecked()
        self.inputs['Atkinson2015'] = self.checkBox_6.isChecked()
        self.inputs['AtkinsonBoore2003SInter'] = self.checkBox_7.isChecked()
        self.inputs['AtkinsonBoore2006'] = self.checkBox_8.isChecked()
        self.inputs['AbrahamsonEtAl2018SInter'] = self.checkBox_9.isChecked()
        self.inputs['ToroEtAl1997'] = self.checkBox_10.isChecked()
        self.inputs['AkkarBommer2010'] = self.checkBox_11.isChecked()
        self.inputs['AbrahamsonEtAl2015SSlab'] = self.checkBox_12.isChecked()
        self.inputs['AkkarEtAlRepi2014'] = self.checkBox_13.isChecked()
        self.inputs['BooreAtkinson2008'] = self.checkBox_14.isChecked()
        self.inputs['CampbellBozorgnia2008'] = self.checkBox_15.isChecked()
        self.inputs['ChiouYoungs2008'] = self.checkBox_16.isChecked()
        self.inputs['ZhaoEtAl2016Asc'] = self.checkBox_17.isChecked()
        self.inputs['Idriss2014'] = self.checkBox_18.isChecked()
        self.inputs['McVerryEtAl2006'] = self.checkBox_19.isChecked()
        self.inputs['Bradley2010'] = self.checkBox_20.isChecked()
        self.inputs['SilvaEtAl2002'] = self.checkBox_21.isChecked()
        self.inputs['AkkarEtAlRjb2014'] = self.checkBox_22.isChecked()

        # Collect data from text edits
        self.inputs['textEdit_7'] = self.textEdit_7.toPlainText().strip()
        self.inputs['textEdit_2'] = self.textEdit_2.toPlainText().strip()
        self.inputs['textEdit_5'] = self.textEdit_5.toPlainText().strip()
        self.inputs['textEdit_6'] = self.textEdit_6.toPlainText().strip()
        self.inputs['textEdit_10'] = self.textEdit_10.toPlainText().strip()
        self.inputs['textEdit_9'] = self.textEdit_9.toPlainText().strip()
        self.inputs['textEdit_12'] = self.textEdit_12.toPlainText().strip()
        self.inputs['textEdit_13'] = self.textEdit_13.toPlainText().strip()
        self.inputs['comboBox_2'] = self.comboBox_2.currentText()
        self.inputs['faults'] = self.faults

##############The inputs for weights of the GMPEs

        self.inputs['weights'] = {
            'AbrahamsonEtAl2014': self.lineEdit_AbrahamsonEtAl2014.text().strip(),
            'BooreEtAl2014': self.lineEdit_BooreEtAl2014.text().strip(),
            'CampbellBozorgnia2014': self.lineEdit_CampbellBozorgnia2014.text().strip(),
            'ChiouYoungs2014': self.lineEdit_ChiouYoungs2014.text().strip(),
            'YoungsEtAl1997SSlab': self.lineEdit_YoungsEtAl1997SSlab.text().strip(),
            'Atkinson2015': self.lineEdit_Atkinson2015.text().strip(),
            'AtkinsonBoore2003SInter': self.lineEdit_AtkinsonBoore2003SInter.text().strip(),
            'AtkinsonBoore2006': self.lineEdit_AtkinsonBoore2006.text().strip(),
            'AbrahamsonEtAl2018SInter': self.lineEdit_AbrahamsonEtAl2018SInter.text().strip(),
            'ToroEtAl1997': self.lineEdit_ToroEtAl1997.text().strip(),
            'AkkarBommer2010': self.lineEdit_AkkarBommer2010.text().strip(),
            'AbrahamsonEtAl2015SSlab': self.lineEdit_AbrahamsonEtAl2015SSlab.text().strip(),
            'AkkarEtAlRepi2014': self.lineEdit_AkkarEtAlRepi2014.text().strip(),
            'BooreAtkinson2008': self.lineEdit_BooreAtkinson2008.text().strip(),
            'CampbellBozorgnia2008': self.lineEdit_CampbellBozorgnia2008.text().strip(),
            'ChiouYoungs2008': self.lineEdit_ChiouYoungs2008.text().strip(),
            'ZhaoEtAl2016Asc': self.lineEdit_ZhaoEtAl2016Asc.text().strip(),
            'Idriss2014': self.lineEdit_Idriss2014.text().strip(),
            'McVerryEtAl2006': self.lineEdit_McVerryEtAl2006.text().strip(),
            'Bradley2010': self.lineEdit_Bradley2010.text().strip(),
            'SilvaEtAl2002': self.lineEdit_SilvaEtAl2002.text().strip(),
            'AkkarEtAlRjb2014': self.lineEdit_AkkarEtAlRjb2014.text().strip()
        }

    def export_inputs(self, filename='inputs.json'):
        with open(filename, 'w') as file:
            json.dump(self.inputs, file, indent=4)
        print(f"Inputs saved to {filename}")



    def find_latest_hazard_map(self, output_directory):
        import glob
        import os

        output_dir = os.path.join(output_directory, "OutPut")
        file_pattern = os.path.join(output_dir, "hazard_map-mean_*.csv")
        files = glob.glob(file_pattern)

        if not files:
            print("No hazard map files found.")
            return None

        files.sort(key=lambda f: os.path.getmtime(f), reverse=True)
        return files[0]  # Return the most recently modified file



    def export_inputs(self, main_output_directory, filename='inputs.json'):
        # Ensure the main output directory exists
        os.makedirs(main_output_directory, exist_ok=True)

        # Define the full path for inputs.json within the output directory
        full_path = os.path.join(main_output_directory, filename)

        # Write the full inputs to the file in the specified directory
        with open(full_path, 'w') as file:
            json.dump(self.inputs, file, indent=4)
        print(f"Inputs saved to {full_path}")

        # Export only fault traces to a separate JSON file
        fault_traces = {
            fault_name: {'fault_trace': fault_info['fault_trace']}
            for fault_name, fault_info in self.inputs.get('faults', {}).items()
            if 'fault_trace' in fault_info
        }
        fault_traces_path = os.path.join(main_output_directory, 'fault_traces.json')

        with open(fault_traces_path, 'w') as file:
            json.dump(fault_traces, file, indent=4)
        print(f"Fault traces saved to {fault_traces_path}")



    def run_seismic_and_export(self):
        """
    Executes the full FQSHA workflow from input collection to hazard map generation.

    This includes:
    - Gathering user input,
    - Generating OpenQuake logic tree files,
    - Calculating seismic activity rates,
    - Running OpenQuake,
    - Generating and displaying hazard maps.
    """

        self.collect_inputs()

        # Get the main output directory
        main_output_directory, sources_directory = self.get_output_directory()

        # Export inputs to the main output directory
        self.export_inputs(main_output_directory)

        # Continue with other steps
        source_model_logic_tree(self.inputs['faults'], main_output_directory)

        all_fault_traces = []
        # Loop through each fault in the 'faults' dictionary
        for fault_name, fault_data in self.inputs['faults'].items():
            if 'fault_trace' in fault_data:  # Check if the key exists (safety)
                all_fault_traces.extend(fault_data['fault_trace'])  # Concatenate the traces

        longitudess = [point[0] for point in all_fault_traces]
        latitudess = [point[1] for point in all_fault_traces]

        # Step 2: Calculate min/max and ranges
        lon_min, lon_max = min(longitudess), max(longitudess)
        lat_min, lat_max = min(latitudess), max(latitudess)

        lon_range = lon_max - lon_min
        lat_range = lat_max - lat_min

        # Step 3: Compute 10% confidence intervals
        confidence = 0.3  # 10%

        lon_min_ci = lon_min - (lon_range * confidence)
        lon_max_ci = lon_max + (lon_range * confidence)

        lat_min_ci = lat_min - (lat_range * confidence)
        lat_max_ci = lat_max + (lat_range * confidence)

        if self.inputs['textEdit_2'] == '':
            self.inputs['textEdit_2']= str(lat_max_ci)

        if self.inputs['textEdit_7'] == '':
            self.inputs['textEdit_7'] = str(lat_min_ci)

        if self.inputs['textEdit_6'] == '':
            self.inputs['textEdit_6'] = str(lon_max_ci)

        if self.inputs['textEdit_5'] == '':
            self.inputs['textEdit_5'] = str(lon_min_ci)

        if self.inputs['textEdit_12'] == '':
            self.inputs['textEdit_12'] = 'WC1994'

        if self.inputs['textEdit_10'] == '':
            self.inputs['textEdit_10'] = str(100)

        if self.inputs['textEdit_9'] == '':
            self.inputs['textEdit_9'] = str(800)



        generate_job_ini(self.inputs, main_output_directory, self.faults)

        self.SeismicActivityRate(self.faults, self.mfdo)
        gmpe_generate_xml(self.inputs, main_output_directory)
        export_faults_to_xml(self.faults, sources_directory)

        print("Seismic activity rate calculation and OpenQuake input generation completed.")
        self.run_oq_engine(main_output_directory)
        print("Hazard Calculation Completed.")

        # Find and use the latest hazard map CSV file for mapping
        csv_file = self.find_latest_hazard_map(main_output_directory)
        if csv_file is not None:
            fault_file = os.path.join(main_output_directory, "fault_traces.json")
            create_contour_map_with_faults(csv_file, fault_file, main_output_directory)
        else:
            print("No suitable hazard map CSV file found.")

    def run_oq_engine(self, main_output_directory):
        try:
            # Change to the output directory
            os.chdir(main_output_directory)

            # Run the commands
            subprocess.run(['oq', 'engine', '--delete-uncompleted-calculations'], check=True, capture_output=True,
                           text=True)
            result = subprocess.run(['oq', 'engine', '--run', 'job.ini', '--exports=csv'], check=True,
                                    capture_output=True, text=True)

            print("Command output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("An error occurred while running the command:", e.stderr)




    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(1500, 1000)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Frame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Set background color to dark gray
        Frame.setStyleSheet("background-color: darkgray;")

        self.frame_4 = QtWidgets.QFrame(Frame)
        self.frame_4.setMaximumSize(QtCore.QSize(600, 900))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(1, 20, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(205, 171, 143))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.frame_4.setPalette(palette)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)

        self.frame_4.setFont(font)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")

        self.comboBox_2 = QtWidgets.QComboBox(self.frame_4)
        self.comboBox_2.setGeometry(QtCore.QRect(260, 70, 201, 41))
        self.comboBox_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setItalic(True)
        font.setWeight(50)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setObjectName("comboBox_2")

        self.comboBox_2.addItem("Calculation_mode")
        self.comboBox_2.setItemData(0, 0, QtCore.Qt.UserRole - 1)

        self.comboBox_2.addItem("classical")
        self.comboBox_2.addItem("event_based")
        # self.comboBox_2.addItem("scenario")
        # self.comboBox_2.addItem("scenario_damage")


        self.comboBox_2.currentIndexChanged.connect(self.handle_selection)

        self.label_12 = QtWidgets.QLabel(self.frame_4)
        self.label_12.setGeometry(QtCore.QRect(10, 60, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")

        self.label_13 = QtWidgets.QLabel(self.frame_4)
        self.label_13.setGeometry(QtCore.QRect(10, 170, 251, 51))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")

        # Grid Spacing

        self.label_14 = QtWidgets.QLabel(self.frame_4)
        self.label_14.setGeometry(QtCore.QRect(10, 300, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")

        # Vs30

        self.label_28 = QtWidgets.QLabel(self.frame_4)
        self.label_28.setGeometry(QtCore.QRect(200, 300, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")

        # magScaleRel

        self.label_29 = QtWidgets.QLabel(self.frame_4)
        self.label_29.setGeometry(QtCore.QRect(320, 300, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")

        # magnitude scale relationship

        self.textEdit_12 = QtWidgets.QTextEdit(self.frame_4)
        self.textEdit_12.setGeometry(QtCore.QRect(440, 300, 100, 31))
        self.textEdit_12.setStyleSheet("background-color: white; color: black;")
        self.textEdit_12.setObjectName("textEdit_1")

        # max lat
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame_4)
        self.textEdit_2.setGeometry(QtCore.QRect(320, 140, 51, 41))
        self.textEdit_2.setStyleSheet("background-color: white; color: black;")
        self.textEdit_2.setObjectName("textEdit_2")

        # min Lon
        self.textEdit_5 = QtWidgets.QTextEdit(self.frame_4)
        self.textEdit_5.setGeometry(QtCore.QRect(270, 180, 51, 41))
        self.textEdit_5.setStyleSheet("background-color: white; color: black;")
        self.textEdit_5.setObjectName("textEdit_5")

        # max Lon
        self.textEdit_6 = QtWidgets.QTextEdit(self.frame_4)
        self.textEdit_6.setGeometry(QtCore.QRect(370, 180, 51, 41))
        self.textEdit_6.setStyleSheet("background-color: white; color: black;")
        self.textEdit_6.setObjectName("textEdit_6")

        # min lat
        self.textEdit_7 = QtWidgets.QTextEdit(self.frame_4)
        self.textEdit_7.setGeometry(QtCore.QRect(320, 220, 51, 41))
        self.textEdit_7.setStyleSheet("background-color: white; color: black;")
        self.textEdit_7.setObjectName("textEdit_7")

        self.textEdit_10 = QtWidgets.QTextEdit(self.frame_4)
        self.textEdit_10.setGeometry(QtCore.QRect(130, 300, 41, 31))
        self.textEdit_10.setStyleSheet("background-color: white; color: black;")
        self.textEdit_10.setObjectName("textEdit_10")

        self.label_15 = QtWidgets.QLabel(self.frame_4)
        self.label_15.setGeometry(QtCore.QRect(170, 360, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Liberation Serif")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")

        self.checkBox = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox.setGeometry(QtCore.QRect(70, 450, 171, 23))
        self.checkBox.setPalette(palette)
        self.checkBox.setObjectName("checkBox")

        self.checkBox_2 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_2.setGeometry(QtCore.QRect(70, 470, 171, 23))
        self.checkBox_2.setObjectName("checkBox_2")

        self.checkBox_3 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_3.setGeometry(QtCore.QRect(70, 490, 191, 23))
        self.checkBox_3.setObjectName("checkBox_3")

        self.checkBox_4 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_4.setGeometry(QtCore.QRect(70, 510, 191, 23))
        self.checkBox_4.setObjectName("checkBox_4")

        self.checkBox_5 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_5.setGeometry(QtCore.QRect(70, 640, 181, 23))
        self.checkBox_5.setObjectName("checkBox_5")

        self.checkBox_6 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_6.setGeometry(QtCore.QRect(70, 860, 151, 23))
        self.checkBox_6.setObjectName("checkBox_6")

        self.checkBox_7 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_7.setGeometry(QtCore.QRect(70, 680, 181, 23))
        self.checkBox_7.setObjectName("checkBox_7")

        self.checkBox_8 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_8.setGeometry(QtCore.QRect(70, 760, 161, 23))
        self.checkBox_8.setObjectName("checkBox_8")

        self.checkBox_9 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_9.setGeometry(QtCore.QRect(70, 660, 181, 23))
        self.checkBox_9.setObjectName("checkBox_9")

        self.checkBox_10 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_10.setGeometry(QtCore.QRect(70, 780, 161, 23))
        self.checkBox_10.setObjectName("checkBox_10")

        self.checkBox_22 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_22.setGeometry(QtCore.QRect(320, 670, 161, 21))
        self.checkBox_22.setObjectName("checkBox_11")

        self.checkBox_11 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_11.setGeometry(QtCore.QRect(320, 650, 161, 23))
        self.checkBox_11.setObjectName("checkBox_11")

        # GMPE panel lables

        self.label_16 = QtWidgets.QLabel(self.frame_4)
        self.label_16.setGeometry(QtCore.QRect(70, 410, 211, 31))
        self.label_16.setObjectName("label_16")

        self.label_17 = QtWidgets.QLabel(self.frame_4)
        self.label_17.setGeometry(QtCore.QRect(320, 620, 241, 17))
        self.label_17.setObjectName("label_17")

        self.label_18 = QtWidgets.QLabel(self.frame_4)
        self.label_18.setGeometry(QtCore.QRect(70, 840, 141, 17))
        self.label_18.setObjectName("label_18")

        self.label_19 = QtWidgets.QLabel(self.frame_4)
        self.label_19.setGeometry(QtCore.QRect(70, 740, 191, 17))
        self.label_19.setObjectName("label_19")

        # AbrahamsonEtAl2015SSlab
        self.label_20 = QtWidgets.QLabel(self.frame_4)
        self.label_20.setGeometry(QtCore.QRect(70, 620, 131, 17))
        self.label_20.setObjectName("label_20")

        self.label_21 = QtWidgets.QLabel(self.frame_4)
        self.label_21.setGeometry(QtCore.QRect(320, 410, 161, 41))
        self.label_21.setObjectName("label_21")

        self.label_22 = QtWidgets.QLabel(self.frame_4)
        self.label_22.setGeometry(QtCore.QRect(70, 550, 67, 17))
        self.label_22.setObjectName("label_22")

        self.label_23 = QtWidgets.QLabel(self.frame_4)
        self.label_23.setGeometry(QtCore.QRect(320, 550, 171, 16))
        self.label_23.setObjectName("label_23")

        self.label_24 = QtWidgets.QLabel(self.frame_4)
        self.label_24.setGeometry(QtCore.QRect(320, 740, 131, 21))
        self.label_24.setObjectName("label_24")

        self.label_25 = QtWidgets.QLabel(self.frame_4)
        self.label_25.setGeometry(QtCore.QRect(320, 830, 211, 31))
        self.label_25.setObjectName("label_25")

        self.label_30 = QtWidgets.QLabel(self.frame_4)
        self.label_30.setGeometry(QtCore.QRect(10, 425, 50, 20))  # adjust as needed
        self.label_30.setText("Weight")
        self.label_30.setObjectName("label_30")

        self.label_31 = QtWidgets.QLabel(self.frame_4)
        self.label_31.setGeometry(QtCore.QRect(260, 425, 50, 20))  # adjust as needed
        self.label_31.setText("Weight")
        self.label_31.setObjectName("label_30")


        self.checkBox_12 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_12.setGeometry(QtCore.QRect(70, 700, 161, 23))
        self.checkBox_12.setObjectName("checkBox_12")

        self.checkBox_13 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_13.setGeometry(QtCore.QRect(320, 690, 171, 23))
        self.checkBox_13.setObjectName("checkBox_13")


        self.checkBox_14 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_14.setGeometry(QtCore.QRect(320, 460, 161, 23))
        self.checkBox_14.setObjectName("checkBox_14")

        self.checkBox_15 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_15.setGeometry(QtCore.QRect(320, 480, 191, 23))
        self.checkBox_15.setObjectName("checkBox_15")

        self.checkBox_16 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_16.setGeometry(QtCore.QRect(320, 500, 181, 23))
        self.checkBox_16.setObjectName("checkBox_16")


        self.checkBox_17 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_17.setGeometry(QtCore.QRect(70, 570, 171, 21))
        self.checkBox_17.setObjectName("checkBox_17")

        self.checkBox_18 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_18.setGeometry(QtCore.QRect(320, 570, 92, 23))
        self.checkBox_18.setObjectName("checkBox_18")

        self.checkBox_19 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_19.setGeometry(QtCore.QRect(330, 770, 141, 23))
        self.checkBox_19.setObjectName("checkBox_19")

        self.checkBox_20 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_20.setGeometry(QtCore.QRect(330, 790, 103, 23))
        self.checkBox_20.setObjectName("checkBox_20")

        self.checkBox_21 = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox_21.setGeometry(QtCore.QRect(330, 860, 121, 23))
        self.checkBox_21.setObjectName("checkBox_21")

        ######################## The text edit boxes for weights

        self.lineEdit_AbrahamsonEtAl2014 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_AbrahamsonEtAl2014.setGeometry(QtCore.QRect(30, 450, 30, 20))
        self.lineEdit_AbrahamsonEtAl2014.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_AbrahamsonEtAl2014.setObjectName("lineEdit_AbrahamsonEtAl2014")
        self.lineEdit_AbrahamsonEtAl2014.setPlaceholderText("1")

        self.lineEdit_BooreEtAl2014 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_BooreEtAl2014.setGeometry(QtCore.QRect(30, 470, 30, 20))
        self.lineEdit_BooreEtAl2014.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_BooreEtAl2014.setObjectName("lineEdit_BooreEtAl2014")
        self.lineEdit_BooreEtAl2014.setPlaceholderText("1")

        self.lineEdit_CampbellBozorgnia2014 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_CampbellBozorgnia2014.setGeometry(QtCore.QRect(30, 490, 30, 20))
        self.lineEdit_CampbellBozorgnia2014.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_CampbellBozorgnia2014.setObjectName("lineEdit_CampbellBozorgnia2014")
        self.lineEdit_CampbellBozorgnia2014.setPlaceholderText("1")

        self.lineEdit_ChiouYoungs2014 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_ChiouYoungs2014.setGeometry(QtCore.QRect(30, 510, 30, 20))
        self.lineEdit_ChiouYoungs2014.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_ChiouYoungs2014.setObjectName("lineEdit_ChiouYoungs2014")
        self.lineEdit_ChiouYoungs2014.setPlaceholderText("1")

        self.lineEdit_YoungsEtAl1997SSlab = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_YoungsEtAl1997SSlab.setGeometry(QtCore.QRect(30, 640, 30, 20))
        self.lineEdit_YoungsEtAl1997SSlab.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_YoungsEtAl1997SSlab.setObjectName("lineEdit_YoungsEtAl1997SSlab")
        self.lineEdit_YoungsEtAl1997SSlab.setPlaceholderText("1")

        self.lineEdit_Atkinson2015 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_Atkinson2015.setGeometry(QtCore.QRect(30, 860, 30, 20))
        self.lineEdit_Atkinson2015.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_Atkinson2015.setObjectName("lineEdit_Atkinson2015")
        self.lineEdit_Atkinson2015.setPlaceholderText("1")

        self.lineEdit_AtkinsonBoore2003SInter = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_AtkinsonBoore2003SInter.setGeometry(QtCore.QRect(30, 680, 30, 20))
        self.lineEdit_AtkinsonBoore2003SInter.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_AtkinsonBoore2003SInter.setObjectName("lineEdit_AtkinsonBoore2003SInter")
        self.lineEdit_AtkinsonBoore2003SInter.setPlaceholderText("1")

        self.lineEdit_AtkinsonBoore2006 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_AtkinsonBoore2006.setGeometry(QtCore.QRect(30, 760, 30, 20))
        self.lineEdit_AtkinsonBoore2006.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_AtkinsonBoore2006.setObjectName("lineEdit_AtkinsonBoore2006")
        self.lineEdit_AtkinsonBoore2006.setPlaceholderText("1")

        self.lineEdit_AbrahamsonEtAl2018SInter = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_AbrahamsonEtAl2018SInter.setGeometry(QtCore.QRect(30, 660, 30, 20))
        self.lineEdit_AbrahamsonEtAl2018SInter.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_AbrahamsonEtAl2018SInter.setObjectName("lineEdit_AbrahamsonEtAl2018SInter")
        self.lineEdit_AbrahamsonEtAl2018SInter.setPlaceholderText("1")

        self.lineEdit_ToroEtAl1997 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_ToroEtAl1997.setGeometry(QtCore.QRect(30, 780, 30, 20))
        self.lineEdit_ToroEtAl1997.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_ToroEtAl1997.setObjectName("lineEdit_ToroEtAl1997")
        self.lineEdit_ToroEtAl1997.setPlaceholderText("1")

        self.lineEdit_AkkarBommer2010 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_AkkarBommer2010.setGeometry(QtCore.QRect(280, 650, 30, 20))
        self.lineEdit_AkkarBommer2010.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_AkkarBommer2010.setObjectName("lineEdit_AkkarBommer2010")
        self.lineEdit_AkkarBommer2010.setPlaceholderText("1")

        self.lineEdit_AbrahamsonEtAl2015SSlab = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_AbrahamsonEtAl2015SSlab.setGeometry(QtCore.QRect(30, 700, 30, 20))
        self.lineEdit_AbrahamsonEtAl2015SSlab.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_AbrahamsonEtAl2015SSlab.setObjectName("lineEdit_AbrahamsonEtAl2015SSlab")
        self.lineEdit_AbrahamsonEtAl2015SSlab.setPlaceholderText("1")

        self.lineEdit_AkkarEtAlRepi2014 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_AkkarEtAlRepi2014.setGeometry(QtCore.QRect(280, 690, 30, 20))
        self.lineEdit_AkkarEtAlRepi2014.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_AkkarEtAlRepi2014.setObjectName("lineEdit_AkkarEtAlRepi2014")
        self.lineEdit_AkkarEtAlRepi2014.setPlaceholderText("1")

        self.lineEdit_BooreAtkinson2008 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_BooreAtkinson2008.setGeometry(QtCore.QRect(280, 460, 30, 20))
        self.lineEdit_BooreAtkinson2008.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_BooreAtkinson2008.setObjectName("lineEdit_BooreAtkinson2008")
        self.lineEdit_BooreAtkinson2008.setPlaceholderText("1")

        self.lineEdit_CampbellBozorgnia2008 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_CampbellBozorgnia2008.setGeometry(QtCore.QRect(280, 480, 30, 20))
        self.lineEdit_CampbellBozorgnia2008.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_CampbellBozorgnia2008.setObjectName("lineEdit_CampbellBozorgnia2008")
        self.lineEdit_CampbellBozorgnia2008.setPlaceholderText("1")

        self.lineEdit_ChiouYoungs2008 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_ChiouYoungs2008.setGeometry(QtCore.QRect(280, 500, 30, 20))
        self.lineEdit_ChiouYoungs2008.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_ChiouYoungs2008.setObjectName("lineEdit_ChiouYoungs2008")
        self.lineEdit_ChiouYoungs2008.setPlaceholderText("1")

        self.lineEdit_ZhaoEtAl2016Asc = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_ZhaoEtAl2016Asc.setGeometry(QtCore.QRect(30, 570, 30, 20))
        self.lineEdit_ZhaoEtAl2016Asc.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_ZhaoEtAl2016Asc.setObjectName("lineEdit_ZhaoEtAl2016Asc")
        self.lineEdit_ZhaoEtAl2016Asc.setPlaceholderText("1")


        self.lineEdit_Idriss2014 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_Idriss2014.setGeometry(QtCore.QRect(280, 570, 30, 20))
        self.lineEdit_Idriss2014.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_Idriss2014.setObjectName("lineEdit_Idriss2014")
        self.lineEdit_Idriss2014.setPlaceholderText("1")

        self.lineEdit_McVerryEtAl2006 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_McVerryEtAl2006.setGeometry(QtCore.QRect(280, 770, 30, 20))
        self.lineEdit_McVerryEtAl2006.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_McVerryEtAl2006.setObjectName("lineEdit_McVerryEtAl2006")
        self.lineEdit_McVerryEtAl2006.setPlaceholderText("1")

        self.lineEdit_Bradley2010 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_Bradley2010.setGeometry(QtCore.QRect(280, 790, 30, 20))
        self.lineEdit_Bradley2010.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_Bradley2010.setObjectName("lineEdit_Bradley2010")
        self.lineEdit_Bradley2010.setPlaceholderText("1")

        self.lineEdit_SilvaEtAl2002 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_SilvaEtAl2002.setGeometry(QtCore.QRect(280, 860, 30, 20))
        self.lineEdit_SilvaEtAl2002.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_SilvaEtAl2002.setObjectName("lineEdit_SilvaEtAl2002")
        self.lineEdit_SilvaEtAl2002.setPlaceholderText("1")

        self.lineEdit_AkkarEtAlRjb2014 = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit_AkkarEtAlRjb2014.setGeometry(QtCore.QRect(280, 670, 30, 20))
        self.lineEdit_AkkarEtAlRjb2014.setStyleSheet("background-color: white; color: black;")
        self.lineEdit_AkkarEtAlRjb2014.setObjectName("lineEdit_AkkarEtAlRjb2014")
        self.lineEdit_AkkarEtAlRjb2014.setPlaceholderText("1")

        ######################## The text edit boxes for weights


        self.label_26 = QtWidgets.QLabel(self.frame_4)
        self.label_26.setGeometry(QtCore.QRect(190, 10, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")

        self.textEdit_9 = QtWidgets.QTextEdit(self.frame_4)
        self.textEdit_9.setGeometry(QtCore.QRect(260, 300, 41, 31))
        self.textEdit_9.setStyleSheet("background-color: white; color: black;")
        self.textEdit_9.setObjectName("textEdit_9")

        self.horizontalLayout.addWidget(self.frame_4)
        self.frame = QtWidgets.QFrame(Frame)
        self.frame.setMaximumSize(QtCore.QSize(400, 900))
        self.frame.setPalette(palette)
        self.frame.setAccessibleName("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # Browse
        self.pushButton = QtWidgets.QPushButton(self.frame)
        # self.pushButton.clicked.connect(lambda: browse_file(ui))
        self.pushButton.clicked.connect(lambda: browse_file(self))
        self.pushButton.setGeometry(QtCore.QRect(140, 390, 141, 41))
        self.pushButton.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(17)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        # # Assuming 'Frame' is the correct parent widget
        # self.pushButton = QtWidgets.QPushButton('Browse', Frame)
        # self.pushButton.setGeometry(QtCore.QRect(140, 390, 141, 41))
        # self.pushButton.clicked.connect(self.browse_file)
        # layout.addWidget(self.pushButton)

        # Store checkboxes in a list
        self.checkboxes = [
            self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4,
            self.checkBox_5, self.checkBox_6, self.checkBox_7, self.checkBox_8,
            self.checkBox_9, self.checkBox_10, self.checkBox_11,self.checkBox_22,
            self.checkBox_12, self.checkBox_13, self.checkBox_14, self.checkBox_15,
            self.checkBox_16, self.checkBox_17, self.checkBox_18, self.checkBox_19,
            self.checkBox_20, self.checkBox_21
        ]

        # Define the styles and font properties for all checkboxes
        checkbox_style = """
                   QCheckBox::indicator {
                       width: 15px;
                       height: 15px;
                       border: 1px solid black;
                       background-color: white;
                   }
                   QCheckBox::indicator:checked {
                       background-color: black;
                   }
               """

        font = QtGui.QFont()
        font.setBold(True)

        # Apply the style and font to each checkbox in the list
        for checkbox in self.checkboxes:
            checkbox.setStyleSheet(checkbox_style)
            checkbox.setFont(font)



        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setText("RUN")
        self.pushButton_2.setGeometry(QtCore.QRect(110, 700, 201, 71))



        # Set the background color to a brownish-orange and the text color to black
        self.pushButton_2.setStyleSheet("background-color: blue; color: black;")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.run_seismic_and_export)


        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(90, 330, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(19)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setIndent(-3)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(60, 480, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(19)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setIndent(-3)
        self.label_3.setObjectName("label_3")


        # Output file name
        self.textEdit_13 = QtWidgets.QTextEdit(self.frame)
        self.textEdit_13.setGeometry(QtCore.QRect(120, 530, 181, 41))
        self.textEdit_13.setStyleSheet("background-color: white; color: black;")
        self.textEdit_13.setPalette(palette)
        self.textEdit_13.setObjectName("textEdit_13")

        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(60, 60, 281, 181))
        self.label_7.setPixmap(QtGui.QPixmap("./logo-1.png"))
        self.label_7.setScaledContents(True)  # Ensure the image fits within the label
        self.label_7.setObjectName("label_7")

        self.horizontalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(Frame)
        self.frame_2.setMaximumSize(QtCore.QSize(500, 900))
        self.frame_2.setPalette(palette)
        self.frame_2.setAcceptDrops(False)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(90, 600, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setIndent(-3)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(90, 520, 261, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setIndent(-3)
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(30, 700, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_6.setTextFormat(QtCore.Qt.AutoText)
        self.label_6.setIndent(-3)
        self.label_6.setObjectName("label_6")

        self.textEdit_3 = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit_3.setGeometry(QtCore.QRect(190, 560, 201, 31))
        self.textEdit_3.setStyleSheet("background-color: white; color: black;")
        self.textEdit_3.setPalette(palette)
        self.textEdit_3.setObjectName("textEdit_3")

        self.textEdit_4 = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit_4.setGeometry(QtCore.QRect(190, 640, 201, 31))
        self.textEdit_4.setStyleSheet("background-color: white; color: black;")
        self.textEdit_4.setPalette(palette)
        self.textEdit_4.setObjectName("textEdit_4")

        self.pushButton_3 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 770, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.open_info_window)

        self.pushButton_5 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_5.setGeometry(QtCore.QRect(160, 810, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.open_scale_window)



        self.pushButton_6 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_6.setGeometry(QtCore.QRect(160, 850, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.open_out_info_window)




        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(80, 250, 351, 141))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setGeometry(QtCore.QRect(90, 0, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")

        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setGeometry(QtCore.QRect(60, 50, 41, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setGeometry(QtCore.QRect(60, 80, 41, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")

        # Khi:

        self.textEdit = QtWidgets.QTextEdit(self.frame_3)
        self.textEdit.setGeometry(QtCore.QRect(120, 40, 201, 31))
        self.textEdit.setStyleSheet("background-color: white; color: black;")
        self.textEdit.setPalette(palette)
        self.textEdit.setObjectName("textEdit")

        # Zeta:

        self.textEdit_11 = QtWidgets.QTextEdit(self.frame_3)
        self.textEdit_11.setGeometry(QtCore.QRect(120, 80, 201, 31))
        self.textEdit_11.setStyleSheet("background-color: white; color: black;")
        self.textEdit_11.setPalette(palette)
        self.textEdit_11.setObjectName("textEdit_11")

        self.label_11 = QtWidgets.QLabel(self.frame_2)
        self.label_11.setGeometry(QtCore.QRect(90, 430, 251, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")

        self.textEdit_8 = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit_8.setGeometry(QtCore.QRect(190, 460, 201, 31))
        self.textEdit_8.setStyleSheet("background-color: white; color: black;")
        self.textEdit_8.setPalette(palette)
        self.textEdit_8.setObjectName("textEdit_8")

        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(100, 70, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setIndent(-3)
        self.label.setObjectName("label")

        # Setting up the ComboBox for MFD selection
        self.comboBox = QtWidgets.QComboBox(self.frame_2)
        self.comboBox.setGeometry(QtCore.QRect(60, 140, 391, 41))
        self.comboBox.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setStrikeOut(False)
        self.comboBox.setFont(font)
        self.comboBox.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.currentIndexChanged.connect(self.set_mfdo)

        self.comboBox.addItem("Magnitude Frequency Distribution options")
        self.comboBox.addItem("Truncated Gutenberg Richter")
        self.comboBox.addItem("Characteristic Gaussian")

        self.comboBox.setItemData(0, 0, QtCore.Qt.UserRole - 1)

        self.label_27 = QtWidgets.QLabel(self.frame_2)
        self.label_27.setGeometry(QtCore.QRect(30, 10, 451, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")

        self.pushButton_4 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_4.setGeometry(QtCore.QRect(158, 730, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Serif")
        font.setPointSize(14)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.open_FQSHA_describe)


        self.horizontalLayout.addWidget(self.frame_2)
        self.frame.raise_()
        self.frame_4.raise_()
        self.frame_2.raise_()

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

        self.textEdits = [
            self.textEdit, self.textEdit_2, self.textEdit_3, self.textEdit_4,
            self.textEdit_5, self.textEdit_6, self.textEdit_7, self.textEdit_8,
            self.textEdit_9, self.textEdit_10, self.textEdit_11, self.textEdit_12,
            self.textEdit_13
        ]

        for textEdit in self.textEdits:
            textEdit.setStyleSheet("""
                background-color: white;  /* Background color */
                color: black;             /* Text color */
                border: 1.2px solid black;  /* Border */
                border-radius: 1px;       /* Optional: Rounds the corners slightly */
            """)



    def SeismicActivityRate(self, faults, mfdo):
        """
    Computes the seismic activity rate for each fault using user-defined parameters.

    Parameters
    ----------
    faults : dict
        Dictionary of fault parameters including geometry, slip, and Mobs.
    mfdo : str
        Magnitude frequency distribution option (e.g., 'Truncated Gutenberg Richter').

    Notes
    -----
    - Calls `momentbudget()` to estimate Mmax and recurrence.
    - Applies either Gaussian or GR model to compute seismicity.
    - Default values are used if the user leaves input fields blank.
    """
        ProjFol = self.textEdit.toPlainText()
        PTI = self.textEdit_3.toPlainText()
        bin = self.textEdit_4.toPlainText()
        Khi = self.textEdit.toPlainText()
        Zeta = self.textEdit_11.toPlainText()
        Siggma = self.textEdit_8.toPlainText()
        Mag_Scale = self.textEdit_12.toPlainText()

        # Set default values if empty
        if not Mag_Scale:
            Mag_Scale = "WC1994"
            print('Window of observation: Where necessary you are using default magnitude scale relationship: WC1994')
        if not PTI:
            PTI = "50"
            print('Window of observation: Where necessary you are using default value 50 years')
        if not bin:
            bin = "0.1"
            print('binstep: Where necessary you are using default value 0.1')
        try:
            PTI = float(PTI)
            bin = float(bin)
        except ValueError:
            raise ValueError(
                "Consider inputting a proper number for 'Probability Time Interval', and 'Magnitude Bin Size'")

        if not Zeta:
            Zeta = "0.5"
            print('Magnitude difference: Where necessary you are using default value 0.5')
        if not Khi:
            Khi = "0.2"
            print('Multiplication Factor: Where necessary you are using default value 0.2')

        if not Siggma:
            Siggma = "0.3"
            print('Standard Deviation: Where necessary you are using default value 0.3')
        try:
            Khi = float(Khi)
            Zeta = float(Zeta)
            Siggma = float(Siggma)

        except ValueError:
            raise ValueError(
                "Consider inputting a proper number for 'Probability Time Interval', and 'Magnitude Bin Size'")




        faults_u = momentbudget(faults, Zeta, Khi, Siggma, ProjFol='output_files', logical_nan='NAN, "",NaN',
                                logical_nan_sdmag='NAN, "",NaN')

        for key, sub_dict in faults_u.items():
            sub_dict['mag_scale'] = Mag_Scale

        if ProjFol == '':
            ProjFol == 'output_files'
        sactivityrate(faults_u, mfdo, PTI, bin, ProjFol='output_files')


    # set_mfdo method
    def set_mfdo(self, index):
        """
    Sets the selected magnitude frequency distribution option.

    Parameters
    ----------
    index : int
        Index from the combo box selection.
    """

        options = [
            "Magnitude Frequency Distribution options",
            "Truncated Gutenberg Richter",
            "Characteristic Gaussian",
        ]

        if index == 0:
            return

        mfdo = options[index]
        self.mfdo = mfdo
        print(f"Selected option: {self.mfdo}")



    # Calculation Mode
    def handle_selection(self):
        """
    Handles user selection from the hazard calculation mode combo box.

    Supported modes:
    - Classical
    - Event-based
    - Scenario (commented)
    """
        # self.comboBox_2.setCurrentText("classical")

        selected_option = self.comboBox_2.currentText()
        print(f"Selected option: {selected_option}")

        if selected_option == "classical":
            print("Classical method selected")
        elif selected_option == "event_based":
            print("Event-based method selected")
        elif selected_option == "scenario":
            print("Scenario method selected")
        elif selected_option == "scenario_damage":
            print("Scenario damage method selected")


    def open_info_window(self):
        self.info_window = InfoWindow()
        self.info_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.info_window.show()

    def open_out_info_window(self):
        self.info_window = OutWindow()
        self.info_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.info_window.show()

    def open_scale_window(self):
        self.scale_window = Scale_Window()
        self.scale_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.scale_window.show()


    def open_FQSHA_describe(self):
        self.info_window = FQSHAWindow()
        self.info_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.info_window.show()




    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("FQSHA", "FQSHA"))
        self.comboBox.setItemText(0, _translate("FQSHA", "Magnitude Frequency Distribution options"))
        self.comboBox.setItemText(1, _translate("FQSHA", "Truncated Gutenberg Richter"))
        self.comboBox.setItemText(2, _translate("FQSHA", "Caracteristic gaussian"))

        self.comboBox_2.setAccessibleDescription(_translate("FQSHA", "Calculation Mode"))
        self.comboBox_2.setItemText(0, _translate("FQSHA", "Calculation Mode"))
        self.comboBox_2.setItemText(1, _translate("FQSHA", "classical"))
        self.comboBox_2.setItemText(2, _translate("FQSHA", "event_based"))
        self.comboBox_2.setItemText(3, _translate("FQSHA", "scenario"))
        # self.comboBox_2.setItemText(4, _translate("FQSHA", "scenario_damage"))
        # self.comboBox_2.setItemText(5, _translate("FQSHA", "scenario"))
        self.comboBox_2.setItemText(4, _translate("FQSHA", "event_based"))

        self.checkBox.setText(_translate("FQSHA", "AbrahamsonEtAl2014"))
        self.checkBox_2.setText(_translate("FQSHA", "BooreEtAl2014"))
        self.checkBox_3.setText(_translate("FQSHA", "CampbellBozorgnia2014"))
        self.checkBox_4.setText(_translate("FQSHA", "ChiouYoungs2014"))
        self.checkBox_5.setText(_translate("FQSHA", "YoungsEtAl1997SSlab"))
        self.checkBox_6.setText(_translate("FQSHA", "Atkinson2015"))
        self.checkBox_7.setText(_translate("FQSHA", "AtkinsonBoore2003SInter"))
        self.checkBox_8.setText(_translate("FQSHA", "AtkinsonBoore2006"))
        self.checkBox_9.setText(_translate("FQSHA", "AbrahamsonEtAl2018SInter"))
        self.checkBox_10.setText(_translate("FQSHA", "ToroEtAl1997"))
        self.checkBox_22.setText(_translate("FQSHA", "AkkarEtAlRjb2014"))
        self.checkBox_11.setText(_translate("FQSHA", "AkkarBommer2010"))
        self.checkBox_12.setText(_translate("FQSHA", "AbrahamsonEtAl2015SSlab"))
        self.checkBox_13.setText(_translate("FQSHA", "AkkarEtAlRepi2014"))
        self.checkBox_14.setText(_translate("FQSHA", "BooreAtkinson2008"))
        self.checkBox_15.setText(_translate("FQSHA", "CampbellBozorgnia2008"))
        self.checkBox_16.setText(_translate("FQSHA", "ChiouYoungs2008"))
        self.checkBox_17.setText(_translate("FQSHA", "ZhaoEtAl2016Asc"))
        self.checkBox_18.setText(_translate("FQSHA", "Idriss2014"))
        self.checkBox_19.setText(_translate("FQSHA", "McVerryEtAl2006"))
        self.checkBox_20.setText(_translate("FQSHA", "Bradley2010"))
        self.checkBox_21.setText(_translate("FQSHA", "SilvaEtAl2002"))


        self.textEdit.setHtml(_translate("FQSHA", ""))  # Khi
        self.textEdit_2.setHtml(_translate("FQSHA", ""))  # max lat
        self.textEdit_3.setHtml(_translate("FQSHA", ""))  # Probability Window(PTI)
        self.textEdit_4.setHtml(_translate("FQSHA", ""))  # Bin Size
        self.textEdit_5.setHtml(_translate("FQSHA", ""))  # min lon
        self.textEdit_6.setHtml(_translate("FQSHA", ""))  # max lon
        self.textEdit_7.setHtml(_translate("FQSHA", ""))  # min lat
        self.textEdit_8.setHtml(_translate("FQSHA", ""))  # Standard deviation
        self.textEdit_9.setHtml(_translate("FQSHA", ""))  # VS30
        self.textEdit_10.setHtml(_translate("FQSHA", ""))  # Grid spacing
        self.textEdit_11.setHtml(_translate("FQSHA", ""))  # Zeta
        self.textEdit_12.setHtml(_translate("FQSHA", ""))  # magnitude scale relationship
        self.textEdit_13.setHtml(_translate("FQSHA", ""))  # Output file name

        self.pushButton.setText(_translate("FQSHA", "Browse"))
        self.pushButton_2.setText(_translate("FQSHA", "RUN"))
        self.pushButton_3.setText(_translate("FQSHA", "FQSHA Input file format"))
        self.pushButton_4.setText(_translate("FQSHA", "FQSHA Description"))
        self.pushButton_5.setText(_translate("FQSHA", "Scale-Relationship selection"))
        self.pushButton_6.setText(_translate("FQSHA", "FQSHA output file format"))

        self.label.setText(_translate("FQSHA", "Activity Rate calculation options:"))
        self.label_2.setText(_translate("FQSHA", "Select the input file:"))
        self.label_3.setText(_translate("FQSHA", "Write the output file name:"))
        self.label_4.setText(_translate("FQSHA", "bin size:"))
        self.label_5.setText(_translate("FQSHA", "Probability Window (years):"))
        self.label_6.setText(_translate("FQSHA", "Application guide:"))
        self.label_8.setText(_translate("FQSHA", "OVCW Parameters:"))
        self.label_9.setText(_translate("FQSHA", "<html>&#950; =</html>"))  # Greek letter xi: ξ:0.2
        self.label_10.setText(_translate("FQSHA", "<html>&#958; =</html>"))  # Greek letter zeta: ζ: 0.5
        self.label_11.setText(_translate("FQSHA", "Mw(M0) Standard Deviation:"))
        self.label_12.setText(_translate("FQSHA", "Hazard Calculation Type:"))
        self.label_13.setText(_translate("FQSHA", "Hazard Calculation Region:"))
        self.label_14.setText(_translate("FQSHA", "Grid Spacing:"))
        self.label_15.setText(_translate("FQSHA", "GMPE Selection:"))
        self.label_16.setText(_translate("FQSHA", "Active Shallow Crustal Regions\n" " (NGA-West2 models):"))
        self.label_17.setText(_translate("FQSHA", "Europe and the Mediterranean:"))
        self.label_18.setText(_translate("FQSHA", "Induced Seismicity:"))
        self.label_19.setText(_translate("FQSHA", "Stable Continental Regions:"))
        self.label_20.setText(_translate("FQSHA", "Subduction Zones:"))
        self.label_21.setText(_translate("FQSHA", "For Global Applications \n" " (Active Shallow Crust):"))
        self.label_22.setText(_translate("FQSHA", "Japan:"))
        self.label_23.setText(_translate("FQSHA", "Near-Source Effects:"))
        self.label_24.setText(_translate("FQSHA", "New Zealand:"))
        self.label_25.setText(_translate("FQSHA", "For Site-Specific Amplification:"))
        self.label_30.setText(_translate("FQSHA", "Weights:"))
        self.label_31.setText(_translate("FQSHA", "Weights:"))
        self.label_26.setText(_translate("FQSHA", "Hazard Panel"))
        self.label_27.setText(_translate("FQSHA", "Seismic Activity Rate Calculation Panel:"))
        self.label_28.setText(_translate("FQSHA", "VS30: "))
        self.label_29.setText(_translate("FQSHA", "magScaleRel: "))

        self.textEdit.setPlaceholderText(_translate("FQSHA", "0.5"))  # xi: ξ
        self.textEdit_2.setPlaceholderText(_translate("FQSHA", "max lat"))
        self.textEdit_3.setPlaceholderText(_translate("FQSHA", "50"))
        self.textEdit_4.setPlaceholderText(_translate("FQSHA", "0.1"))
        self.textEdit_5.setPlaceholderText(_translate("FQSHA", "min lon"))
        self.textEdit_6.setPlaceholderText(_translate("FQSHA", "max lon"))
        self.textEdit_7.setPlaceholderText(_translate("FQSHA", "min lat"))
        self.textEdit_8.setPlaceholderText(_translate("FQSHA", "0.3"))
        self.textEdit_9.setPlaceholderText(_translate("FQSHA", "800"))
        self.textEdit_10.setPlaceholderText(_translate("FQSHA", "100"))
        self.textEdit_11.setPlaceholderText(_translate("FQSHA", "0.2"))  # zeta:ζ
        self.textEdit_12.setPlaceholderText(_translate("FQSHA", "WC1994"))  # manitude scale relationship

#
# if __name__ == "__main__":
#     import sys


def take_screenshot(widget, filename='screenshot.png', scale=3):
    import os
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtCore import QSize

    # Get the directory of the current script (project root)
    project_root = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(project_root, filename)

    # Create a high-resolution pixmap by scaling
    original_size = widget.size()
    high_res_size = QSize(original_size.width() * scale, original_size.height() * scale)

    # Render to a larger QPixmap
    pixmap = QPixmap(high_res_size)
    pixmap.setDevicePixelRatio(scale)
    widget.render(pixmap)

    # Save as PNG
    pixmap.save(filepath, 'PNG')
    print(f"📸 High-resolution screenshot saved to {filepath}")


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()

    # Add a short delay to ensure the window is rendered
    QtCore.QTimer.singleShot(1000, lambda: take_screenshot(Frame, "FQSHA_screenshot.png", scale=4))

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())

