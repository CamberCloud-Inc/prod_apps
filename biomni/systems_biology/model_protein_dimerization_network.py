#!/usr/bin/env python3
"""
Wrapper for Biomni model_protein_dimerization_network tool
"""
import sys
import json
from biomni.tool.systems_biology import model_protein_dimerization_network


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
    
    install_dependencies()
    if len(sys.argv) != 4:
        print("Usage: model_protein_dimerization_network.py <monomer_concentrations_json> <dimerization_affinities_json> <network_topology_json>")
        sys.exit(1)

    monomer_concentrations = json.loads(sys.argv[1])
    dimerization_affinities = json.loads(sys.argv[2])
    network_topology = json.loads(sys.argv[3])

    result = model_protein_dimerization_network(monomer_concentrations, dimerization_affinities, network_topology)
    print(result)

if __name__ == "__main__":
    main()
