#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.query_drug_interactions
Queries drug-drug interactions.
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
        description='Queries drug-drug interactions'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    drug_names = input_data.get('drug_names')
    interaction_types = input_data.get('interaction_types')
    severity_levels = input_data.get('severity_levels')
    data_lake_path = input_data.get('data_lake_path')

    if not drug_names:
        raise ValueError("Missing required parameter: drug_names")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import query_drug_interactions

    result = query_drug_interactions(
        drug_names=drug_names,
        interaction_types=interaction_types,
        severity_levels=severity_levels,
        data_lake_path=data_lake_path
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'drug_interactions_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
