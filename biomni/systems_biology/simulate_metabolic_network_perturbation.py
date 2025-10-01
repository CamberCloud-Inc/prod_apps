#!/usr/bin/env python3
"""
Wrapper for Biomni simulate_metabolic_network_perturbation tool
"""
import sys
import json
import argparse
import os


def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Simulate metabolic network perturbation using Biomni'
    )
    parser.add_argument('input_file', help='JSON file with simulation parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    model_file = input_data.get('model_file')
    initial_concentrations = input_data.get('initial_concentrations')
    perturbation_params = input_data.get('perturbation_params')
    simulation_time = input_data.get('simulation_time', 100)
    time_points = input_data.get('time_points', 1000)

    # Import after dependencies are installed
    from biomni.tool.systems_biology import simulate_metabolic_network_perturbation

    result = simulate_metabolic_network_perturbation(
        model_file, initial_concentrations, perturbation_params, simulation_time, time_points
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'metabolic_network_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
