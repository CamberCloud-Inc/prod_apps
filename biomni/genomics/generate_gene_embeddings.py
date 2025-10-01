#!/usr/bin/env python3
"""Biomni Tool: Generate Gene Embeddings with ESM Models
Wraps: biomni.tool.genomics.generate_gene_embeddings_with_ESM_models
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    deps = ['biomni', 'torch', 'fair-esm', 'requests', 'tqdm']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Generate protein embeddings for genes using ESM language models'
    )
    parser.add_argument('gene_ids', help='Comma-separated list of ENSEMBL gene IDs (e.g., "ENSG00000139618,ENSG00000141510")')
    parser.add_argument('--model-name', default='esm2_t6_8M_UR50D',
                       help='ESM model name (default: esm2_t6_8M_UR50D)')
    parser.add_argument('--layer', type=int, default=6,
                       help='Layer to extract embeddings from (default: 6)')
    parser.add_argument('--batch-size', type=int, default=1,
                       help='Batch size for processing (default: 1)')
    parser.add_argument('--max-length', type=int, default=1024,
                       help='Maximum sequence length (default: 1024)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Parse gene IDs from comma-separated string
    gene_ids = [g.strip() for g in args.gene_ids.split(',') if g.strip()]

    if not gene_ids:
        raise ValueError("No gene IDs provided")

    from biomni.tool.genomics import generate_gene_embeddings_with_ESM_models

    save_path = os.path.join(args.output, 'gene_embeddings.pt')
    result = generate_gene_embeddings_with_ESM_models(
        ensembl_gene_ids=gene_ids,
        model_name=args.model_name,
        layer=args.layer,
        save_path=save_path,
        batch_size=args.batch_size,
        max_sequence_length=args.max_length
    )

    output_file = os.path.join(args.output, 'embeddings_log.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")
    print(f"Embeddings saved to: {save_path}")

if __name__ == '__main__':
    main()
