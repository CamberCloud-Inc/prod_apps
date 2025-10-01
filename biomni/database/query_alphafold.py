#!/usr/bin/env python3
"""
Biomni Tool: Query AlphaFold
Wraps: biomni.tool.database.query_alphafold
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
        description='Query the AlphaFold Database API for protein structure predictions'
    )
    parser.add_argument('input_file', help='JSON file with parameters from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    from biomni.tool.database import query_alphafold

    result = query_alphafold(
        uniprot_id=input_data.get('uniprot_id'),
        endpoint=input_data.get('endpoint', 'prediction'),
        residue_range=input_data.get('residue_range'),
        download=input_data.get('download', False),
        output_dir=input_data.get('output_dir'),
        file_format=input_data.get('file_format', 'pdb'),
        model_version=input_data.get('model_version', 'v4'),
        model_number=input_data.get('model_number', 1)
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'alphafold_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
