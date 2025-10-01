#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.predict_admet_properties
Predicts ADMET properties for a list of compounds.
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
        description='Predicts ADMET properties for a list of compounds'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    smiles_list = input_data.get('smiles_list')
    ADMET_model_type = input_data.get('ADMET_model_type', 'MPNN')

    if not smiles_list:
        raise ValueError("Missing required parameter: smiles_list")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import predict_admet_properties

    result = predict_admet_properties(
        smiles_list=smiles_list,
        ADMET_model_type=ADMET_model_type
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'admet_properties_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
