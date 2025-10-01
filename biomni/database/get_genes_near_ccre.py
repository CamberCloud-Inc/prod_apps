#!/usr/bin/env python3
"""
Biomni Tool: Get Genes Near Ccre
Wraps: biomni.tool.database.get_genes_near_ccre
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
        description='Get Genes Near Ccre'
    )
    parser.add_argument('--accession', required=True, help='cCRE accession ID')
    parser.add_argument('--assembly', required=True, help='Genome assembly (e.g., 'GRCh38')')
    parser.add_argument('--chromosome', required=True, help='Chromosome name')
    parser.add_argument('--k', default='10', help='Number of nearest genes to return (default: 10)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.database import get_genes_near_ccre

    result = get_genes_near_ccre(
        accession=args.accession,
        assembly=args.assembly,
        chromosome=args.chromosome,
        k=int(args.k) if args.k else None
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'genes_near_ccre.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
