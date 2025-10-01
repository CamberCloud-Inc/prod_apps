#!/usr/bin/env python3
"""
Perform Cosinor Analysis

Performs cosinor analysis on physiological time series data to characterize circadian rhythms.
"""

import argparse
import sys
import json
import os
import subprocess


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Perform Cosinor Analysis'
    )
    parser.add_argument('--time-data-file', required=True, help='File containing time points (JSON array or CSV)')
    parser.add_argument('--physiological-data-file', required=True, help='File containing physiological measurements (JSON array or CSV)')
    parser.add_argument('--period', type=float, default=24.0, help='Expected period in hours (default: 24.0)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import perform_cosinor_analysis

    # Load time_data from file
    with open(args.time_data_file, 'r') as f:
        if args.time_data_file.endswith('.json'):
            time_data = json.load(f)
        else:  # Assume CSV
            time_data = [float(line.strip()) for line in f if line.strip()]

    # Load physiological_data from file
    with open(args.physiological_data_file, 'r') as f:
        if args.physiological_data_file.endswith('.json'):
            physiological_data = json.load(f)
        else:  # Assume CSV
            physiological_data = [float(line.strip()) for line in f if line.strip()]

    result = perform_cosinor_analysis(
        time_data=time_data,
        physiological_data=physiological_data,
        period=args.period
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cosinor_analysis_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
