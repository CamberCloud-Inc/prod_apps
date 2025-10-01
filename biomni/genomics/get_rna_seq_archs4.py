#!/usr/bin/env python3
"""Biomni Tool: Get RNA-seq from ARCHS4
Wraps: biomni.tool.genomics.get_rna_seq_archs4
"""
import argparse
import sys
import subprocess
import os

def install_dependencies():
    deps = ['biomni', 'gget']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Fetch RNA-seq expression data for a gene from ARCHS4 database'
    )
    parser.add_argument('gene_name', help='Gene name to query')
    parser.add_argument('--top-k', type=int, default=10,
                       help='Number of top tissues to return (default: 10)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.genomics import get_rna_seq_archs4

    result = get_rna_seq_archs4(gene_name=args.gene_name, K=args.top_k)

    output_file = os.path.join(args.output, 'rna_seq_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
