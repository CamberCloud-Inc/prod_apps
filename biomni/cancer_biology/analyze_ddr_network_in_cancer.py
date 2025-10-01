#!/usr/bin/env python3
"""
Wrapper for Biomni analyze_ddr_network_in_cancer tool
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
        description='Analyze DNA damage response network in cancer'
    )
    parser.add_argument('expression_data_path', help='Path to gene expression data file')
    parser.add_argument('mutation_data_path', help='Path to mutation data file (VCF or MAF format)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('--output-dir', default='./results', help='Directory for output files (default: ./results)')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import analyze_ddr_network_in_cancer

    result = analyze_ddr_network_in_cancer(
        expression_data_path=args.expression_data_path,
        mutation_data_path=args.mutation_data_path,
        output_dir=args.output_dir
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'ddr_network_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
