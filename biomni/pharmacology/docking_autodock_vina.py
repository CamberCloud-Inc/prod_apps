#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.docking_autodock_vina
Performs docking using AutoDock Vina with specified parameters.
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
        description='Performs docking using AutoDock Vina'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    smiles_list = input_data.get('smiles_list')
    receptor_pdb_file = input_data.get('receptor_pdb_file')
    box_center = input_data.get('box_center')
    box_size = input_data.get('box_size')
    ncpu = input_data.get('ncpu', 1)

    if not smiles_list or not receptor_pdb_file or not box_center or not box_size:
        raise ValueError("Missing required parameters: smiles_list, receptor_pdb_file, box_center, box_size")

    # Convert to tuple if needed
    box_center = tuple(box_center) if isinstance(box_center, list) else box_center
    box_size = tuple(box_size) if isinstance(box_size, list) else box_size

    # Import after dependencies are installed
    from biomni.tool.pharmacology import docking_autodock_vina

    result = docking_autodock_vina(
        smiles_list=smiles_list,
        receptor_pdb_file=receptor_pdb_file,
        box_center=box_center,
        box_size=box_size,
        ncpu=ncpu
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'docking_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
