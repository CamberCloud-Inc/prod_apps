#!/usr/bin/env python3
"""
Wrapper for Biomni perform_flux_balance_analysis tool
"""
import sys
import json
import argparse
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
        description='Perform flux balance analysis using Biomni'
    )
    parser.add_argument('input_file', help='JSON file with FBA parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    model_file = input_data.get('model_file')
    constraints = input_data.get('constraints')
    objective_reaction = input_data.get('objective_reaction')
    output_filename = input_data.get('output_file', 'fba_results.csv')

    # Import after dependencies are installed
    from biomni.tool.systems_biology import perform_flux_balance_analysis

    result = perform_flux_balance_analysis(model_file, constraints, objective_reaction, output_filename)

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'fba_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
