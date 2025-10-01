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
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze Hemodynamic Data'
    )
    parser.add_argument('input_file', help='Input JSON file with pressure_data and sampling_rate')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_hemodynamic_data

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    pressure_data = inputs['pressure_data']
    sampling_rate = inputs['sampling_rate']
    output_file = inputs.get('output_file', 'hemodynamic_results.csv')

    result = analyze_hemodynamic_data(
        pressure_data=pressure_data,
        sampling_rate=sampling_rate,
        output_file=output_file
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'hemodynamic_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
