#!/usr/bin/env python3
"""
Simulate Thyroid Hormone Pharmacokinetics

Simulates the transport and binding of thyroid hormones across different tissue compartments
using an ODE-based pharmacokinetic model.
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
        description='Simulate Thyroid Hormone Pharmacokinetics'
    )
    parser.add_argument('input_file', help='Input JSON file with parameters, initial_conditions and optional time settings')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import simulate_thyroid_hormone_pharmacokinetics

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    parameters = inputs['parameters']
    initial_conditions = inputs['initial_conditions']
    time_span = inputs.get('time_span', [0, 24])
    time_points = inputs.get('time_points', 100)

    result = simulate_thyroid_hormone_pharmacokinetics(
        parameters=parameters,
        initial_conditions=initial_conditions,
        time_span=tuple(time_span),
        time_points=time_points
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'thyroid_hormone_pharmacokinetics_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
