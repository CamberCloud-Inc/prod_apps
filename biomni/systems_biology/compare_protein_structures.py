#!/usr/bin/env python3
"""
Wrapper for Biomni compare_protein_structures tool
"""
import sys
import argparse
import os
import json


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
        description='Compare protein structures using Biomni'
    )
    parser.add_argument('input_file', help='JSON file with comparison parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    pdb_file1 = input_data.get('pdb_file1')
    pdb_file2 = input_data.get('pdb_file2')
    chain_id1 = input_data.get('chain_id1', 'A')
    chain_id2 = input_data.get('chain_id2', 'A')
    output_prefix = input_data.get('output_prefix', 'protein_comparison')

    # Import after dependencies are installed
    from biomni.tool.systems_biology import compare_protein_structures

    result = compare_protein_structures(pdb_file1, pdb_file2, chain_id1, chain_id2, output_prefix)

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'comparison_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
