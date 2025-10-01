#!/usr/bin/env python3
"""
Wrapper for Biomni model_protein_dimerization_network tool
"""
import sys
import argparse
import os
import json


def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'networkx']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Model protein dimerization network using Biomni'
    )
    parser.add_argument('monomer_concentrations', help='JSON string or file with monomer concentrations')
    parser.add_argument('dimerization_affinities', help='JSON string or file with dimerization affinities')
    parser.add_argument('network_topology', help='JSON string or file with network topology')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Parse JSON parameters (handle both strings and file paths)
    def parse_json_param(param):
        try:
            return json.loads(param)
        except json.JSONDecodeError:
            if os.path.exists(param):
                with open(param, 'r') as f:
                    return json.load(f)
            raise ValueError(f"Parameter is neither valid JSON nor a file path: {param}")

    monomer_concentrations = parse_json_param(args.monomer_concentrations)
    dimerization_affinities = parse_json_param(args.dimerization_affinities)
    network_topology = parse_json_param(args.network_topology)

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
