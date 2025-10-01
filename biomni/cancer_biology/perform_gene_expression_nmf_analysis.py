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
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Perform gene expression NMF analysis'
    )
    parser.add_argument('input_file', help='JSON file with parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import perform_gene_expression_nmf_analysis

    with open(args.input_file, 'r') as f:
        params = json.load(f)

    expression_data_path = params['expression_data_path']
    n_components = params.get('n_components', 5)
    output_dir = params.get('output_dir', './results')

    result = perform_gene_expression_nmf_analysis(
        expression_data_path=expression_data_path,
        n_components=n_components,
        output_dir=output_dir
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'nmf_analysis_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
