#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_fda_safety_signals
Analyzes FDA safety signals for drugs.
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
        description='Analyzes FDA safety signals for drugs'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    drug_list = input_data.get('drug_list')
    comparison_period = input_data.get('comparison_period')
    signal_threshold = input_data.get('signal_threshold', 2.0)

    if not drug_list:
        raise ValueError("Missing required parameter: drug_list")

    # Convert comparison_period to tuple if it's a list
    if comparison_period and isinstance(comparison_period, list):
        comparison_period = tuple(comparison_period)

    # Import after dependencies are installed
    from biomni.tool.pharmacology import analyze_fda_safety_signals

    result = analyze_fda_safety_signals(
        drug_list=drug_list,
        comparison_period=comparison_period,
        signal_threshold=signal_threshold
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'safety_signals_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
