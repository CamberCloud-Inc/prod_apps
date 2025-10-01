#!/usr/bin/env python3
"""
Wrapper for Biomni perform_flux_balance_analysis tool
"""
import sys
import argparse
import os
import json


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
    parser.add_argument('model_file', help='Path to metabolic model file')
    parser.add_argument('--constraints', help='JSON string or file with flux constraints')
    parser.add_argument('--objective-reaction', help='Objective reaction for optimization')
    parser.add_argument('--output-filename', default='fba_results.csv', help='Output filename (default: fba_results.csv)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Parse JSON parameters (handle both strings and file paths)
    def parse_json_param(param):
        if not param:
            return None
        try:
            return json.loads(param)
        except json.JSONDecodeError:
            if os.path.exists(param):
                with open(param, 'r') as f:
                    return json.load(f)
            raise ValueError(f"Parameter is neither valid JSON nor a file path: {param}")

    model_file = args.model_file
    constraints = parse_json_param(args.constraints) if args.constraints else None
    objective_reaction = args.objective_reaction
    output_filename = args.output_filename

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
