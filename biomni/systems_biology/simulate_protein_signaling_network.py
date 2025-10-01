#!/usr/bin/env python3
"""
Wrapper for Biomni simulate_protein_signaling_network tool
"""
import sys
import argparse
import os
import json


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
        description='Simulate protein signaling network using Biomni'
    )
    parser.add_argument('network_structure', help='JSON string or file with network structure')
    parser.add_argument('reaction_params', help='JSON string or file with reaction parameters')
    parser.add_argument('species_params', help='JSON string or file with species parameters')
    parser.add_argument('--simulation-time', type=float, default=100, help='Simulation time (default: 100)')
    parser.add_argument('--time-points', type=int, default=1000, help='Number of time points (default: 1000)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Parse JSON parameters (handle both strings and file paths)
    def parse_json_param(param):
        try:
            return json.loads(param)
        except json.JSONDecodeError:
            if os.path.exists(param):
                with open(param, 'r') as f:
                    return json.load(f)
            raise ValueError(f"Parameter is neither valid JSON nor a file path: {param}")

    network_structure = parse_json_param(args.network_structure)
    reaction_params = parse_json_param(args.reaction_params)
    species_params = parse_json_param(args.species_params)
    simulation_time = args.simulation_time
    time_points = args.time_points

    # Import after dependencies are installed
    from biomni.tool.systems_biology import simulate_protein_signaling_network

    result = simulate_protein_signaling_network(
        network_structure, reaction_params, species_params, simulation_time, time_points
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'signaling_network_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
