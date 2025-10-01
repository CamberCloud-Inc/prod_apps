#!/usr/bin/env python3
"""Biomni Tool: Create Harmony Embeddings
Wraps: biomni.tool.genomics.create_harmony_embeddings_scRNA
"""
import argparse
import sys
import subprocess
import os

def install_dependencies():
    deps = ['biomni', 'scanpy', 'anndata', 'harmony-pytorch']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Create Harmony batch-corrected embeddings for single-cell RNA-seq data'
    )
    parser.add_argument('adata_file', help='AnnData H5AD file from stash')
    parser.add_argument('--batch-key', required=True,
                       help='Column name in adata.obs for batch information')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.genomics import create_harmony_embeddings_scRNA

    result = create_harmony_embeddings_scRNA(
        adata_filename=args.adata_file,
        batch_key=args.batch_key,
        data_dir=args.output
    )

    output_file = os.path.join(args.output, 'harmony_log.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")
    print(f"Embeddings saved to: {os.path.join(args.output, 'harmony_emb_data.h5ad')}")

if __name__ == '__main__':
    main()
