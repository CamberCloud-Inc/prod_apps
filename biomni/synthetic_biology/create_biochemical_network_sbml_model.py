#!/usr/bin/env python3
"""
Camber app wrapper for create_biochemical_network_sbml_model from biomni.tool.synthetic_biology
"""

import argparse
import sys
import json
import os
import subprocess


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Create biochemical network SBML model'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.synthetic_biology import create_biochemical_network_sbml_model

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    reaction_network = input_data.get("reaction_network")
    kinetic_parameters = input_data.get("kinetic_parameters")
    output_file = input_data.get("output_file", "biochemical_model.xml")

    # Call the function
    result = create_biochemical_network_sbml_model(
        reaction_network=reaction_network,
        kinetic_parameters=kinetic_parameters,
        output_file=output_file
    )

    # Write result to file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'sbml_model_result.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
