#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.find_alternative_drugs_ddinter
Finds alternative drugs to avoid contraindicated interactions.
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
        description='Finds alternative drugs to avoid contraindicated interactions'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    target_drug = input_data.get('target_drug')
    contraindicated_drugs = input_data.get('contraindicated_drugs')
    therapeutic_class = input_data.get('therapeutic_class')
    data_lake_path = input_data.get('data_lake_path')

    if not target_drug or not contraindicated_drugs:
        raise ValueError("Missing required parameters: target_drug, contraindicated_drugs")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import find_alternative_drugs_ddinter

    result = find_alternative_drugs_ddinter(
        target_drug=target_drug,
        contraindicated_drugs=contraindicated_drugs,
        therapeutic_class=therapeutic_class,
        data_lake_path=data_lake_path
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'alternative_drugs_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
