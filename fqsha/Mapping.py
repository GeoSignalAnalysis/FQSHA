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
# FQSHA - Fault-based Seismic Hazard Assessment Toolkit
# Copyright (C) 2025 Tavakolizadeh et al., (2025)
# License: GNU Affero General Public License v3.0+

import pandas as pd
import pygmt
import json
import os
import glob
import re

def get_largest_hazard_map_csv(directory):
    """Finds the hazard_map-mean_*.csv file with the largest numeric suffix."""
    pattern = os.path.join(directory, "hazard_map-mean_*.csv")
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError("No hazard_map-mean_*.csv files found.")

    def extract_number(f):
        match = re.search(r"hazard_map-mean_(\d+)\.csv", os.path.basename(f))
        return int(match.group(1)) if match else -1

    best_file = max(files, key=extract_number)
    return best_file

def create_contour_map_with_faults(csv_file, fault_file, output_directory):
    # Load CSV data, skipping the header line
    data = pd.read_csv(csv_file, header=None, skiprows=1, names=["longitude", "latitude", "PGA-0.02", "PGA-0.1"])

    # Ensure longitude, latitude, and values are numeric
    data = data.dropna(subset=["longitude", "latitude", "PGA-0.02", "PGA-0.1"])
    data["longitude"] = pd.to_numeric(data["longitude"], errors='coerce')
    data["latitude"] = pd.to_numeric(data["latitude"], errors='coerce')
    data["PGA-0.02"] = pd.to_numeric(data["PGA-0.02"], errors='coerce')
    data["PGA-0.1"] = pd.to_numeric(data["PGA-0.1"], errors='coerce')
    data = data.dropna(subset=["longitude", "latitude", "PGA-0.02", "PGA-0.1"])

    # Define plotting region
    region = [
        round(data['longitude'].min(), 2),
        round(data['longitude'].max(), 2),
        round(data['latitude'].min(), 2),
        round(data['latitude'].max(), 2)
    ]

    # Load faults from JSON
    with open(fault_file, 'r') as f:
        fault_data = json.load(f)

    # Generate plots for both PGA levels
    for column_index, column_name in [(2, "PGA-0.02"), (3, "PGA-0.1")]:
        fig = pygmt.Figure()

        grid = pygmt.sphinterpolate(
            data=data[['longitude', 'latitude', data.columns[column_index]]],
            region=region,
            spacing=0.05
        )

        fig.basemap(region=region, projection="M6i", frame=True)
        fig.coast(shorelines=True, water="skyblue", land="gray")
        fig.grdimage(grid=grid, cmap="jet")
        fig.grdcontour(grid=grid, annotation="1+f8p", pen="black")
        fig.colorbar(position="JMR+o0.5c/0c+w10c", frame='af+l"PGA (g)"')

        for fault_name, fault_info in fault_data.items():
            fault_trace = fault_info['fault_trace']
            fig.plot(
                x=[pt[0] for pt in fault_trace],
                y=[pt[1] for pt in fault_trace],
                pen="1p,black"
            )
            mid_index = len(fault_trace) // 2
            fig.text(
                x=fault_trace[mid_index][0],
                y=fault_trace[mid_index][1],
                text=fault_name,
                font="12p,Helvetica-Bold,black",
                justify="LB"
            )

        output_filename = os.path.join(output_directory, f"contour_with_faults_{column_name}.pdf")
        fig.savefig(output_filename)
        print(f"Map saved: {output_filename}")
        fig.show()

def create_map_from_largest_result(hazard_map_dir, fault_file, output_directory):
    csv_file = get_largest_hazard_map_csv(hazard_map_dir)
    print(f"Using most complete result: {csv_file}")
    create_contour_map_with_faults(csv_file, fault_file, output_directory)

# Example usage:
# create_map_from_largest_result(
#     "/home/aori/PycharmProjects/FQSHA_Review/FQSHA/fqsha/FQSHA_output/OutPut",
#     "input_data/faults.json",
#     "output_maps"
# )
