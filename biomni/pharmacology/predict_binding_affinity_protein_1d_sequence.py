#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.predict_binding_affinity_protein_1d_sequence
Predicts protein-ligand binding affinity.
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
        description='Predicts protein-ligand binding affinity'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    smiles_list = input_data.get('smiles_list')
    amino_acid_sequence = input_data.get('amino_acid_sequence')
    affinity_model_type = input_data.get('affinity_model_type', 'MPNN-CNN')

    if not smiles_list or not amino_acid_sequence:
        raise ValueError("Missing required parameters: smiles_list, amino_acid_sequence")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import predict_binding_affinity_protein_1d_sequence

    result = predict_binding_affinity_protein_1d_sequence(
        smiles_list=smiles_list,
        amino_acid_sequence=amino_acid_sequence,
        affinity_model_type=affinity_model_type
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'binding_affinity_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
