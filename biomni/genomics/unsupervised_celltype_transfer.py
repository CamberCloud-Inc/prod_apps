#!/usr/bin/env python3
"""Biomni Tool: Unsupervised Cell Type Transfer
Wraps: biomni.tool.genomics.unsupervised_celltype_transfer_between_scRNA_datasets
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    deps = ['biomni', 'scanpy', 'anndata', 'popv']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Transfer cell type annotations between single-cell RNA-seq datasets using popV'
    )
    parser.add_argument('annotated_h5ad', help='Reference annotated H5AD file from stash')
    parser.add_argument('query_h5ad', help='Query H5AD file to annotate from stash')
    parser.add_argument('--ref-labels-key', required=True, help='Column name in ref_adata.obs for cell type labels')
    parser.add_argument('--query-batch-key', default=None, help='Batch key for query dataset')
    parser.add_argument('--ref-batch-key', default=None, help='Batch key for reference dataset')
    parser.add_argument('--celltypist', action='store_true', help='Use CELLTYPIST method')
    parser.add_argument('--knn-bbknn', action='store_true', help='Use KNN_BBKNN method')
    parser.add_argument('--knn-harmony', action='store_true', help='Use KNN_HARMONY method')
    parser.add_argument('--knn-scanorama', action='store_true', help='Use KNN_SCANORAMA method')
    parser.add_argument('--knn-scvi', action='store_true', help='Use KNN_SCVI method')
    parser.add_argument('--onclass', action='store_true', help='Use ONCLASS method')
    parser.add_argument('--random-forest', action='store_true', help='Use Random_Forest method')
    parser.add_argument('--scanvi-popv', action='store_true', default=True, help='Use SCANVI_POPV method (default)')
    parser.add_argument('--support-vector', action='store_true', help='Use Support_Vector method')
    parser.add_argument('--xgboost', action='store_true', help='Use XGboost method')
    parser.add_argument('--n-jobs', type=int, default=1, help='Number of parallel jobs')
    parser.add_argument('--n-samples-per-label', type=int, default=10, help='Samples per label')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.genomics import unsupervised_celltype_transfer_between_scRNA_datasets

    result = unsupervised_celltype_transfer_between_scRNA_datasets(
        path_to_annotated_h5ad=args.annotated_h5ad,
        path_to_not_annotated_h5ad=args.query_h5ad,
        ref_labels_key=args.ref_labels_key,
        query_batch_key=args.query_batch_key,
        ref_batch_key=args.ref_batch_key,
        CELLTYPIST=args.celltypist,
        KNN_BBKNN=args.knn_bbknn,
        KNN_HARMONY=args.knn_harmony,
        KNN_SCANORAMA=args.knn_scanorama,
        KNN_SCVI=args.knn_scvi,
        ONCLASS=args.onclass,
        Random_Forest=args.random_forest,
        SCANVI_POPV=args.scanvi_popv,
        Support_Vector=args.support_vector,
        XGboost=args.xgboost,
        n_jobs=args.n_jobs,
        output_folder=args.output,
        n_samples_per_label=args.n_samples_per_label
    )

    output_file = os.path.join(args.output, 'transfer_log.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
