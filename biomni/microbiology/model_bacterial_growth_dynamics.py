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
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import model_bacterial_growth_dynamics

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    initial_population = input_data.get('initial_population')
    growth_rate = input_data.get('growth_rate')
    clearance_rate = input_data.get('clearance_rate')
    niche_size = input_data.get('niche_size')
    simulation_time = input_data.get('simulation_time', 24)
    time_step = input_data.get('time_step', 0.1)

    # Call the function
    result = model_bacterial_growth_dynamics(
        initial_population=initial_population,
        growth_rate=growth_rate,
        clearance_rate=clearance_rate,
        niche_size=niche_size,
        simulation_time=simulation_time,
        time_step=time_step
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'growth_dynamics_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
