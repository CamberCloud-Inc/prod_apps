#!/usr/bin/env python3
"""
Analyze Endolysosomal Calcium Dynamics

Analyze calcium dynamics in endo-lysosomal compartments using ELGA/ELGA1 probe data.
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
        description='Analyze Endolysosomal Calcium Dynamics'
    )
    parser.add_argument('input_file', help='Input JSON file with time_points, luminescence_values and optional parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_endolysosomal_calcium_dynamics

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    time_points = inputs['time_points']
    luminescence_values = inputs['luminescence_values']
    treatment_time = inputs.get('treatment_time')
    cell_type = inputs.get('cell_type', '')
    treatment_name = inputs.get('treatment_name', '')
    output_file = inputs.get('output_file', 'calcium_analysis_results.txt')

    result = analyze_endolysosomal_calcium_dynamics(
        time_points=time_points,
        luminescence_values=luminescence_values,
        treatment_time=treatment_time,
        cell_type=cell_type,
        treatment_name=treatment_name,
        output_file=output_file
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'calcium_dynamics_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
