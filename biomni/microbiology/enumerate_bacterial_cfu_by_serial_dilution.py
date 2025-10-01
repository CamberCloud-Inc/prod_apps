#!/usr/bin/env python3
"""
Quantify bacterial concentration (CFU/mL) using serial dilutions and spot plating.
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
        description='Quantify bacterial concentration (CFU/mL) using serial dilutions and spot plating.'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import enumerate_bacterial_cfu_by_serial_dilution

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    initial_sample_volume_ml = input_data.get('initial_sample_volume_ml', 1.0)
    estimated_concentration = input_data.get('estimated_concentration', 1e8)
    dilution_factor = input_data.get('dilution_factor', 10)
    num_dilutions = input_data.get('num_dilutions', 8)
    spots_per_dilution = input_data.get('spots_per_dilution', 3)
    output_file = input_data.get('output_file', 'cfu_enumeration_results.csv')

    # Call the function
    result = enumerate_bacterial_cfu_by_serial_dilution(
        initial_sample_volume_ml=initial_sample_volume_ml,
        estimated_concentration=estimated_concentration,
        dilution_factor=dilution_factor,
        num_dilutions=num_dilutions,
        spots_per_dilution=spots_per_dilution,
        output_file=output_file
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cfu_enumeration_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
