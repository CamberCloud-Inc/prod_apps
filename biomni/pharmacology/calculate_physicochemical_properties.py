#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.calculate_physicochemical_properties
Calculates physicochemical properties of molecules.
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
        description='Calculates physicochemical properties of molecules'
    )
    parser.add_argument('--smiles-string', required=True, help='SMILES representation of the molecule')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Get parameter
    smiles_string = args.smiles_string

    # Import after dependencies are installed
    from biomni.tool.pharmacology import calculate_physicochemical_properties

    result = calculate_physicochemical_properties(
        smiles_string=smiles_string
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'physicochemical_properties_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
