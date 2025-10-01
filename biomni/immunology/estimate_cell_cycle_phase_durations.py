#!/usr/bin/env python3
"""
Camber wrapper for estimate_cell_cycle_phase_durations from biomni.tool.immunology
"""

import argparse
import sys
import json
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
        description='Estimate cell cycle phase durations from flow cytometry data'
    )
    parser.add_argument('input_file', help='JSON file with flow cytometry data and initial estimates')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    flow_cytometry_data = input_data['flow_cytometry_data']
    initial_estimates = input_data['initial_estimates']

    # Import after dependencies are installed
    from biomni.tool.immunology import estimate_cell_cycle_phase_durations

    result = estimate_cell_cycle_phase_durations(
        flow_cytometry_data=flow_cytometry_data,
        initial_estimates=initial_estimates
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cell_cycle_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
