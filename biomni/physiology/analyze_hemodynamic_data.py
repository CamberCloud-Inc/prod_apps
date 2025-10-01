#!/usr/bin/env python3
"""
Analyze Hemodynamic Data

Analyzes raw blood pressure data to calculate key hemodynamic parameters.
"""

import argparse
import sys
import json
import os
import subprocess


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni', 'scipy']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze Hemodynamic Data'
    )
    parser.add_argument('--pressure-data-file', required=True, help='File containing blood pressure values in mmHg (JSON array or CSV)')
    parser.add_argument('--sampling-rate', type=float, required=True, help='Sampling frequency of the pressure recording in Hz')
    parser.add_argument('--output-file', default='hemodynamic_results.csv', help='Name for output file (default: hemodynamic_results.csv)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_hemodynamic_data

    # Load pressure data from file
    with open(args.pressure_data_file, 'r') as f:
        if args.pressure_data_file.endswith('.json'):
            pressure_data = json.load(f)
        else:  # Assume CSV
            pressure_data = [float(line.strip()) for line in f if line.strip()]

    result = analyze_hemodynamic_data(
        pressure_data=pressure_data,
        sampling_rate=args.sampling_rate,
        output_file=args.output_file
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'hemodynamic_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
