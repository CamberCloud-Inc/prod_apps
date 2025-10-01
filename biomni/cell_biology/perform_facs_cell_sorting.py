#!/usr/bin/env python3
"""
Camber wrapper for perform_facs_cell_sorting from Biomni
"""

import argparse
import json
import os
import sys




def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Perform FACS cell sorting'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cell_biology import perform_facs_cell_sorting

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    cell_suspension_data = input_data.get("cell_suspension_data", "")
    fluorescence_parameter = input_data.get("fluorescence_parameter", "")
    threshold_min = input_data.get("threshold_min")
    threshold_max = input_data.get("threshold_max")
    output_file = input_data.get("output_file", "sorted_cells.csv")

    # Call the function
    result = perform_facs_cell_sorting(
        cell_suspension_data=cell_suspension_data,
        fluorescence_parameter=fluorescence_parameter,
        threshold_min=threshold_min,
        threshold_max=threshold_max,
        output_file=output_file
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'result.json')

    output = {
        "research_log": result
    }

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
