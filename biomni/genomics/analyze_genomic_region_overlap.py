#!/usr/bin/env python3
"""Biomni Tool: Analyze Genomic Region Overlap
Wraps: biomni.tool.genomics.analyze_genomic_region_overlap
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    deps = ['biomni', 'pybedtools', 'pandas']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Analyze overlaps between two or more sets of genomic regions'
    )
    parser.add_argument('bed_files', nargs='+',
                       help='Two or more BED files to analyze for overlaps')
    parser.add_argument('--output-prefix', default='overlap_analysis',
                       help='Prefix for output files (default: overlap_analysis)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Use bed files directly
    region_sets = args.bed_files

    if len(region_sets) < 2:
        raise ValueError("At least two BED files are required for overlap analysis")

    from biomni.tool.genomics import analyze_genomic_region_overlap

    # Update output prefix to include directory
    output_prefix = os.path.join(args.output, args.output_prefix)

    result = analyze_genomic_region_overlap(
        region_sets=region_sets,
        output_prefix=output_prefix
    )

    output_file = os.path.join(args.output, 'overlap_analysis_log.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
