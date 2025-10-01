#!/usr/bin/env python3
"""
Model bacterial population dynamics over time using ordinary differential equations.
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
        description='Model bacterial population dynamics over time using ordinary differential equations.'
    )
    parser.add_argument('--initial-population', type=float, required=True, help='Initial bacterial population size')
    parser.add_argument('--growth-rate', type=float, required=True, help='Bacterial growth rate (per hour)')
    parser.add_argument('--clearance-rate', type=float, required=True, help='Bacterial clearance/death rate (per hour)')
    parser.add_argument('--niche-size', type=float, required=True, help='Maximum carrying capacity of the niche')
    parser.add_argument('--simulation-time', type=float, default=24, help='Total simulation time in hours')
    parser.add_argument('--time-step', type=float, default=0.1, help='Time step for numerical integration')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import model_bacterial_growth_dynamics

    # Call the function
    result = model_bacterial_growth_dynamics(
        initial_population=args.initial_population,
        growth_rate=args.growth_rate,
        clearance_rate=args.clearance_rate,
        niche_size=args.niche_size,
        simulation_time=args.simulation_time,
        time_step=args.time_step
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'growth_dynamics_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
