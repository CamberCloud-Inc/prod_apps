#!/usr/bin/env python3
"""
Camber app wrapper for simulate_gene_circuit_with_growth_feedback from biomni.tool.synthetic_biology
"""

import argparse
import sys
import json
import os
import subprocess
import numpy as np


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni', 'numpy']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Simulate gene circuit with growth feedback'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.synthetic_biology import simulate_gene_circuit_with_growth_feedback

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    circuit_topology = np.array(input_data.get("circuit_topology"))
    kinetic_params = input_data.get("kinetic_params")
    growth_params = input_data.get("growth_params")
    simulation_time = input_data.get("simulation_time", 100)
    time_points = input_data.get("time_points", 1000)

    # Call the function
    result = simulate_gene_circuit_with_growth_feedback(
        circuit_topology=circuit_topology,
        kinetic_params=kinetic_params,
        growth_params=growth_params,
        simulation_time=simulation_time,
        time_points=time_points
    )

    # Write result to file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'gene_circuit_simulation.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
