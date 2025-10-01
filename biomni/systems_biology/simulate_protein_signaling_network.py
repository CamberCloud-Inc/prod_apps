#!/usr/bin/env python3
"""
Wrapper for Biomni simulate_protein_signaling_network tool
"""
import sys
import json
from biomni.tool.systems_biology import simulate_protein_signaling_network


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
    if len(sys.argv) < 4:
        print("Usage: simulate_protein_signaling_network.py <network_structure_json> <reaction_params_json> <species_params_json> [simulation_time] [time_points]")
        sys.exit(1)

    network_structure = json.loads(sys.argv[1])
    reaction_params = json.loads(sys.argv[2])
    species_params = json.loads(sys.argv[3])
    simulation_time = float(sys.argv[4]) if len(sys.argv) > 4 else 100
    time_points = int(sys.argv[5]) if len(sys.argv) > 5 else 1000

    result = simulate_protein_signaling_network(
        network_structure, reaction_params, species_params, simulation_time, time_points
    )
    print(result)

if __name__ == "__main__":
    main()
