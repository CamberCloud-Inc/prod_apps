#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.run_autosite
Runs AutoSite to identify potential binding sites in a protein.
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
        description='Runs AutoSite to identify potential binding sites in a protein'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    pdb_file = input_data.get('pdb_file')
    output_dir = input_data.get('output_dir')
    spacing = input_data.get('spacing', 1.0)

    if not pdb_file or not output_dir:
        raise ValueError("Missing required parameters: pdb_file, output_dir")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import run_autosite

    result = run_autosite(
        pdb_file=pdb_file,
        output_dir=output_dir,
        spacing=spacing
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'autosite_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
