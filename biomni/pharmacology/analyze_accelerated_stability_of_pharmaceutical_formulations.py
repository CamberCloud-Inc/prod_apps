#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_accelerated_stability_of_pharmaceutical_formulations
Analyzes accelerated stability of pharmaceutical formulations.
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
        description='Analyzes accelerated stability of pharmaceutical formulations'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    formulations = input_data.get('formulations')
    storage_conditions = input_data.get('storage_conditions')
    time_points = input_data.get('time_points')

    if not formulations or not storage_conditions or not time_points:
        raise ValueError("Missing required parameters: formulations, storage_conditions, time_points")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import analyze_accelerated_stability_of_pharmaceutical_formulations

    result = analyze_accelerated_stability_of_pharmaceutical_formulations(
        formulations=formulations,
        storage_conditions=storage_conditions,
        time_points=time_points
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'stability_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
