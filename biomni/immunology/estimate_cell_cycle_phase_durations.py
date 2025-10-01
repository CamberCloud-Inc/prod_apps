#!/usr/bin/env python3
"""
Biomni Tool: Estimate Cell Cycle Phase Durations
Wraps: biomni.tool.immunology.estimate_cell_cycle_phase_durations
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Estimate Cell Cycle Phase Durations'
    )
    parser.add_argument('--flow_cytometry_data', help='Flow cytometry measurements from dual-pulse labeling (JSON dict)')
    parser.add_argument('--initial_estimates', help='Initial parameter estimates for optimization (JSON dict)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.immunology import estimate_cell_cycle_phase_durations

    # Parse JSON inputs
    flow_cytometry_data = json.loads(args.flow_cytometry_data) if args.flow_cytometry_data else None
    initial_estimates = json.loads(args.initial_estimates) if args.initial_estimates else None

    result = estimate_cell_cycle_phase_durations(
        flow_cytometry_data=flow_cytometry_data,
        initial_estimates=initial_estimates
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cell_cycle_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
