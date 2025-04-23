import pandas as pd
import pygmt
import json
import os

def create_contour_map_with_faults(csv_file, fault_file, output_directory):
    # Load CSV data, skipping the header line
    data = pd.read_csv(csv_file, header=None, skiprows=1, names=["longitude", "latitude", "PGA-0.02", "PGA-0.1"])

    # Ensure longitude, latitude, and values are numeric
    data = data.dropna(subset=["longitude", "latitude", "PGA-0.02", "PGA-0.1"])
    data["longitude"] = pd.to_numeric(data["longitude"], errors='coerce')
    data["latitude"] = pd.to_numeric(data["latitude"], errors='coerce')
    data["PGA-0.02"] = pd.to_numeric(data["PGA-0.02"], errors='coerce')
    data["PGA-0.1"] = pd.to_numeric(data["PGA-0.1"], errors='coerce')

    # Drop rows with invalid longitude, latitude, or values
    data = data.dropna(subset=["longitude", "latitude", "PGA-0.02", "PGA-0.1"])

    # Define the region of interest
    region = [
        round(data['longitude'].min(), 2),
        round(data['longitude'].max(), 2),
        round(data['latitude'].min(), 2),
        round(data['latitude'].max(), 2)
    ]

    # Load fault traces from JSON file
    with open(fault_file, 'r') as f:
        fault_data = json.load(f)

    # Generate maps for both PGA columns
    for column_index, column_name in [(2, "PGA-0.02"), (3, "PGA-0.1")]:
        fig = pygmt.Figure()

        # Create a grid from the data using spherical interpolation
        grid = pygmt.sphinterpolate(
            data=data[['longitude', 'latitude', data.columns[column_index]]],
            region=region,
            spacing=0.05
        )

        # Create map with coastlines, contours, and fault traces
        fig.basemap(region=region, projection="M6i", frame=True)
        fig.coast(shorelines=True, water="skyblue", land="gray")
        fig.grdimage(grid=grid, cmap="jet")
        fig.grdcontour(grid=grid, annotation="1+f8p", pen="black")
        fig.colorbar(frame=f'af+l"{column_name}"', cmap="jet", position="JMR+o1.5c/0c+w12c")

        # Plot fault traces and add labels
        for fault_name, fault_info in fault_data.items():
            fault_trace = fault_info['fault_trace']
            # Plot the fault trace
            fig.plot(
                x=[pt[0] for pt in fault_trace],
                y=[pt[1] for pt in fault_trace],
                pen="1p,black"
            )

            # Add label at the midpoint of the fault trace
            mid_index = len(fault_trace) // 2
            fig.text(
                x=fault_trace[mid_index][0],
                y=fault_trace[mid_index][1],
                text=fault_name,
                font="12p,Helvetica-Bold,black",
                justify="LB"
            )

        fig.show()
        # Save the map
        output_filename = os.path.join(output_directory, f"contour_with_faults_{column_name}.pdf")
        fig.savefig(output_filename)
        print(f"Map saved: {output_filename}")

# Example usage:
# create_contour_map_with_faults("/path/to/csv_file.csv", "/path/to/fault_file.json", "/path/to/output_directory")
