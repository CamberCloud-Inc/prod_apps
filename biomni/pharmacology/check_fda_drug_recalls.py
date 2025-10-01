#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.check_fda_drug_recalls
Checks FDA drug recalls database.
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
        description='Checks FDA drug recalls database'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    drug_name = input_data.get('drug_name')
    classification = input_data.get('classification')
    date_range = input_data.get('date_range')

    if not drug_name:
        raise ValueError("Missing required parameter: drug_name")

    # Convert date_range to tuple if it's a list
    if date_range and isinstance(date_range, list):
        date_range = tuple(date_range)

    # Import after dependencies are installed
    from biomni.tool.pharmacology import check_fda_drug_recalls

    result = check_fda_drug_recalls(
        drug_name=drug_name,
        classification=classification,
        date_range=date_range
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'fda_recalls_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
