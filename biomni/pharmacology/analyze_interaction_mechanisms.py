#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_interaction_mechanisms
Analyzes drug-drug interaction mechanisms.
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
        description='Analyzes drug-drug interaction mechanisms'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    drug_pair = input_data.get('drug_pair')
    detailed_analysis = input_data.get('detailed_analysis', True)
    data_lake_path = input_data.get('data_lake_path')

    if not drug_pair:
        raise ValueError("Missing required parameter: drug_pair")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import analyze_interaction_mechanisms

    result = analyze_interaction_mechanisms(
        drug_pair=drug_pair,
        detailed_analysis=detailed_analysis,
        data_lake_path=data_lake_path
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'interaction_mechanisms_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
