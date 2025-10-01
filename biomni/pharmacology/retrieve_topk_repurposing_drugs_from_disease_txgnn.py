#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.retrieve_topk_repurposing_drugs_from_disease_txgnn
Predicts top K drug repurposing candidates for a given disease using TxGNN.
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
        description='Predicts top K drug repurposing candidates for a given disease using TxGNN'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    disease_name = input_data.get('disease_name')
    data_lake_path = input_data.get('data_lake_path')
    k = input_data.get('k', 5)

    if not disease_name or not data_lake_path:
        raise ValueError("Missing required parameters: disease_name, data_lake_path")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import retrieve_topk_repurposing_drugs_from_disease_txgnn

    result = retrieve_topk_repurposing_drugs_from_disease_txgnn(
        disease_name=disease_name,
        data_lake_path=data_lake_path,
        k=k
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'drug_repurposing_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
