#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.run_3d_chondrogenic_aggregate_assay
Runs 3D chondrogenic aggregate assay.
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
        description='Runs 3D chondrogenic aggregate assay'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    chondrocyte_cells = input_data.get('chondrocyte_cells')
    test_compounds = input_data.get('test_compounds')
    culture_duration_days = input_data.get('culture_duration_days', 21)
    measurement_intervals = input_data.get('measurement_intervals', 7)

    if not chondrocyte_cells or not test_compounds:
        raise ValueError("Missing required parameters: chondrocyte_cells, test_compounds")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import run_3d_chondrogenic_aggregate_assay

    result = run_3d_chondrogenic_aggregate_assay(
        chondrocyte_cells=chondrocyte_cells,
        test_compounds=test_compounds,
        culture_duration_days=culture_duration_days,
        measurement_intervals=measurement_intervals
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'chondrogenic_assay_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
