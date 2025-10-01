#!/usr/bin/env python3
"""Biomni Tool: Interspecies Gene Conversion
Wraps: biomni.tool.genomics.interspecies_gene_conversion
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    deps = ['biomni', 'pybiomart', 'pandas', 'numpy']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Convert ENSEMBL gene IDs between different species using BioMart'
    )
    parser.add_argument('gene_list_file', help='JSON file with list of ENSEMBL gene IDs from stash')
    parser.add_argument('--source-species', required=True,
                       help='Source species (human, mouse, rat, zebrafish, fly, worm, yeast, chicken, pig, cow, dog, macaque)')
    parser.add_argument('--target-species', required=True,
                       help='Target species (human, mouse, rat, zebrafish, fly, worm, yeast, chicken, pig, cow, dog, macaque)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load gene list
    with open(args.gene_list_file, 'r') as f:
        gene_list = json.load(f)

    if not isinstance(gene_list, list):
        raise ValueError("Gene list file must contain a JSON array of gene IDs")

    from biomni.tool.genomics import interspecies_gene_conversion

    result = interspecies_gene_conversion(
        gene_list=gene_list,
        source_species=args.source_species,
        target_species=args.target_species
    )

    output_file = os.path.join(args.output, 'conversion_log.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")
    print(f"Conversion CSV: {args.source_species}_to_{args.target_species}_gene_conversion.csv")

if __name__ == '__main__':
    main()
