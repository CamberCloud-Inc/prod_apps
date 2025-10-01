#!/usr/bin/env python3
"""Biomni Tool: Gene Set Enrichment Analysis
Wraps: biomni.tool.genomics.gene_set_enrichment_analysis
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    deps = ['biomni', 'gget', 'gseapy']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Perform gene set enrichment analysis using multiple databases'
    )
    parser.add_argument('genes', help='Comma-separated list of gene symbols (e.g., "BRCA1,TP53,EGFR")')
    parser.add_argument('--database', default='ontology',
                       help='Database: pathway, transcription, ontology, diseases_drugs, celltypes, kinase_interactions (default: ontology)')
    parser.add_argument('--top-k', type=int, default=10,
                       help='Number of top pathways to return (default: 10)')
    parser.add_argument('--background', default=None,
                       help='Optional comma-separated list of background genes')
    parser.add_argument('--plot', action='store_true',
                       help='Generate bar plot of results')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Parse gene list from comma-separated string
    genes = [g.strip() for g in args.genes.split(',') if g.strip()]

    if not genes:
        raise ValueError("No genes provided")

    # Parse background if provided
    background_list = None
    if args.background:
        background_list = [g.strip() for g in args.background.split(',') if g.strip()]

    from biomni.tool.genomics import gene_set_enrichment_analysis

    result = gene_set_enrichment_analysis(
        genes=genes,
        top_k=args.top_k,
        database=args.database,
        background_list=background_list,
        plot=args.plot
    )

    output_file = os.path.join(args.output, 'enrichment_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
