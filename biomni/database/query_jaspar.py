#!/usr/bin/env python3
"""
Biomni Tool: Query JASPAR
Wraps: biomni.tool.database.query_jaspar
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
        description='Query the JASPAR REST API'
    )
    parser.add_argument('input_file', help='JSON file with parameters from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    from biomni.tool.database import query_jaspar

    result = query_jaspar(prompt=input_data.get('prompt'),
        endpoint=input_data.get('endpoint'),
        verbose=input_data.get('verbose'))

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'jaspar_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
