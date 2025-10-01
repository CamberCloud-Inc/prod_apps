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
    parser.add_argument('--time-points-file', required=True, help='File containing time points (JSON array or CSV)')
    parser.add_argument('--luminescence-values-file', required=True, help='File containing luminescence measurements (JSON array or CSV)')
    parser.add_argument('--treatment-time', type=float, help='Time point when treatment was applied (optional)')
    parser.add_argument('--cell-type', default='', help='Type of cells used (optional)')
    parser.add_argument('--treatment-name', default='', help='Name of treatment applied (optional)')
    parser.add_argument('--output-file', default='calcium_analysis_results.txt', help='Output filename (default: calcium_analysis_results.txt)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_endolysosomal_calcium_dynamics

    # Load time_points from file
    with open(args.time_points_file, 'r') as f:
        if args.time_points_file.endswith('.json'):
            time_points = json.load(f)
        else:  # Assume CSV
            time_points = [float(line.strip()) for line in f if line.strip()]

    # Load luminescence_values from file
    with open(args.luminescence_values_file, 'r') as f:
        if args.luminescence_values_file.endswith('.json'):
            luminescence_values = json.load(f)
        else:  # Assume CSV
            luminescence_values = [float(line.strip()) for line in f if line.strip()]

    result = analyze_endolysosomal_calcium_dynamics(
        time_points=time_points,
        luminescence_values=luminescence_values,
        treatment_time=args.treatment_time,
        cell_type=args.cell_type,
        treatment_name=args.treatment_name,
        output_file=args.output_file
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'calcium_dynamics_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
