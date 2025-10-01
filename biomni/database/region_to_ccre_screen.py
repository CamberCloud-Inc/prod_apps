#!/usr/bin/env python3
"""
Biomni Tool: Region To Ccre Screen
Wraps: biomni.tool.database.region_to_ccre_screen
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni', 'biopython']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Region To Ccre Screen'
    )
    parser.add_argument('--coord_chrom', required=True, help='Chromosome name')
    parser.add_argument('--coord_start', required=True, help='Start genomic coordinate')
    parser.add_argument('--coord_end', required=True, help='End genomic coordinate')
    parser.add_argument('--assembly', default='GRCh38', help='Genome assembly (default: GRCh38)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.database import region_to_ccre_screen

    result = region_to_ccre_screen(
        coord_chrom=args.coord_chrom,
        coord_start=args.coord_start,
        coord_end=args.coord_end,
        assembly=args.assembly
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'region_to_ccre.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
