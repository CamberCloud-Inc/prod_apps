#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_xenograft_tumor_growth_inhibition
Analyzes xenograft tumor growth inhibition data.
"""

import argparse
import sys
import subprocess
import os
import json


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyzes xenograft tumor growth inhibition data'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    data_path = input_data.get('data_path')
    time_column = input_data.get('time_column')
    volume_column = input_data.get('volume_column')
    group_column = input_data.get('group_column')
    subject_column = input_data.get('subject_column')
    output_dir = input_data.get('output_dir', './results')

    if not data_path or not time_column or not volume_column or not group_column or not subject_column:
        raise ValueError("Missing required parameters: data_path, time_column, volume_column, group_column, subject_column")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import analyze_xenograft_tumor_growth_inhibition

    result = analyze_xenograft_tumor_growth_inhibition(
        data_path=data_path,
        time_column=time_column,
        volume_column=volume_column,
        group_column=group_column,
        subject_column=subject_column,
        output_dir=output_dir
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'xenograft_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
