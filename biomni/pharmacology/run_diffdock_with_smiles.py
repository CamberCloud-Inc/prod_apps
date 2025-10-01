#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.run_diffdock_with_smiles
Runs DiffDock inference for molecular docking using a Docker container.
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
        description='Runs DiffDock inference for molecular docking using a Docker container'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    pdb_path = input_data.get('pdb_path')
    smiles_string = input_data.get('smiles_string')
    local_output_dir = input_data.get('local_output_dir')
    gpu_device = input_data.get('gpu_device', 0)
    use_gpu = input_data.get('use_gpu', True)

    if not pdb_path or not smiles_string or not local_output_dir:
        raise ValueError("Missing required parameters: pdb_path, smiles_string, local_output_dir")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import run_diffdock_with_smiles

    result = run_diffdock_with_smiles(
        pdb_path=pdb_path,
        smiles_string=smiles_string,
        local_output_dir=local_output_dir,
        gpu_device=gpu_device,
        use_gpu=use_gpu
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'diffdock_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
