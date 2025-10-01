#!/usr/bin/env python3
"""Biomni Tool: Annotate Cell Type with PanhumanPy
Wraps: biomni.tool.genomics.annotate_celltype_with_panhumanpy
"""
import argparse
import sys
import subprocess
import os

def install_dependencies():
    deps = ['biomni', 'scanpy', 'anndata', 'panhumanpy']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Hierarchical cell type annotation using panhumanpy and Azimuth Neural Network'
    )
    parser.add_argument('adata_file', help='AnnData H5AD file from stash')
    parser.add_argument('--feature-names-col', default=None,
                       help='Column name in adata.var containing gene names (default: use index)')
    parser.add_argument('--no-refine', action='store_true',
                       help='Skip label refinement for consistent granularity')
    parser.add_argument('--no-umap', action='store_true',
                       help='Skip ANN embeddings and UMAP generation')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.genomics import annotate_celltype_with_panhumanpy

    result = annotate_celltype_with_panhumanpy(
        adata_path=args.adata_file,
        feature_names_col=args.feature_names_col,
        refine=not args.no_refine,
        umap=not args.no_umap,
        output_dir=args.output
    )

    output_file = os.path.join(args.output, 'annotation_log.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
