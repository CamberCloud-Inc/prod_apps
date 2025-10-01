#!/usr/bin/env python3
"""
Camber wrapper for perform_facs_cell_sorting from Biomni
"""

import json
import sys

from biomni.tool.cell_biology import perform_facs_cell_sorting



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
    
    install_dependencies()
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

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

    # Output result as JSON
    output = {
        "research_log": result
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
