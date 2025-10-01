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
    parser.add_argument('--species-params', type=str, required=True, help='Parameters for each species (JSON string)')
    parser.add_argument('--interactions', type=str, required=True, help='Interaction parameters between species (JSON string)')
    parser.add_argument('--simulation-time', type=float, default=100, help='Total simulation time')
    parser.add_argument('--time-step', type=float, default=0.1, help='Time step for numerical integration')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import simulate_microbial_population_dynamics

    # Parse JSON string parameters
    species_params = json.loads(args.species_params)
    interactions = json.loads(args.interactions)

    # Call the function
    result = simulate_microbial_population_dynamics(
        species_params=species_params,
        interactions=interactions,
        simulation_time=args.simulation_time,
        time_step=args.time_step
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'population_dynamics_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
