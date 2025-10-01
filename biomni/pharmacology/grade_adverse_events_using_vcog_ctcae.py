#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.grade_adverse_events_using_vcog_ctcae
Grades adverse events using VCOG-CTCAE criteria.
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
        description='Grades adverse events using VCOG-CTCAE criteria'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    clinical_data_file = input_data.get('clinical_data_file')

    if not clinical_data_file:
        raise ValueError("Missing required parameter: clinical_data_file")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import grade_adverse_events_using_vcog_ctcae

    result = grade_adverse_events_using_vcog_ctcae(
        clinical_data_file=clinical_data_file
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'adverse_events_grading_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
