#!/usr/bin/env python3
"""
Wrapper for Biomni model_protein_dimerization_network tool
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
        description='Model protein dimerization network using Biomni'
    )
    parser.add_argument('input_file', help='JSON file with network parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    monomer_concentrations = input_data.get('monomer_concentrations')
    dimerization_affinities = input_data.get('dimerization_affinities')
    network_topology = input_data.get('network_topology')

    # Import after dependencies are installed
    from biomni.tool.systems_biology import model_protein_dimerization_network

    result = model_protein_dimerization_network(monomer_concentrations, dimerization_affinities, network_topology)

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'dimerization_network_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
