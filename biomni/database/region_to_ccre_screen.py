#!/usr/bin/env python3
"""
Biomni Tool: Region to cCRE Screen
Wraps: biomni.tool.database.region_to_ccre_screen
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
        description='Get cCREs intersecting with a genomic region'
    )
    parser.add_argument('input_file', help='JSON file with parameters from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    from biomni.tool.database import region_to_ccre_screen

    result = region_to_ccre_screen(
        coord_chrom=input_data.get('coord_chrom'),
        coord_start=input_data.get('coord_start'),
        coord_end=input_data.get('coord_end'),
        assembly=input_data.get('assembly', 'GRCh38')
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'region_to_ccre.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
