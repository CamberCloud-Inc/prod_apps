#!/usr/bin/env python3
"""
Optimize anaerobic digestion process conditions to maximize VFA production or methane yield.
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
        description='Optimize anaerobic digestion process conditions to maximize VFA production or methane yield.'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import optimize_anaerobic_digestion_process

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    waste_characteristics = input_data.get('waste_characteristics')
    operational_parameters = input_data.get('operational_parameters')
    target_output = input_data.get('target_output', 'methane_yield')
    optimization_method = input_data.get('optimization_method', 'rsm')

    # Call the function
    result = optimize_anaerobic_digestion_process(
        waste_characteristics=waste_characteristics,
        operational_parameters=operational_parameters,
        target_output=target_output,
        optimization_method=optimization_method
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'digestion_optimization_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
