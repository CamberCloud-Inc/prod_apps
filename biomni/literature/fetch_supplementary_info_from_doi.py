#!/usr/bin/env python3
"""
Camber wrapper for fetch_supplementary_info_from_doi from biomni.tool.literature
"""

import argparse
import sys
import json
import subprocess
import os


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Fetch supplementary information from DOI'
    )
    parser.add_argument('input_file', help='JSON file with DOI from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    doi = input_data['doi']

    # Import after dependencies are installed
    from biomni.tool.literature import fetch_supplementary_info_from_doi

    # Create output directory and use it for supplementary files
    os.makedirs(args.output, exist_ok=True)

    result = fetch_supplementary_info_from_doi(doi=doi, output_dir=args.output)

    # Write summary output
    output_file = os.path.join(args.output, 'supplementary_info.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
