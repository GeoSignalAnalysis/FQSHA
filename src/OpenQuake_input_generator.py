import os


def gmpe_generate_xml(inputs, output_directory):
    checkboxes = [
        inputs['AbrahamsonEtAl2014'],
        inputs['BooreEtAl2014'],
        inputs['CampbellBozorgnia2014'],
        inputs['ChiouYoungs2014'],
        inputs['YoungsEtAl1997SSlab'],
        inputs['Atkinson2015'],
        inputs['AtkinsonBoore2003SInter'],
        inputs['AtkinsonBoore2006'],
        inputs['AbrahamsonEtAl2018SInter'],
        inputs['ToroEtAl1997'],
        inputs['AkkarBommer2010'],
        inputs['AbrahamsonEtAl2015SSlab'],
        inputs['AkkarEtAlRepi2014'],
        inputs['BooreAtkinson2008'],
        inputs['CampbellBozorgnia2008'],
        inputs['ChiouYoungs2008'],
        inputs['ZhaoEtAl2016Asc'],
        inputs['Idriss2014'],
        inputs['McVerryEtAl2006'],
        inputs['Bradley2010'],
        inputs['SilvaEtAl2002'],
        inputs['AkkarEtAlRjb2014']
    ]

    models = [
        "AbrahamsonEtAl2014", "BooreEtAl2014", "CampbellBozorgnia2014", "ChiouYoungs2014",
        "YoungsEtAl1997SSlab", "Atkinson2015", "AtkinsonBoore2003SInter", "AtkinsonBoore2006",
        "AbrahamsonEtAl2018SInter", "ToroEtAl1997", "AkkarBommer2010", "AbrahamsonEtAl2015SSlab",
        "AkkarEtAlRepi2014", "BooreAtkinson2008", "CampbellBozorgnia2008",
        "ChiouYoungs2008", "ZhaoEtAl2016Asc", "Idriss2014", "McVerryEtAl2006",
        "Bradley2010", "SilvaEtAl2002", "AkkarEtAlRjb2014",
    ]

    # Filter only selected models
    selected_models = [model for model, checked in zip(models, checkboxes) if checked]

    # Calculate weight for each selected model (equally distributed)
    num_selected_models = len(selected_models)
    if num_selected_models > 0:
        base_weight = round(1 / num_selected_models, 6)
    else:
        print("No GMPE models selected.")
        return

    # Start building the XML string
    xml_gmpe = '''<?xml version="1.0" encoding="UTF-8"?>
<nrml xmlns:gml="http://www.opengis.net/gml"
      xmlns="http://openquake.org/xmlns/nrml/0.4">
    <logicTree logicTreeID="lt1">

        <logicTreeBranchingLevel branchingLevelID="bl1">
            <logicTreeBranchSet uncertaintyType="gmpeModel" branchSetID="bs1"
                    applyToTectonicRegionType="Active Shallow Crust">
'''

    # Add branches for selected checkboxes with equal weights
    branch_id = 1
    total_weight = 0  # Track the total weight
    for i, model in enumerate(selected_models):
        # Adjust the weight of the last model to make the total exactly 1.0
        if i == num_selected_models - 1:
            weight = round(1.0 - total_weight, 6)
        else:
            weight = base_weight
            total_weight += weight

        xml_gmpe += f'''
                <logicTreeBranch branchID="b{branch_id}">
                    <uncertaintyModel>{model}</uncertaintyModel>
                    <uncertaintyWeight>{weight:.6f}</uncertaintyWeight>
                </logicTreeBranch>'''
        branch_id += 1

    # Close the XML structure
    xml_gmpe += '''
            </logicTreeBranchSet>
        </logicTreeBranchingLevel>

    </logicTree>
</nrml>'''

    # Ensure the output directory exists
    try:
        os.makedirs(output_directory, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory: {e}")
        return

    # Save the XML content to the output directory, overwriting if exists
    with open(os.path.join(output_directory, "gmpe_logic_tree.xml"), "w") as f:
        f.write(xml_gmpe)

    print(f"GMPE XML file generated successfully in {output_directory}")




def source_model_logic_tree(faults, output_directory):
    """
    Generates an OpenQuake source model logic tree XML file, including all fault names in the 'uncertaintyModel' section.

    Args:
        faults (dict): Dictionary of faults where keys are fault names.
        output_directory (str): Directory where the XML file should be saved.
    """
    # Start building the XML content
    xml_source_model = '''<?xml version="1.0" encoding="UTF-8"?>
<nrml xmlns:gml="http://www.opengis.net/gml"
      xmlns="http://openquake.org/xmlns/nrml/0.4">
  <logicTree logicTreeID="lt1">
    <logicTreeBranchSet uncertaintyType="sourceModel"
                        branchSetID="bs1">
      <logicTreeBranch branchID="b1">
        <uncertaintyModel>\n'''

    # Add the fault names from the dictionary into the 'uncertaintyModel' section
    for fault_name in faults.keys():
        xml_source_model += f'./Sources/{fault_name}.xml\n'

    # Close the uncertainty model and the rest of the XML
    xml_source_model += '''        </uncertaintyModel>
        <uncertaintyWeight>1.0</uncertaintyWeight>
      </logicTreeBranch>
    </logicTreeBranchSet>
  </logicTree>
</nrml>'''

    # Ensure the output directory exists, and save the XML content to the output directory
    os.makedirs(output_directory, exist_ok=True)
    with open(os.path.join(output_directory, "source_model_logic_tree.xml"), "w") as f:  # 'w' mode for overwrite
        f.write(xml_source_model)
    print(f"GMPE XML file generated successfully in {output_directory} as source_model_logic_tree.xml")


#
# def generate_job_ini(inputs, output_directory):
#     job_ini_content = f"""[general]
# description = Fault.PSHA
# calculation_mode = {inputs['comboBox_2']}
#
# [geometry]
# region = {inputs['textEdit_5']} {inputs['textEdit_2']}, {inputs['textEdit_6']} {inputs['textEdit_2']}, {inputs['textEdit_6']} {inputs['textEdit_7']}, {inputs['textEdit_5']} {inputs['textEdit_7']}
# region_grid_spacing = {inputs['textEdit_10']}
#
# [logic_tree]
# number_of_logic_tree_samples = 1
#
# [erf]
# rupture_mesh_spacing = 0.4
# width_of_mfd_bin = 0.1
# area_source_discretization = 1
#
# [site_params]
# reference_vs30_value = {inputs['textEdit_9']}
# reference_vs30_type = inferred
# reference_depth_to_2pt5km_per_sec = 2.0
# reference_depth_to_1pt0km_per_sec = 100.0
#
# [Calculation parameters]
# source_model_logic_tree_file = source_model_logic_tree.xml
# gsim_logic_tree_file = gmpe_logic_tree.xml
# intensity_measure_types_and_levels = {{"PGA": [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]}}
# truncation_level = 5
# maximum_distance = 250
# number_of_ground_motion_fields = 0
# investigation_time = 50
#
# [output]
#
# export_dir = {os.path.join(output_directory, "OutPut")}
# individual_curves = true
# mean_hazard_curves = true
# quantile_hazard_curves = 0.05 0.5 0.95
# uniform_hazard_spectra = true
# hazard_maps = true
# poes = 0.02, 0.1
# """
#
#     # Save the job.ini content to the output directory, overwriting if exists
#     os.makedirs(output_directory, exist_ok=True)
#     with open(os.path.join(output_directory, "job.ini"), "w") as f:
#         f.write(job_ini_content)
#
#     print(f"job.ini file generated successfully in {output_directory}")



# import os
#
# def calculate_bounds_from_fault_trace(faults):
#     min_lat, max_lat = float('inf'), float('-inf')
#     min_lon, max_lon = float('inf'), float('-inf')
#
#     for fault_name, fault_data in faults.items():
#         fault_trace = fault_data.get('fault_trace', [])
#         for lon, lat in fault_trace:  # Adjusting order if necessary
#             min_lat = min(min_lat, lat)
#             max_lat = max(max_lat, lat)
#             min_lon = min(min_lon, lon)
#             max_lon = max(max_lon, lon)
#
#     # Rounding to integers
#     return round(min_lat), round(max_lat), round(min_lon), round(max_lon)
#
# def generate_job_ini(inputs, output_directory, faults):
#     # Calculate bounds if text edits are not filled
#     min_lat = inputs['textEdit_7'] or calculate_bounds_from_fault_trace(faults)[0]
#     max_lat = inputs['textEdit_2'] or calculate_bounds_from_fault_trace(faults)[1]
#     min_lon = inputs['textEdit_5'] or calculate_bounds_from_fault_trace(faults)[2]
#     max_lon = inputs['textEdit_6'] or calculate_bounds_from_fault_trace(faults)[3]
#
#     # Ensuring the coordinates are formatted as integers for the job.ini file
#     region_coordinates = f"{min_lon} {max_lat}, {max_lon} {max_lat}, {max_lon} {min_lat}, {min_lon} {min_lat}"
#
#     # Create job.ini content
#     job_ini_content = f"""[general]
# description = Fault.PSHA
# calculation_mode = {inputs['comboBox_2']}
#
# [geometry]
# region = {region_coordinates}
# region_grid_spacing = {inputs['textEdit_10']}
#
# [logic_tree]
# number_of_logic_tree_samples = 1
#
# [erf]
# rupture_mesh_spacing = 0.4
# width_of_mfd_bin = 0.1
# area_source_discretization = 1
#
# [site_params]
# reference_vs30_value = {inputs['textEdit_9']}
# reference_vs30_type = inferred
# reference_depth_to_2pt5km_per_sec = 2.0
# reference_depth_to_1pt0km_per_sec = 100.0
#
# [Calculation parameters]
# source_model_logic_tree_file = source_model_logic_tree.xml
# gsim_logic_tree_file = gmpe_logic_tree.xml
# intensity_measure_types_and_levels = {{"PGA": [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]}}
# truncation_level = 5
# maximum_distance = 300
# number_of_ground_motion_fields = 0
# investigation_time = 50
#
# [output]
# export_dir = {os.path.join(output_directory, "OutPut")}
# individual_curves = true
# mean_hazard_curves = true
# quantile_hazard_curves = 0.05 0.5 0.95
# uniform_hazard_spectra = true
# hazard_maps = true
# poes = 0.02, 0.1
# """
#
#     # Save the job.ini content to the output directory, overwriting if exists
#     os.makedirs(output_directory, exist_ok=True)
#     with open(os.path.join(output_directory, "job.ini"), "w") as f:
#         f.write(job_ini_content)
#
#     print(f"job.ini file generated successfully in {output_directory}")
#
#
import os

def calculate_bounds_with_padding(faults, padding_factor=0.05):
    min_lat, max_lat = float('inf'), float('-inf')
    min_lon, max_lon = float('inf'), float('-inf')

    for fault_name, fault_data in faults.items():
        fault_trace = fault_data.get('fault_trace', [])
        for lon, lat in fault_trace:
            min_lat = min(min_lat, lat)
            max_lat = max(max_lat, lat)
            min_lon = min(min_lon, lon)
            max_lon = max(max_lon, lon)

    # Calculate padding based on 5% of the latitude and longitude ranges
    lat_range = max_lat - min_lat
    lon_range = max_lon - min_lon

    # Adjust bounds by 5%
    min_lat = round(min_lat - padding_factor * lat_range, 6)
    max_lat = round(max_lat + padding_factor * lat_range, 6)
    min_lon = round(min_lon - padding_factor * lon_range, 6)
    max_lon = round(max_lon + padding_factor * lon_range, 6)

    return min_lat, max_lat, min_lon, max_lon

def generate_job_ini(inputs, output_directory, faults):
    # Calculate bounds if text edits are not filled
    min_lat = inputs['textEdit_7'] or calculate_bounds_with_padding(faults)[0]
    max_lat = inputs['textEdit_2'] or calculate_bounds_with_padding(faults)[1]
    min_lon = inputs['textEdit_5'] or calculate_bounds_with_padding(faults)[2]
    max_lon = inputs['textEdit_6'] or calculate_bounds_with_padding(faults)[3]

    # Ensuring the coordinates are formatted as integers for the job.ini file
    region_coordinates = f"{min_lon} {max_lat}, {max_lon} {max_lat}, {max_lon} {min_lat}, {min_lon} {min_lat}"

    # Create job.ini content
    job_ini_content = f"""[general]
description = Fault.PSHA
calculation_mode = {inputs['comboBox_2']}

[geometry]
region = {region_coordinates}
region_grid_spacing = {inputs['textEdit_10']}

[logic_tree]
number_of_logic_tree_samples = 1

[erf]
rupture_mesh_spacing = 0.4
width_of_mfd_bin = 0.1
area_source_discretization = 1

[site_params]
reference_vs30_value = {inputs['textEdit_9']}
reference_vs30_type = inferred
reference_depth_to_2pt5km_per_sec = 2.0
reference_depth_to_1pt0km_per_sec = 100.0

[Calculation parameters]
source_model_logic_tree_file = source_model_logic_tree.xml
gsim_logic_tree_file = gmpe_logic_tree.xml
intensity_measure_types_and_levels = {{"PGA": [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]}}
truncation_level = 5
maximum_distance = 300
number_of_ground_motion_fields = 0
investigation_time = 50

[output]
export_dir = {os.path.join(output_directory, "OutPut")}
individual_curves = true
mean_hazard_curves = true
quantile_hazard_curves = 0.05 0.5 0.95
uniform_hazard_spectra = true
hazard_maps = true
poes = 0.02, 0.1
"""

    # Save the job.ini content to the output directory, overwriting if exists
    os.makedirs(output_directory, exist_ok=True)
    with open(os.path.join(output_directory, "job.ini"), "w") as f:
        f.write(job_ini_content)

    print(f"job.ini file generated successfully in {output_directory}")
