#!/usr/bin/env python3
"""
Camber app wrapper for analyze_bifurcation_diagram from biomni.tool.synthetic_biology
"""

import argparse
import sys
import json
import os
import subprocess
import numpy as np


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze bifurcation diagram for dynamical systems'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.synthetic_biology import analyze_bifurcation_diagram

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    time_series_data = np.array(input_data.get("time_series_data"))
    parameter_values = np.array(input_data.get("parameter_values"))
    system_name = input_data.get("system_name", "Dynamical System")
    output_dir = input_data.get("output_dir", "./")

    # Call the function
    result = analyze_bifurcation_diagram(
        time_series_data=time_series_data,
        parameter_values=parameter_values,
        system_name=system_name,
        output_dir=output_dir
    )

    # Write result to file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'bifurcation_analysis.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
