#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.check_drug_combination_safety
Checks safety of drug combinations.
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
        description='Checks safety of drug combinations'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    drug_list = input_data.get('drug_list')
    include_mechanisms = input_data.get('include_mechanisms', True)
    include_management = input_data.get('include_management', True)
    data_lake_path = input_data.get('data_lake_path')

    if not drug_list:
        raise ValueError("Missing required parameter: drug_list")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import check_drug_combination_safety

    result = check_drug_combination_safety(
        drug_list=drug_list,
        include_mechanisms=include_mechanisms,
        include_management=include_management,
        data_lake_path=data_lake_path
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'drug_combination_safety_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
