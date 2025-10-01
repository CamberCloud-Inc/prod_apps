#!/usr/bin/env python3
"""Biomni Tool: Analyze Comparative Genomics and Haplotypes
Wraps: biomni.tool.genomics.analyze_comparative_genomics_and_haplotypes
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    deps = ['biomni', 'biopython', 'pandas', 'numpy']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Perform comparative genomics and haplotype analysis on multiple genome samples'
    )
    parser.add_argument('sample_files_json', help='JSON file with list of sample FASTA file paths from stash')
    parser.add_argument('reference_genome', help='Reference genome FASTA file from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load sample files list
    with open(args.sample_files_json, 'r') as f:
        sample_files = json.load(f)

    if not isinstance(sample_files, list):
        raise ValueError("Sample files JSON must contain an array of file paths")

    from biomni.tool.genomics import analyze_comparative_genomics_and_haplotypes

    result = analyze_comparative_genomics_and_haplotypes(
        sample_fasta_files=sample_files,
        reference_genome_path=args.reference_genome,
        output_dir=args.output
    )

    output_file = os.path.join(args.output, 'comparative_genomics_log.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
