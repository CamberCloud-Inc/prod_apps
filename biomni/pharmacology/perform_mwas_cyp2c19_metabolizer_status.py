#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.perform_mwas_cyp2c19_metabolizer_status
Performs methylation-wide association study (MWAS) for CYP2C19 metabolizer status.
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
        description='Performs methylation-wide association study (MWAS) for CYP2C19 metabolizer status'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    methylation_data_path = input_data.get('methylation_data_path')
    metabolizer_status_path = input_data.get('metabolizer_status_path')
    covariates_path = input_data.get('covariates_path')
    pvalue_threshold = input_data.get('pvalue_threshold', 0.05)
    output_file = input_data.get('output_file', 'significant_cpg_sites.csv')

    if not methylation_data_path or not metabolizer_status_path:
        raise ValueError("Missing required parameters: methylation_data_path, metabolizer_status_path")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import perform_mwas_cyp2c19_metabolizer_status

    result = perform_mwas_cyp2c19_metabolizer_status(
        methylation_data_path=methylation_data_path,
        metabolizer_status_path=metabolizer_status_path,
        covariates_path=covariates_path,
        pvalue_threshold=pvalue_threshold,
        output_file=output_file
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'mwas_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
