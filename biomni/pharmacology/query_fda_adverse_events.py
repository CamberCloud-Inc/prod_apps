#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.query_fda_adverse_events
Queries FDA adverse events database.
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
        description='Queries FDA adverse events database'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    drug_name = input_data.get('drug_name')
    date_range = input_data.get('date_range')
    severity_filter = input_data.get('severity_filter')
    outcome_filter = input_data.get('outcome_filter')
    limit = input_data.get('limit', 100)

    if not drug_name:
        raise ValueError("Missing required parameter: drug_name")

    # Convert date_range to tuple if it's a list
    if date_range and isinstance(date_range, list):
        date_range = tuple(date_range)

    # Import after dependencies are installed
    from biomni.tool.pharmacology import query_fda_adverse_events

    result = query_fda_adverse_events(
        drug_name=drug_name,
        date_range=date_range,
        severity_filter=severity_filter,
        outcome_filter=outcome_filter,
        limit=limit
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'fda_adverse_events_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
