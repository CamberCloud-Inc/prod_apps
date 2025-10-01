#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.estimate_alpha_particle_radiotherapy_dosimetry
Estimates alpha particle radiotherapy dosimetry.
"""

import argparse
import sys
import subprocess
import os
import json


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Estimates alpha particle radiotherapy dosimetry'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    biodistribution_data = input_data.get('biodistribution_data')
    radiation_parameters = input_data.get('radiation_parameters')
    output_file = input_data.get('output_file', 'dosimetry_results.csv')

    if not biodistribution_data or not radiation_parameters:
        raise ValueError("Missing required parameters: biodistribution_data, radiation_parameters")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import estimate_alpha_particle_radiotherapy_dosimetry

    result = estimate_alpha_particle_radiotherapy_dosimetry(
        biodistribution_data=biodistribution_data,
        radiation_parameters=radiation_parameters,
        output_file=output_file
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'dosimetry_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
