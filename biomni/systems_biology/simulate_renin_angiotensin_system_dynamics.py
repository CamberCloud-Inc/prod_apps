#!/usr/bin/env python3
"""
Wrapper for Biomni simulate_renin_angiotensin_system_dynamics tool
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
        description='Simulate renin-angiotensin system dynamics using Biomni'
    )
    parser.add_argument('initial_concentrations', help='JSON string or file with initial concentrations')
    parser.add_argument('rate_constants', help='JSON string or file with rate constants')
    parser.add_argument('feedback_params', help='JSON string or file with feedback parameters')
    parser.add_argument('--simulation-time', type=float, default=48, help='Simulation time (default: 48)')
    parser.add_argument('--time-points', type=int, default=100, help='Number of time points (default: 100)')
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

    initial_concentrations = parse_json_param(args.initial_concentrations)
    rate_constants = parse_json_param(args.rate_constants)
    feedback_params = parse_json_param(args.feedback_params)
    simulation_time = args.simulation_time
    time_points = args.time_points

    # Import after dependencies are installed
    from biomni.tool.systems_biology import simulate_renin_angiotensin_system_dynamics

    result = simulate_renin_angiotensin_system_dynamics(
        initial_concentrations, rate_constants, feedback_params, simulation_time, time_points
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'renin_angiotensin_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
