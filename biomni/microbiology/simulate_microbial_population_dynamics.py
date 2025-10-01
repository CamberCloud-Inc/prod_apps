#!/usr/bin/env python3
"""
Simulate microbial population dynamics with multiple interacting species.
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
        description='Simulate microbial population dynamics with multiple interacting species.'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import simulate_microbial_population_dynamics

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    species_params = input_data.get('species_params')
    interactions = input_data.get('interactions')
    simulation_time = input_data.get('simulation_time', 100)
    time_step = input_data.get('time_step', 0.1)

    # Call the function
    result = simulate_microbial_population_dynamics(
        species_params=species_params,
        interactions=interactions,
        simulation_time=simulation_time,
        time_step=time_step
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'population_dynamics_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
