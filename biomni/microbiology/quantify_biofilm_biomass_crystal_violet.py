#!/usr/bin/env python3
"""
Quantify biofilm biomass using the crystal violet staining method.
"""

import sys
import json
import argparse
import os



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
        description='Quantify biofilm biomass using the crystal violet staining method.'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import quantify_biofilm_biomass_crystal_violet

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    absorbance_readings = input_data.get('absorbance_readings')
    control_wells = input_data.get('control_wells')
    sample_names = input_data.get('sample_names')

    # Call the function
    result = quantify_biofilm_biomass_crystal_violet(
        absorbance_readings=absorbance_readings,
        control_wells=control_wells,
        sample_names=sample_names
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'biofilm_quantification_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
