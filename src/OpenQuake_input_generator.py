import os

def gmpe_generate_xml(checkboxes, output_directory="../FQSHA_outputs/"):
    # Define mapping between checkboxes and their corresponding uncertainty models
    models = [
        {"checkbox": checkboxes[0], "model": "AbrahamsonEtAl2014"},      # self.checkBox
        {"checkbox": checkboxes[1], "model": "BooreEtAl2014"},           # self.checkBox_2
        {"checkbox": checkboxes[2], "model": "CampbellBozorgnia2014"},   # self.checkBox_3
        {"checkbox": checkboxes[3], "model": "ChiouYoungs2014"},         # self.checkBox_4
        {"checkbox": checkboxes[4], "model": "YoungsEtAl1997"},          # self.checkBox_5
        {"checkbox": checkboxes[5], "model": "Atkinson2015"},            # self.checkBox_6
        {"checkbox": checkboxes[6], "model": "AtkinsonBoore2003"},       # self.checkBox_7
        {"checkbox": checkboxes[7], "model": "AtkinsonBoore2006"},       # self.checkBox_8
        {"checkbox": checkboxes[8], "model": "ZhaoEtAl2006S"},           # self.checkBox_9
        {"checkbox": checkboxes[9], "model": "ToroEtAl1997"},            # self.checkBox_10
        # {"checkbox": checkboxes[10], "model": "AkkarEtAl2014"},        # self.checkBox_11 (commented out in the GUI)
        {"checkbox": checkboxes[10], "model": "AkkarBommer2010"},        # self.checkBox_11 (now AkkarBommer2010)
        {"checkbox": checkboxes[11], "model": "AtkinsonBoore2011"},      # self.checkBox_12
        {"checkbox": checkboxes[12], "model": "AkkarEtAl2014Crustal"},   # self.checkBox_13
        {"checkbox": checkboxes[13], "model": "BooreAtkinson2008"},      # self.checkBox_14
        {"checkbox": checkboxes[14], "model": "CampbellBozorgnia2008"},  # self.checkBox_15
        {"checkbox": checkboxes[15], "model": "ChiouYoungs2008"},        # self.checkBox_16
        {"checkbox": checkboxes[16], "model": "ZhaoEtAl2006Crustal"},    # self.checkBox_17
        {"checkbox": checkboxes[17], "model": "Idriss2014"},             # self.checkBox_18
        {"checkbox": checkboxes[18], "model": "McVerryEtAl2006"},        # self.checkBox_19
        {"checkbox": checkboxes[19], "model": "Bradley2010"},            # self.checkBox_20
        {"checkbox": checkboxes[20], "model": "SilvaEtAl2002"}           # self.checkBox_21
    ]

    # Filter only selected models
    selected_models = [model for model in models if model["checkbox"].isChecked()]

    # Calculate weight for each selected model (equally distributed)
    num_selected_models = len(selected_models)
    if num_selected_models > 0:
        weight = 1 / num_selected_models
    else:
        print("No GMPE models selected.")
        return

    # Start building the XML string
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<nrml xmlns:gml="http://www.opengis.net/gml"
      xmlns="http://openquake.org/xmlns/nrml/0.4">
    <logicTree logicTreeID="lt1">

        <logicTreeBranchingLevel branchingLevelID="bl1">
            <logicTreeBranchSet uncertaintyType="gmpeModel" branchSetID="bs1"
                    applyToTectonicRegionType="Active Shallow Crust">
'''

    # Add branches for selected checkboxes with equal weights
    branch_id = 1
    for model_info in selected_models:
        model = model_info["model"]
        xml_content += f'''
                <logicTreeBranch branchID="b{branch_id}">
                    <uncertaintyModel>{model}</uncertaintyModel>
                    <uncertaintyWeight>{weight:.6f}</uncertaintyWeight>
                </logicTreeBranch>'''
        branch_id += 1

    # Close the XML structure
    xml_content += '''
            </logicTreeBranchSet>
        </logicTreeBranchingLevel>

    </logicTree>
