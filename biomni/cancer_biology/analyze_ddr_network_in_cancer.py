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
    parser.add_argument('input_file', help='JSON file with parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import analyze_ddr_network_in_cancer

    with open(args.input_file, 'r') as f:
        params = json.load(f)

    expression_data_path = params['expression_data_path']
    mutation_data_path = params['mutation_data_path']
    output_dir = params.get('output_dir', './results')

    result = analyze_ddr_network_in_cancer(
        expression_data_path=expression_data_path,
        mutation_data_path=mutation_data_path,
        output_dir=output_dir
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'ddr_network_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
