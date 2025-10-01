#!/usr/bin/env python3
"""
Camber app wrapper for analyze_bacterial_growth_rate from biomni.tool.synthetic_biology
"""

import argparse
import sys
import json
import os
import subprocess


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze bacterial growth rate from OD measurements'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.synthetic_biology import analyze_bacterial_growth_rate

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    time_points = input_data.get("time_points")
    od_measurements = input_data.get("od_measurements")
    strain_name = input_data.get("strain_name", "Unknown strain")
    output_dir = input_data.get("output_dir", "./")

    # Call the function
    result = analyze_bacterial_growth_rate(
        time_points=time_points,
        od_measurements=od_measurements,
        strain_name=strain_name,
        output_dir=output_dir
    )

    # Write result to file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'bacterial_growth_analysis.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
