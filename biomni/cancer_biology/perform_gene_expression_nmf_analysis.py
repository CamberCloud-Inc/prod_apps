#!/usr/bin/env python3
"""
Wrapper for Biomni perform_gene_expression_nmf_analysis tool
"""

import argparse
import sys
import json
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['FlowCytometryTools', 'biomni', 'gseapy']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Perform gene expression NMF analysis'
    )
    parser.add_argument('expression_data_path', help='Path to gene expression data file')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('-n', '--n-components', type=int, default=5, help='Number of NMF components/signatures to extract (default: 5)')
    parser.add_argument('--output-dir', default='./results', help='Directory for output files (default: ./results)')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import perform_gene_expression_nmf_analysis

    result = perform_gene_expression_nmf_analysis(
        expression_data_path=args.expression_data_path,
        n_components=args.n_components,
        output_dir=args.output_dir
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'nmf_analysis_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