</nrml>'''

    # Save the XML content to the output directory, overwriting if exists
    os.makedirs(output_directory, exist_ok=True)
    with open(os.path.join(output_directory, "gmpe_logic_tree.xml"), "w") as f:  # 'w' mode for overwrite
        f.write(xml_content)

    print(f"GMPE XML file generated successfully in {output_directory}")




def source_model_logic_tree(faults, output_directory):
    """
    Generates an OpenQuake source model logic tree XML file, including all fault names in the 'uncertaintyModel' section.

    Args:
        faults (dict): Dictionary of faults where keys are fault names.
        output_directory (str): Directory where the XML file should be saved.
    """
    # Start building the XML content
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<nrml xmlns:gml="http://www.opengis.net/gml"
      xmlns="http://openquake.org/xmlns/nrml/0.4">
  <logicTree logicTreeID="lt1">
    <logicTreeBranchSet uncertaintyType="sourceModel"
                        branchSetID="bs1">
      <logicTreeBranch branchID="b1">
        <uncertaintyModel>\n'''

    # Add the fault names from the dictionary into the 'uncertaintyModel' section
    for fault_name in faults.keys():
        xml_content += f'./Sources/{fault_name}.xml\n'

    # Close the uncertainty model and the rest of the XML
    xml_content += '''        </uncertaintyModel>
        <uncertaintyWeight>1.0</uncertaintyWeight>
      </logicTreeBranch>
    </logicTreeBranchSet>
  </logicTree>
</nrml>'''

    # Save the XML content to the output directory, overwriting if exists
    os.makedirs(output_directory, exist_ok=True)
    with open(os.path.join(output_directory, "source_model_logic_tree.xml"), "w") as f:
        f.write(xml_content)

    print(f"Source model logic tree XML generated successfully in {output_directory}")






def get_output_directory(self):
    folder_name = self.textEdit_13.toPlainText().strip()  # Get the user input for folder name
    if folder_name:
        output_dir = f"./{folder_name}/FQSHA_project/Hazard_Output/"
    else:
        output_dir = f"./{self.Project_foldername}/Hazard_Output/"

    # Create the Hazard_Output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    return output_dir



# This function generates the job.ini file
def generate_job_ini(self, output_directory):
    # Fetch input values from the GUI
    min_lat = self.textEdit_7.toPlainText().strip()
    max_lat = self.textEdit_2.toPlainText().strip()
    min_lon = self.textEdit_5.toPlainText().strip()
    max_lon = self.textEdit_6.toPlainText().strip()
    grid_spacing = self.textEdit_10.toPlainText().strip()
    vs30 = self.textEdit_9.toPlainText().strip()

    # Get calculation mode from the combo box
    calculation_mode = self.comboBox_2.currentText()

    # Use the directory containing gmpe_logic_tree.xml for export_dir
    gmpe_logic_tree_path = os.path.join(output_directory, "gmpe_logic_tree.xml")
    export_dir = output_directory  # Set the output directory

    # Create the job.ini content
    ini_content = f"""[general]
description = Fault_based Hazard
calculation_mode = {calculation_mode}

[geometry]
region = {min_lon} {max_lat}, {max_lon} {max_lat}, {max_lon} {min_lat}, {min_lon} {min_lat}
region_grid_spacing = {grid_spacing}

[logic_tree]
number_of_logic_tree_samples = 1

[erf]
rupture_mesh_spacing = 0.4
width_of_mfd_bin = 0.1
area_source_discretization = 1

[site_params]
reference_vs30_value = {vs30}
reference_vs30_type = inferred
reference_depth_to_2pt5km_per_sec = 2.0
reference_depth_to_1pt0km_per_sec = 100.0

[Calculation parameters]
source_model_logic_tree_file = source_model_logic_tree.xml
gsim_logic_tree_file = gmpe_logic_tree.xml
intensity_measure_types_and_levels = {{'PGA': [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]}}
truncation_level = 5
maximum_distance = 250
number_of_ground_motion_fields = 0
investigation_time = 50

[output]
export_dir = {export_dir}
individual_curves = true
mean_hazard_curves = true
quantile_hazard_curves = 0.05 0.5 0.95
uniform_hazard_spectra = true
hazard_maps = true
poes = 0.02, 0.1
"""

    # Save the ini file in the output directory
    ini_file_path = os.path.join(output_directory, "job.ini")
    with open(ini_file_path, "w") as f:
        f.write(ini_content)

    print(f"job.ini file generated successfully in {output_directory}")