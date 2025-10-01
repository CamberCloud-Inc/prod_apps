#!/usr/bin/env python3
"""
Biomni Tool: Query IUCN
Wraps: biomni.tool.database.query_iucn
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
        description='Query the IUCN Red List API'
    )
    parser.add_argument('input_file', help='JSON file with parameters from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    from biomni.tool.database import query_iucn

    result = query_iucn(prompt=input_data.get('prompt'),
        endpoint=input_data.get('endpoint'),
        token=input_data.get('token'),
        verbose=input_data.get('verbose'))

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'iucn_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
