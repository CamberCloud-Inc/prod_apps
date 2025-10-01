#!/usr/bin/env python3
"""
Simulate microbial community dynamics using the generalized Lotka-Volterra model.
"""

import sys
import json
import argparse
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'biopython']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Simulate microbial community dynamics using the generalized Lotka-Volterra model.'
    )
    parser.add_argument('--initial-populations', type=str, required=True, help='Initial population sizes for each species (JSON string)')
    parser.add_argument('--growth-rates', type=str, required=True, help='Growth rates for each species (JSON string)')
    parser.add_argument('--interaction-matrix', type=str, required=True, help='Interaction matrix between species (JSON string)')
    parser.add_argument('--simulation-time', type=float, default=100, help='Total simulation time')
    parser.add_argument('--time-step', type=float, default=0.1, help='Time step for numerical integration')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import simulate_generalized_lotka_volterra_dynamics

    # Parse JSON string parameters
    initial_populations = json.loads(args.initial_populations)
    growth_rates = json.loads(args.growth_rates)
    interaction_matrix = json.loads(args.interaction_matrix)

    # Call the function
    result = simulate_generalized_lotka_volterra_dynamics(
        initial_populations=initial_populations,
        growth_rates=growth_rates,
        interaction_matrix=interaction_matrix,
        simulation_time=args.simulation_time,
        time_step=args.time_step
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'lotka_volterra_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
