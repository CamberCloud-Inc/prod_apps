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
    parser.add_argument('input_file', help='Input JSON file with time_data, physiological_data and optional period')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import perform_cosinor_analysis

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    time_data = inputs['time_data']
    physiological_data = inputs['physiological_data']
    period = inputs.get('period', 24.0)

    result = perform_cosinor_analysis(
        time_data=time_data,
        physiological_data=physiological_data,
        period=period
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cosinor_analysis_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
