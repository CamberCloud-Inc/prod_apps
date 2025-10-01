#!/usr/bin/env python3
"""Biomni Tool: Download Synapse Data
Wraps: biomni.tool.support_tools.download_synapse_data
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
        description='Download data from Synapse repository'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Read input file with parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters from input data
    entity_ids = input_data.get('entity_ids')
    download_location = input_data.get('download_location')
    follow_link = input_data.get('follow_link', False)
    recursive = input_data.get('recursive', False)
    timeout = input_data.get('timeout', 300)
    entity_type = input_data.get('entity_type', 'file')

    # Import after dependencies are installed
    from biomni.tool.support_tools import download_synapse_data

    result = download_synapse_data(
        entity_ids=entity_ids,
        download_location=download_location,
        follow_link=follow_link,
        recursive=recursive,
        timeout=timeout,
        entity_type=entity_type
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'download_result.txt')
    with open(output_file, 'w') as f:
        f.write(str(result))
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
