#!/usr/bin/env python3
"""
Biomni Tool: Query PDB Identifiers
Wraps: biomni.tool.database.query_pdb_identifiers
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Retrieve detailed data for PDB identifiers'
    )
    parser.add_argument('input_file', help='JSON file with parameters from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    from biomni.tool.database import query_pdb_identifiers

    result = query_pdb_identifiers(identifiers=input_data.get('identifiers'),
        return_type=input_data.get('return_type'),
        download=input_data.get('download'),
        attributes=input_data.get('attributes'))

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'pdb_identifiers_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
