#!/usr/bin/env python3
"""
Biomni Tool: Query ClinicalTrials
Wraps: biomni.tool.database.query_clinicaltrials
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
        description='Query ClinicalTrials.gov API for clinical studies'
    )
    parser.add_argument('input_file', help='JSON file with parameters from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    from biomni.tool.database import query_clinicaltrials

    result = query_clinicaltrials(
        prompt=input_data.get('prompt'),
        endpoint=input_data.get('endpoint'),
        term=input_data.get('term'),
        status=input_data.get('status'),
        condition=input_data.get('condition'),
        intervention=input_data.get('intervention'),
        location=input_data.get('location'),
        phase=input_data.get('phase'),
        page_size=input_data.get('page_size', 10),
        max_pages=input_data.get('max_pages', 1),
        page_token=input_data.get('page_token'),
        verbose=input_data.get('verbose', True)
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'clinicaltrials_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
